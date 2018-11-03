# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:35:06 2018

@author: prabl
"""

import phoenixdb
import phoenixdb.cursor
import pandas as pd

database_url = 'http://18.188.70.4:8765/'
conn = phoenixdb.connect(database_url, autocommit=True)

cursor = conn.cursor()

############################
# ###### Easy Queries ######
############################

cursor.execute("select count(*) from \"server_logs_test\"")
Total_rows = int(cursor.fetchone()[0])

## QUERY 1 ##
cursor.execute("select \"type\", count(*) as counts from \"server_logs_test\" group by \"type\"")
Type_counts = pd.DataFrame(cursor.fetchall())
Type_counts.columns = ["Type", "Counts"]

# computing percentage of GET,POST and HEAD requests
Type_counts['Percent'] = Type_counts.Counts/Total_rows * 100

# Printing to console
print("Query 1: Get Percentage of GET, POST and HEAD requests")
print(Type_counts)

## QUERY 2 ##
cursor.execute("select count(*) as counts from \"server_logs_test\" where \"status\" like '4__'")
Failed_counts = pd.DataFrame(cursor.fetchall())
Failed_counts.columns = ["Counts"]

# computing percentage of failed requests
Failed_counts['Failed_Percent'] = Failed_counts.Counts/Total_rows * 100

cursor.execute("select count(*) as counts from \"server_logs_test\" where \"status\" like '2__'")
Success_counts = pd.DataFrame(cursor.fetchall())
Success_counts.columns = ["Counts"]

# computing percentage of failed requests
Success_counts['Success_Percent'] = Success_counts.Counts/Total_rows * 100

# Printing to console
print(" ")
print("Query 2: Get Percentage of successfull and failed requests")
print(Failed_counts)
print(Success_counts)

## QUERY 3 ##
cursor.execute("select avg(to_number(\"bytes\")) as average_bytes_per_request from \"server_logs_test\"")
Average_Bytes = float(cursor.fetchone()[0])
# Printing to console
print(" ")
print("Query 3: Get average number of bytes sent")
print(Average_Bytes)

## Query 4 ##
cursor.execute("select \"domain_ext\", count(*) as requests_per_domain from \"server_logs_test\" \
group by \"domain_ext\" order by requests_per_domain desc")
Requests_per_domain = pd.DataFrame(cursor.fetchall())
Requests_per_domain.columns = ["Domain_Extension", "Counts"]

# Printing to console
print(" ")
print("Query 4: Get percentage of requests per domain extension")
print(Requests_per_domain.head(10))

#  # QUERY 5 ##
cursor.execute("select count(*) as requests_on_4th_july from \"server_logs_test\" where (\"server_ts\" like '1995-07-04%')")
July_4th = int(cursor.fetchone()[0])
# Printing to console
print(" ")
print("Query 5: Get Number of requests on 4th of July 1995")
print(July_4th)

##############################
####### Medium Queries #######
##############################

## QUERY 6 ##
cursor.execute(" select \"country\", count(*) as requests_per_region from \"server_logs_test\" \
group by \"country\" order by requests_per_region desc")
Requests_per_region = pd.DataFrame(cursor.fetchall())
Requests_per_region.columns = ["Domain_Extension", "Counts"]

# Printing to console
print(" ")
print("Query 6: Percentage of traffic based on geographic regions")
print(Requests_per_region.head(10))

## QUERY 7 ##
cursor.execute("select \"url\", avg(count_per_day) as avg_per_day \
from (select DAYOFYEAR(TO_TIME(\"server_ts\")) as day_of_year,\"url\", count(\"url\") as count_per_day \
from \"server_logs_test\" group by DAYOFYEAR(TO_TIME(\"server_ts\")) , \"url\") group by \"url\" \
order by avg_per_day desc")
Average_per_URL_per_day = pd.DataFrame(cursor.fetchall())
Average_per_URL_per_day.columns = ["URL","Average_Per_Day_Per_URL"]

# Printing to console
print(" ")
print("Query 7: Number of requests per page per day")
print(Requests_per_region.head(25))


## QUERY 8 ##
cursor.execute("select count(*) as number_of_image_requests from \"server_logs_test\" where \
(\"url\" like '%.gif')")
Number_of_image_requests = int(cursor.fetchone()[0])

#Printing to console
print(" ")
print("Query 8: Number of requests per page per day")
print(Number_of_image_requests)

###################################
####### Challenging Queries #######
###################################

## QUERY 9 ##
cursor.execute("select \"month\", \"day\", sum(TO_NUMBER(\"count\")) as requests \
from \"sl_metadata\" group by \"month\",\"day\" order by \"month\",requests desc")
Traffic_Over_Days_of_Month = pd.DataFrame(cursor.fetchall())
Traffic_Over_Days_of_Month.columns = ["Month", "Day", "Total_Requests"]

# Printing to console
print(" ")
print("Query 9: When is the peak traffic time? Over a Month")
print(Traffic_Over_Days_of_Month.head(25))


cursor.execute("select WEEK(TO_TIME(\"date\")) as week, sum(TO_NUMBER(\"count\")) as requests \
from \"sl_metadata\" group by week,\"dayofweek\" order by requests desc")
Traffic_Over_Weeks = pd.DataFrame(cursor.fetchall())
Traffic_Over_Weeks.columns = ["Week_of_Year", "Total_Requests"]

# Printing to console
print(" ")
print("Query 9: When is the peak traffic time? Over a Week")
print(Traffic_Over_Weeks.head(25))

cursor.execute("select \"month\", \"day\", \"hour\", sum(TO_NUMBER(\"count\")) as requests \
from \"sl_metadata\" group by \"month\",\"day\",\"hour\" order by \"month\",\"day\",requests desc")
Traffic_Over_Day = pd.DataFrame(cursor.fetchall())
Traffic_Over_Day.columns = ["Month","Day","Hour","Total_Requests"]

# Printing to console
print(" ")
print("Query 9: When is the peak traffic time? Over a Week")
print(Traffic_Over_Day.head(25))

### QUERY 10 ##
cursor.execute("select \"date\" from \"sl_metadata\" where \"denied\" >= '9' and \"hosts\" < '20'")
High_failure_timeranges = pd.DataFrame(cursor.fetchall())
High_failure_timeranges.columns = ["Server_Timestamp"]

print(High_failure_timeranges.head(5))

for ts in High_failure_timeranges.Server_Timestamp:
    # print(str(ts))
    cursor.execute("select \"host\" from \"server_logs_test\" where \
    TO_TIMESTAMP(\"server_ts\") >= TO_TIMESTAMP('{}') and \
    TO_TIMESTAMP(\"server_ts\") <= TO_TIMESTAMP('{}') + (0.00347222222)".format(str(ts),str(ts)))
    Failure_hosts = pd.DataFrame(cursor.fetchall()) 
    Failure_hosts.columns = ["Host"]
    
    # Printing to console
    print(" ")
    print("Query 10: Suspicious Host Names in 5 minutes from ", str(ts))
    print(len(Failure_hosts.Host.unique()))
    
    

