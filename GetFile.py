import pymongo
import sys
import os
from bson.binary import Binary
from datetime import datetime
import shutil

client = pymongo.MongoClient(
    "mongodb+srv://haicauancarem:tiachop1@cluster0.dd88nyj.mongodb.net/?retryWrites=true&w=majority")
mydb = client["MLOpsData"]
mycol = mydb["weight"]


outputFolderPath = sys.argv[1]
if os.path.exists(outputFolderPath) and os.path.isdir(outputFolderPath):
    shutil.rmtree(outputFolderPath)
for x in mycol.find():
  filename = x["fileName"]
  os.makedirs(os.path.dirname(outputFolderPath + "/" + str(x["binDate"]) +"/" + filename), exist_ok=True)
  with open(outputFolderPath + "/" + str(x["binDate"]) +"/" + filename, "wb") as f:
    f.write(x["file"])