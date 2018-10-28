from IPy import IP
import re
import hbase_client
import uuid
import time
import tldextract
from datetime import datetime
from location.geo_ip import GeoIPUtil

log_file_path = '/home/ubuntu/datasets/nasa_log_jul'
regex = "(.*) - - \[(.*)\] \"([A-Z]+) (.*)\" ([0-9]{3}) (-|[0-9]+)"
pattern = re.compile(regex)

FAMILIES = ['log_info','loca_info']
TABLE = 'server_logs_new'
LOG_COLS =  ["log_info:host", "log_info:server_ts", "log_info:type", "log_info:url", "log_info:status", "log_info:bytes"]
#hbase_client.truncate_table(TABLE, FAMILIES)

###########################
#Metadata setup
###########################
tgt_time_fmt = "%Y-%m-%d %H:%M:%S"
src_time_fmt = "%d/%b/%Y:%H:%M:%S %z"

start_time = "1995-08-01 00:00:00"
meta = metadata(truncate=True)
meta.initialize_timer(start_time=start_time)
window = meta.next_bound()
lower_b = time.mktime(time.strptime(start_time, tgt_time_fmt))
upper_b = next(window)
d_meta = {}


#validating IP
def is_IP(host):
    try:
        IP(host)
        return True
    except ValueError:
        return False

def transform_URL(url):
    url = re.sub("HTTP.*$", '', url) #replacing the suffix HTTP.*
    return url

def transform_server_ts(server_ts):
    server_ts = datetime.strptime(server_ts, src_time_fmt)
    server_ts = server_ts.strftime(tgt_time_fmt)
    return server_ts


def get_domain_ext(name):
    obj = tldextract.extract(name)
    return obj.suffix

LOCA_COL_FAMILY = 'loca_info'
def transform_loca_info(loca_info):
    result = {}
    for k,v in loca_info.items():
        if v is not None:
            new_key = LOCA_COL_FAMILY + ':' + k
            result[new_key] = str(v)
    return result

geo_ip = GeoIPUtil()
BATCH_LIMIT = 100
count = 1
batch_index = 1
fail_batch_count = 0
#Extract
with open(log_file_path, "r", encoding = 'ISO-8859-1') as file:
    start = time.time()
    batch = {} #empty batch

    for line in file:
        #timer
        stage0 = time.time()

        match = pattern.match(line)
        if match is None:
            continue

        try:
            log_info = {}
            #Transform
            for i in range(len(LOG_COLS)):
                log_info[LOG_COLS[i]] = match.group(i+1)
        
            #BYTES
            if log_info["log_info:bytes"] == '-':
                log_info["log_info:bytes"] = '0' 


            #URL
            url = transform_URL(log_info['log_info:url'])
            log_info['log_info:url'] = url
       
            #TS
            server_ts = transform_server_ts(log_info['log_info:server_ts'])
            log_info['log_info:server_ts'] = server_ts

            stage1 = time.time()
            
            #add HOST and LOCATION info
            host = log_info['log_info:host']
            if is_IP(host):
                log_info['log_info:is_ip'] = '1'
                loca_info = geo_ip.get_loc_by_ip(host)
            else:
                ext = get_domain_ext(host)
                log_info['log_info:domain_ext'] = ext
                loca_info = geo_ip.get_country_by_domain(host)
        
            #print(loca_info)    
            #print(log_info)
        
            result = log_info.copy()
            if loca_info is not None:
                loca_info = transform_loca_info(loca_info)
                result.update(loca_info)

            stage2 = time.time()
            #print(result) 
            #print('\n')        
            #Load
            ROW_ID = str(time.time())#str(uuid.uuid1()) #TODO change this
            batch[ROW_ID] = result #add entry to batch

            #batch size check
            if len(batch) == BATCH_LIMIT:
                try:
                    print('Batch Index:', batch_index)
                    hbase_client.insert_batch(TABLE, batch)
                except Exception as e:
                    print (e)
                    fail_batch_count += 1
                batch.clear()
                batch_index += 1
                
            stage3 = time.time()
            #print("{},{},{}".format(stage1 - stage0, stage2 - stage1, stage3 - stage2))
        
            ########################
            #METADATA operations
            ########################
            curr_ts = time.mktime(time.strptime(server_ts, tgt_time_fmt))
            #print(str(curr_ts), str(lower_b), str(upper_b))
            if lower_b <= curr_ts < upper_b:
                meta.inc_count() #increment count of requests

            #crosssing the boundry
            elif curr_ts > upper_b:
                #TODO make sure all the empty bounds are inserted with 0s

                d_meta['count:count'] = str(meta.count)
                cal = datetime.utcfromtimestamp(lower_b)
                d_meta['calendar:day'] = str(cal.day)
                d_meta['calendar:month'] = str(cal.month)
                d_meta['calendar:hour'] = str(cal.hour)
                d_meta['calendar:dayofweek'] = str(cal.weekday())
                d_meta['calendar:date'] = str(cal)
                print(str(meta.count), " for ", str(cal))
                meta.add_row(str(upper_b), d_meta)

                #update these accordingly
                meta.reset_count()
                meta.inc_count()
                lower_b = upper_b
                upper_b = next(window)

            if count == 10000:
                break
            count += 1
        except Exception as e:
            print ('Exception while processing log: ', line)
            print (e)

    #final batch
    if len(batch) > 0:
        try:
            hbase_client.insert_batch(TABLE, batch)
        except Exception as e:
            print (e)
            fail_batch_count += 1

    end = time.time()
    print('Total Time(sec):', end - start)
    print('Total entries processed:', count)
    print('Total batches failed:', fail_batch_count)
