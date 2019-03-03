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


## Visualizing the stack: 

![Data ingestion outline](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/architecture_diag.png)


## Data pipeline

![Data ingestion pipeline](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/flow.png)


### Data pre-processing

Even though publicly available, the log-entries were messy! Several of the entries had IP address errors, non-UTF characters, and uneven structuring of the URL. The data was pre-processed using a python script entry-by-entry and the script emitted the cleaned log entry. Though the current scheme emits one entry, the architecture can be extended to support multiple emits and multiple sources.


### Data ingestion

The Ingestion Engine comprises of a python batch job and a Geo-IP Database. The batch job reads the server log files, extracts the log entries, transforms them and load them into HBase cluster. Each log entry is parsed based on a regular expression and the required fields such as `Host`, `Server Timestamp`, `URL`, `Request Type`, `Response Code` & `Bytes Transferred` are extracted. Using the Host IP/Domain the location information such as `Country`, `City`, `Region`, `Latitude` & `Longitude` are fetched from the Geo-IP Database. A record is created with both the log information and location information and is inserted into the HBase table in batches. During the ingestion process, an additional metadata is built to keep track of the total successful/failed requests and unique Hosts within each time window. The metadata is inserted into another HBase table as a time series data.

### Data Storage

#### About cluster:

We set up a three node EC2 cluster on AWS. Wanting to get our hands dirty, we decided to do the setup from scratch. One out of the three nodes was master, and the other two being slave nodes. Another node acted as an ingestion node, and one more for visualization. Cumulatively, there were 5 nodes.

Here is a brief description of the specifications of every node:

##### Cluster specifications:
| Spec | Details                                 |
|---------------|--------------------------------------------------|
| Nodes | 3x AWS EC2 t3.xlarge instances                                 |
| Hardware | 4 vCPUs, 16 GB Memory, 32 GB SSD                                 |
| Platform OS | Ubuntu 18.04                                 |
| Java | 1.8                                 |
| Hadoop | Hadoop 2.7.7, Replication factor: 2, One master, two slaves                                 |
| HBase | HBase 1.4.8, One master, two region servers, Quorum - 3 nodes                                 |
| Phoenix | Phoenix 1.14.0                                |


##### Ingestion instance:
| Spec | Details                                 |
|---------------|--------------------------------------------------|
| Node | 1x AWS EC2 t3.xlarge instances                                 |
| Hardware | 4 vCPUs, 16 GB Memory, 32 GB SSD                                 |
| Platform OS | Ubuntu 18.04                                 |
| python | python 3.6, happybase (HBase Client), pygeoip (Query from Geo ip Database)                              |
| GeoIP | [Link](http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz)                                 |




##### Visualization and Analysis instance:
| Spec | Details                                 |
|---------------|--------------------------------------------------|
| Node | 1x AWS EC2 t3.xlarge instances                                 |
| Hardware | 4 vCPUs, 16 GB Memory, 32 GB SSD                                 |
| Platform OS | Ubuntu 18.04                                 |
| python | python 3.6, phoenixdb (Apache Phoenix client),Keras                                 |
| Zepellin | Zepellin 0.8.0                                 |


#### HBase tables and schemas

We are using the following HBase tables:

1. `server_logs`

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


2. `sl_metadata`

Metadata table stores the metrics of the parsed server logs within a window. We have set the window time to be 5 minutes. In essence, every 5 minutes, a new row will be inserted in the table with the scores pertaining to that window.


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


## Data Querying and Visualizations:

We analyzed the traffic trends over the two months. This was analyzed at three levels of granularity: Day, Week and Month.

#### Traffic trends over a month:
![Traffic trend analysis over a month](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph1.png)

***

#### Traffic trend analysis over weeks:
![Traffic trend analysis over weeks](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph2.png)

***

Using the I.P addresses from our server logs along with the external dataset of geographical regions of each I.P address we found out the countries that have the highest number of requests.

