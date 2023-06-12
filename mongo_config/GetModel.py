import json
import pymongo
import sys
import os
from bson.binary import Binary
from datetime import datetime
import shutil
import argparse
import gridfs

parser = argparse.ArgumentParser()


# python GetModel.py --modelName testmodel
# Kết quả lưu trong file versionList.json, ngay trong folder này luôn


parser.add_argument("--modelName", help="Add model name you want to get")
parser.add_argument("--version", help="Add version")

args = parser.parse_args()

client = pymongo.MongoClient(
    "mongodb+srv://haicauancarem:tiachop1@cluster0.dd88nyj.mongodb.net/?retryWrites=true&w=majority",
    connectTimeoutMS=300000,
    serverSelectionTimeoutMS=300000
)
mydb = client["MLOpsData"]
mycol = mydb["weight"]
# fs = gridfs.GridFS(mydb)

# outputFolderPath = args.outputFolderPath

# if os.path.exists(outputFolderPath) and os.path.isdir(outputFolderPath):
#     shutil.rmtree(outputFolderPath)

modelName = args.modelName
# version = args.version

# for x in mycol.find():
#   filename = x["fileName"]
#   os.makedirs(os.path.dirname(outputFolderPath + "/" + str(x["binDate"]) +"/" + filename), exist_ok=True)
#   with open(outputFolderPath + "/" + str(x["binDate"]) +"/" + filename, "wb") as f:
#     f.write(x["file"])

y = mycol.find({'modelName': modelName}).sort("id", -1)

versionArray = []
for element in y:
    versionArray += [element["version"]]


data = {"version_array": versionArray}

# write data to a JSON file
with open("versionList.json", "w") as f:
    json.dump(data, f)

# read data from the JSON file
with open("versionList.json", "r") as f:
    data = json.load(f)


# print(os.environ['VERSION_ARRAY'])
# x = None
# for element in y:
#     x = element
# if x:
#     gridID = x["gridID"]
#     weightFileName = x["weightFileName"]
#     temp = fs.get(gridID).read()
#     os.makedirs(os.path.dirname(outputFolderPath +"/" + weightFileName), exist_ok=True)
#     with open(outputFolderPath +"/" + weightFileName, "wb") as f:
#         f.write(temp)
# else:
#     raise Exception("Sorry, there is no model with that name")
