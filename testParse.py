from IPy import IP
import pandas as pd
import re
import time
from datetime import datetime

def isIP(string):
    try:
        IP(string)
        return "TRUE"
    except ValueError:
        return "FALSE"


s= "(.*) - - \[(.*)\] \"([A-Z]+) (.*) HTTP/1.0\" ([0-9]{3}) ([0-9]+)"
pattern = re.compile(s)

with open("F:\\Study\\MS\\Big_Data_And_Analytics\\NoSQL_POC\\NASA_access_log_Jul95\\access_log_Jul95","r") as f:

    print("Parsing")
    matches = pattern.findall(f.read())


df = pd.DataFrame(data=matches,columns=["domain","serverTime","type","url","status","bytes_trx"])
df["isIP"] = df.domain.map(lambda x: isIP(x))
print("IP")
time_pattern = "%d/%b/%Y:%H:%M:%S %z"
df["UTCTime"] = df.serverTime.map(lambda x: int(time.mktime(time.strptime(x,time_pattern))))
print("UTC")
df.serverTime = df.UTCTime.map(lambda x: str(datetime.utcfromtimestamp(x)))
Ids = []
idx=0
for timeInstance in df.UTCTime:
    Ids.append(str(timeInstance)+"_"+ str(idx))
    idx += 1
    #time.sleep(1e-12)
print("ID")
df["ID"] = Ids
df["url_ext"] = df.url.map(lambda x: "None" if "." not in x else x.split(".")[1])

df.columns = [x.upper() for x in ["domain","serverTime","type","url","status","bytes_trx","isIP","UTCTime","ID","url_ext"]]
#print(df)
df.to_csv("F:\\Study\\MS\\Big_Data_And_Analytics\\NoSQL_POC\\NASA_access_log_Jul95\\parsed.csv",index=False, columns=[x.upper() for x in ["ID","domain","serverTime","type","url","status","bytes_trx","isIP","UTCTime","url_ext"]])
print("written")