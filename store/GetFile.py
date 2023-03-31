import pymongo
import sys
import os
from bson.binary import Binary
from datetime import datetime
import shutil
import argparse

parser = argparse.ArgumentParser()

# python GetFile.py --outputFolderPath output --modelName testmodel --version 2.1
# outputFolderPath là cái path để tạo cái folder, sau đó nó sẽ để 3 cái file với model name tương ứng vào
parser.add_argument("--outputFolderPath", help="Add path you want to create folder to put weight file in")
parser.add_argument("--modelName", help="Add model name you want to get")
parser.add_argument("--version", help="Add version")

args = parser.parse_args()

client = pymongo.MongoClient(
    "mongodb+srv://haicauancarem:tiachop1@cluster0.dd88nyj.mongodb.net/?retryWrites=true&w=majority")
mydb = client["MLOpsData"]
mycol = mydb["weight"]

outputFolderPath = args.outputFolderPath

if os.path.exists(outputFolderPath) and os.path.isdir(outputFolderPath):
    shutil.rmtree(outputFolderPath)

modelName = args.modelName
version = args.version

# for x in mycol.find():
#   filename = x["fileName"]
#   os.makedirs(os.path.dirname(outputFolderPath + "/" + str(x["binDate"]) +"/" + filename), exist_ok=True)
#   with open(outputFolderPath + "/" + str(x["binDate"]) +"/" + filename, "wb") as f:
#     f.write(x["file"])

y = mycol.find({'modelName': modelName, 'version': version}).sort("version", 1)
x = None
for element in y:
    x = element
if x:
    weightFileName = x["weightFileName"]
    os.makedirs(os.path.dirname(outputFolderPath +"/" + weightFileName), exist_ok=True)
    with open(outputFolderPath +"/" + weightFileName, "wb") as f:
        f.write(x["weightFile"])
else:
    raise Exception("Sorry, there is no model with that name")