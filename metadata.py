import hbase_client
from datetime import datetime
import time


#####
# Class for metadata operations
#####

class metadata():

    #####
    # Constructor with options to truncate or create metadata table
    #####

    def __init__(self, table='sl_metadata', families=['metainfo','calendar'], create=False, truncate=False):
        self.table = table
        self.families = families
        self.count = 0
        self.denied = 0
        self.hosts = set()
        self.start_time = 0
        self.interval = 0

        if create:
            self.create_table()
        if truncate:
            self.truncate_table()

    #####
    # Initialize timer with start time and window interval
    #####

    def initialize_timer(self, start_time="1995-07-01 00:00:00", interval=5):
        ts = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
        self.start_time = int(ts)
        self.interval = interval

    #####
    # Get the next window time using generators
    #####

    def next_bound(self):
        start = self.start_time
        while True:
            start = start + 60*self.interval 
            yield start

    #####
    # Housekeeping - getters and setters
    #####

    def reset_count(self):
        self.count = 0

    def inc_count(self):
        self.count += 1

    def inc_denied(self):
        self.denied +=1

    def reset_denied(self):
        self.denied = 0

    def add_host(self, host):
        self.hosts.add(host)

    def get_num_hosts(self):
        return len(self.hosts)

    def reset_hosts(self):
        self.hosts.clear()        

    def truncate_table(self):
        hbase_client.truncate_table(self.table, self.families)
    
    def create_table(self):
        hbase_client.create_table(self.table, self.families)

    #####
    # Add row to the metadata table
    #####

    def add_row(self, row_key, column_info):
        hbase_client.insert_row(self.table, row_key, column_info)


#####
# Main method to test functionality
#####

if __name__ == '__main__':
    md = metadata()
    md.initialize_timer()
    itr = md.next_bound()
    
    print(next(itr))
    print(next(itr))
    print(next(itr))
    print(next(itr))

    #n=0
    #for i in md.next_bound():
        #n = md.next_bound()
        #print(str(datetime.utcfromtimestamp(i)))
        #n+=1
        #if n==10:
            #break

    
