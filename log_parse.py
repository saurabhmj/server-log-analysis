from IPy import IP
import re
import hbase_client
from metadata import metadata
import uuid
import time
import tldextract
from datetime import datetime
from location.geo_ip import GeoIPUtil

log_file_path = '/home/ubuntu/datasets/nasa_log_aug'
regex = "(.*) - - \[(.*)\] \"([A-Z]+) (.*)\" ([0-9]{3}) (-|[0-9]+)"
pattern = re.compile(regex)

FAMILIES = ['log_info','loca_info']
TABLE = 'server_logs_test'
LOG_COLS =  ["log_info:host", "log_info:server_ts", "log_info:type", "log_info:url", "log_info:status", "log_info:bytes"]

#hbase_client.truncate_table(TABLE, FAMILIES)


###########################
#Metadata setup
###########################
tgt_time_fmt = "%Y-%m-%d %H:%M:%S"
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

src_time_fmt = "%d/%b/%Y:%H:%M:%S %z"
tgt_time_fmt = "%Y-%m-%d %H:%M:%S"
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
count = 1
fail_count = 0
#Extract
st = time.time()
with open(log_file_path, "r", encoding = 'ISO-8859-1') as file:
    for line in file:
        match = pattern.match(line)
        if match is None:
            continue
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

        #add HOST and LOCATION info
        host = log_info['log_info:host']
        if is_IP(host):
            log_info['log_info:is_ip'] = '1'
            loca_info = geo_ip.get_loc_by_ip(host)
        else:
            ext = get_domain_ext(host)
            log_info['log_info:domain_ext'] = ext
            #print(geo_ip.get_country(ext))
            loca_info = geo_ip.get_loc_by_name(host)
        
        #print(loca_info)    
        #print(log_info)
        
        result = log_info.copy()
        if loca_info is not None:
            if loca_info['country'] is None:
                loca_info['country']=geo_ip.get_country(ext) 
            loca_info = transform_loca_info(loca_info)
            result.update(loca_info)

        #print(result) 
        #print('\n')        
        #Load
        ROW_ID = str(time.time())#str(uuid.uuid1()) #TODO change this

        ########################
        #METADATA operations
        ########################
        curr_ts = time.mktime(time.strptime(server_ts, tgt_time_fmt))
        #print(str(curr_ts), str(lower_b), str(upper_b))
        if lower_b <= curr_ts < upper_b:
           meta.inc_count() #increment count of requests

        elif curr_ts > upper_b:
            d_meta['count:count'] = str(meta.count)
            cal = datetime.utcfromtimestamp(lower_b)
            d_meta['calendar:day'] = str(cal.day)
            d_meta['calendar:month'] = str(cal.month)
            d_meta['calendar:hour'] = str(cal.hour)
            d_meta['calendar:dayofweek'] = str(cal.weekday())
            d_meta['calendar:date'] = str(cal)
            print(str(meta.count), " for ", str(cal))

            meta.reset_count()

            meta.add_row(str(upper_b), d_meta)

            lower_b = upper_b
            upper_b = next(window)



        try:
            hbase_client.insert_row(TABLE, ROW_ID, result)
        except:
            fail_count += 1
        if count == 10000:
            break
        if count%5000 == 0:
            print(count, " rows inserted")
        count += 1
    print('Total entries processed:', count)
    print('Total insertions failed:', fail_count)

    print(str((time.time() - st)/60))
