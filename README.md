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
