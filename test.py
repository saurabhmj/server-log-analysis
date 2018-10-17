
#cluster end points
import requests
SERVER = "ec2-54-89-149-209.compute-1.amazonaws.com"
PORT = 8080
URL = 'http://{}:{}'.format(SERVER, PORT)

def get_req(path):
  resp = requests.get(URL + path)
  print (resp.content)
  if resp.status_code != 200:
    raise ApiError(resp.status_code)

def post_req(path, data):
  resp = requests.post(URL + path, data)
  print (resp.text)


####cluster####
#status
get_req('/status/cluster')
#version
get_req('/version/cluster')

####namespaces####
#list
get_req('/namespaces')

#cretae a new namespace
#post_req('/namespaces/hive5', {})

#create a table

