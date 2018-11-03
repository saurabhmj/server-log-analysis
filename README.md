## Detecting Traffic Trends and Intrusion using Apache HBASE


### HBase tables and schemas

We are using the following HBase tables:

1. server_logs

**row_key**: timestamp when the log was parsed by the system

| Column family | Possible Columns                                 | Description
|---------------|--------------------------------------------------|--------------------------
| log_info      | host   | The IP or domain name of the request |
| log_info      | server_ts                                                 | Timestamp of server in the Date format |
| log_info      | type                                                 | type of request|
| log_info      | url                                                 | url requested|
| log_info      | status                                                 | status code sent in response|
| log_info      | bytes                                                 | number of bytes transferred|
| loca_info      | country                                                 | country where the request originated|


2. sl_metadata

**row_key**: date of latest possible entry in the window in Timestamp format

| Column family | Possible Columns                                 | Description
|---------------|--------------------------------------------------|--------------------------
| metainfo      | count   | Number of requests in the time window |
| metainfo      | denied                                                 | Number of requests with response code as 4xx |
| metainfo      | hosts                                                 | Number of unique IPs/domains that requested in the window|
| calendar      | day                                                 | day of the window|
| calendar      | month                                                 | month of the window|
| calendar      | hour                                                 | hour of the window|
| calendar      | dayofweek                                                 | day of week of the window (Sunday=0)|
| calendar      | date                                                 | date of earliest possible entry in the window in Date format|


### Visualizations:

#### Traffic trends over a month:
![Traffic trend analysis over a month](https://github.umn.edu/jannu007/hive5/blob/master/Visualizations/graph1.png)



#### Traffic trend analysis over weeks:
![Traffic trend analysis over weeks](https://github.umn.edu/jannu007/hive5/blob/master/Visualizations/graph2.png)


#### Traffic trend analysis by geographic regions
![Traffic trend analysis by geographic regions](https://github.umn.edu/jannu007/hive5/blob/master/Visualizations/graph3.png)



#### Top 10 popular domain extensions
![Top 10 popular domain extensions](https://github.umn.edu/jannu007/hive5/blob/master/Visualizations/graph4.png)



#### Distribution of response types
![Distribution of response types](https://github.umn.edu/jannu007/hive5/blob/master/Visualizations/graph5.png)



#### Variation in traffic over two days
![Variation in traffic over two days](https://github.umn.edu/jannu007/hive5/blob/master/Visualizations/graph6.png)



#### Number of denied requests by day over two months
![Number of denied requests by day over two months](https://github.umn.edu/jannu007/hive5/blob/master/Visualizations/graph7.png)