#### Traffic trend analysis by geographic regions
![Traffic trend analysis by geographic regions](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph3.png)


***

Some request logs contain a domain extension in place of the I.P address.. We would like to see which domain extensions show the highest traffic

#### Top 10 popular domain extensions
![Top 10 popular domain extensions](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph4.png)


***

Each server log contains the request type – GET or POST and we want to find out how many of each kind have been accessed from our server.

#### Distribution of response types
![Distribution of response types](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph5.png)


***
#### Variation in traffic over two days
![Variation in traffic over two days](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph6.png)


***
#### Number of denied requests by day over two months
![Number of denied requests by day over two months](https://github.com/saurabhmj/server-log-analysis/blob/master/Visualizations/graph7.png)


## Challenges and learnings:

* It was challenging to set up the entire NoSQL system on AWS Cloud. Multiple issues were faced while setting up configurations particularly: 
a. Changing parameters in the XML files for configuring Apache HBase.
b. Setting up Zookeeper Quorum (This is the set of nodes which run Zookeeper)
c. Opening ports on the AWS so that the EC2 instances can communicate with each other was an issue.

* Initially, we had worked towards using Apache Drill for querying data with HBase. Subsequently, was dropped out of our system due to multiple issues faced while trying to install due to version dependencies especially for Guava. It also did not allow multiple users to connect to HBase concurrently.

* **Be careful while using Apache Phoenix** Switching over to Apache Phoenix to query the data in HBase, we initially faced an issue with Phoenix tables. We initially ingested data through the Phoenix API and created a Phoenix table. However, this meant we lost control over how the internal HBase table is structured as Phoenix takes control over this. In order to be able to use a structure that was well suited to solve business questions we decided to ingest the data in HBase using the HBase API and then create a Phoenix View to query our data.

* Another minor challenge with Phoenix was getting acquainted with the nuances of Phoenix SQLline. **Phoenix automatically type-casts all the commands to uppercase and thus anything that is in lower-case had to be written in double-quotes.** The team members spent at least an hour trying to figure out why their queries did not work when everything *looked* right. Surprisingly, none of the documentation on the Apache Phoenix website addresses this problem. 

* Another issue with Phoenix is **the way data types are structured.** Phoenix has a very specific type-serialization approach that it uses to store various data types. One way that we worked around this is by declaring all columns as `VARCHAR` type in Phoenix and then used the SQL-like functions to convert data types in Phoenix such as `TO_NUMBER` or `TO_TIMESTAMP`.

* In order to be able to use **Tableau to visualize the results of our queries** we intended to use Apache Spark to connect Phoenix to Tableau. However, initially we face issues with user permissions while installing Spark. Once this was fixed we faced an issue wherein we were unable to view the user created tables in Spark and only Phoenix system created table slike the system metadata table were visible through Spark. As were short on time, we then abandoned this approach and moved onto using Apache Zeppelin.


## Conclusion

1. Installing Hadoop has a sharp learning curve. After overcoming this factor however, installing any other software over Hadoop becomes easier. 

2. As proved by many other peer projects, big data technologies are buggy and it is unfair to conclude a technology’s usability only by accessing its performance through a demo in an ideal environment.

3. Open source systems are a great and terrible option at the same time. One of the most frustrating parts as a developer is to see an issue you are facing listed as an unresolved bug on Jira of a technology. We were the first-hand witnesses to this thanks to Apache Drill.

4. Technology integration in Hadoop stack can only be verified by doing, implementing and generating test-cases. We were able to get Spark SQL and Phoenix set-up. But, it was not possible to connect both of these technologies together since Spark SQL is unable to read Phoenix Views at this moment.

5. Phoenix provides a very efficient layer to query HBase tables. We can confidently conclude that Phoenix, although not “the perfect” existing querying solution available, does overcome HBase’s lacuna of not having an SQL-like query engine better than many other tools like Drill and Hive.
