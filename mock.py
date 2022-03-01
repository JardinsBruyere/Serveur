import time,sqlite3,json,requests
import datetime
import random
from random_word import RandomWords
import numpy as np


numdays=24*3
NbrCapteur=3
NbrTypes=2
NbrStation=2

r = RandomWords()

conn = sqlite3.connect('capteur.db') 
c =  conn.cursor()
base = datetime.datetime.today()
date_list = np.arange(datetime.datetime(2022,1,1,0,0), datetime.datetime(2023,12,12,23,0), datetime.timedelta(hours=1)).astype(datetime.datetime)   
c.execute("delete from SensorReading;")
c.execute("delete from Sensor;")
c.execute("delete from Station;")
c.execute("delete from SensorTypes;")
c.execute("delete from sqlite_sequence;");
conn.commit()

for i in range(0,NbrTypes):
    c.execute("insert into SensorTypes (Unit) values (\"NbrTypes_%s\");"%(r.get_random_word()))

for i in range(0,NbrStation):
    c.execute("insert into Station (Name) values (\"Station_%s\");"%(r.get_random_word()))
    
for i in range(0,NbrCapteur):
    mac="BC:FF:4D:4"+str(i)+":BD:DC"
    query="insert into Sensor (Type,DateAdded,Station,Name,MacAdress) values (%s,\"%s\",%s,\"Sensor_%s\",\"%s\");"%(random.randint(1,NbrTypes),str(date_list[i]),random.randint(1,NbrStation),r.get_random_word(),str(mac))
    print(query)
    c.execute(query)

z=0
for capteur in range(0,9):
    z=random.randint(-10,10)
    for i in range(0,numdays):
        c.execute("INSERT INTO SensorReading (SensorId,DateAdded,Value) VALUES (%s, \"%s\",\"%s\");" %(str(capteur+1),str(date_list[i]),str(z)))
        if(random.randint(0,1)==1):
            z+=random.randint(0,10)
        else:
            z-=random.randint(0,10)
            

conn.commit() 


print("Table SensorTypes:")
c.execute("select * from SensorTypes;")
res=c.fetchall()
print(*res, sep = "\n")

print("\nTable Station:")
c.execute("select * from Station;")
res=c.fetchall()
print(*res, sep = "\n")

print("\nTable Sensor:")
c.execute("select * from Sensor;")
res=c.fetchall()
print(*res, sep = "\n")


print("\nTable SensorReading:")
c.execute("select * from SensorReading;")
res=c.fetchall()
print(*res, sep = "\n")


