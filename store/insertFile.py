import pymongo
# import base64
# import bson
import sys
# import os
from bson.binary import Binary
from datetime import datetime

client = pymongo.MongoClient(
    "mongodb+srv://haicauancarem:tiachop1@cluster0.dd88nyj.mongodb.net/?retryWrites=true&w=majority")
mydb = client["MLOpsData"]
mycol = mydb["weight"]

now = datetime.now()
binDate = now.year*10000000000 + now.month * 100000000 + now.day * 1000000 + now.hour*10000 + now.minute*100 + now.second
current_time = now.strftime("%d/%m/%Y-%H:%M:%S")

filePath = sys.argv[1]
with open(filePath, "rb") as f:
  encoded = Binary(f.read())  
x = mycol.insert_one({"filePath": filePath , "fileName": filePath.split("/")[-1], "file": encoded, "date": current_time, "binDate": binDate})

