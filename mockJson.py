import json
import requests

#change ip to match yours
url = "http://172.21.224.39:5050"

#json dict
data = {
   "sensor_array":[
      {
         "id":1,
         "type":"humidity",
         "val":6969
      },
      {
         "id":2,
         "type":"temp",
         "val":21.8597
      },
      {
         "id":3,
         "type":"red",
         "val":2315
      },
      {
         "id":4,
         "type":"green",
         "val":2273
      },
      {
         "id":5,
         "type":"blue",
         "val":1991
      },
      {
         "id":6,
         "type":"c",
         "val":4890
      },
      {
         "id":7,
         "type":"colorTemp",
         "val":4361
      },
      {
         "id":8,
         "type":"Lux",
         "val":1378
      }
   ],
   "station":{
      "status":"status_ok",
      "MAC":"BC:FF:4D:49:BD:DC"
   }
}

#json headers
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

#send request
r = requests.post(url, data=json.dumps(data), headers=headers)

#print status code (should be 200)
print(r.status_code)