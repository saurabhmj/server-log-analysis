## Summary


The project aims to analyze the trends in traffic on web-server using the server logs. It is essential to analyze the web server logs in order to understand the traffic and usage patterns of users over a period of time or even over geographic regions. Analyzing these logs can assist companies in making key decisions towards improving user experience and Quality of Service.


One other aim of the project is to be able to configure Hadoop system. For this purpose, no pre-built sandox was used and hadoop cluster was created by combining three AWS EC2 instances to work together. This helped us become acquainted with not only the analysis, but engineering part as well.


## Datasets


#### NASA HTTP Datasets
https://ita.ee.lbl.gov/html/traces.html

The data consists of HTTP requests generated over a period of two months (Jul 01 - Aug 31, 1995) to the NASA Kennedy Space Center Web server in Florida. And there are no entries between Aug 01 - Aug 3rd due to server shutdown. ~3.5 Million Entries


#### GeoIP Database

http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz


The data consists of IP addresses to Geographical location mapping.


## Technology stack


### Apache HBase

Apache HBase is a distributed column-oriented database built on top of the Hadoop File system. Apache HBase is modeled after Google's Bigtable: A Distributed Storage System for Structured Data by Chang et al. It is a part of the Hadoop ecosystem that provides random real-time read/write access to data in the Hadoop File System.


### Apache Phoenix

Apache Phoenix is an open source, massively parallel, relational database engine supporting OLTP for Hadoop using Apache HBase as its backing store. It enables developers to access large dataset in real-time with familiar SQL interface. It provides standard SQL and JDBC APIs with full ACID transaction capabilities as well as support for late-bound, schema-on-read with existing data in HBase.

Apache Phoenix compiles SQL query into a series of HBase scans, and orchestrates the running of those scans to produce regular JDBC result sets. Direct use of the HBase API, along with coprocessors and custom filters, results in performance on the order of milliseconds for small queries, or seconds for tens of millions of rows.


## Technology 'stack'(!): 

![Data ingestion outline](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/architecture_diag.png)


### Components and their usability:

* Apache HBase: A distributed column-oriented database built on top of the Hadoop File system. Apache HBase is modeled after Google's Bigtable [paper](https://research.google.com/archive/bigtable-osdi06.pdf)

#### Why HBase?



* Apache Phoenix: Apache Phoenix is an open source, massively parallel, relational database engine supporting OLTP for Hadoop using Apache HBase as its backing store. It enables developers to access large dataset in real-time with familiar SQL interface.




## Data pre-processing

Even though publicly available, the log-entries were messy! Several of the entries had IP address errors, non-UTF characters, and uneven structuring of the URL. The data was pre-processed using a python script entry-by-entry and the script emitted the cleaned log entry. Though the current scheme emits one entry, the architecture can be extended to support multiple emits and multiple sources.


## Data ingestion



## Data Storage

Hive managed tables are employed to store data in ORC, Avro and Parquet data formats. The script to create all the tables is [here](https://github.com/saurabhmj/hive-project/blob/master/create_table.hql)


## Data Querying




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

***

### Visualizations:

#### Traffic trends over a month:
![Traffic trend analysis over a month](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph1.png)

***

#### Traffic trend analysis over weeks:
![Traffic trend analysis over weeks](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph2.png)

***
#### Traffic trend analysis by geographic regions
![Traffic trend analysis by geographic regions](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph3.png)


***
#### Top 10 popular domain extensions
![Top 10 popular domain extensions](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph4.png)


***
#### Distribution of response types
![Distribution of response types](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph5.png)


***
#### Variation in traffic over two days
![Variation in traffic over two days](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph6.png)


***
#### Number of denied requests by day over two months
![Number of denied requests by day over two months](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph7.png)
