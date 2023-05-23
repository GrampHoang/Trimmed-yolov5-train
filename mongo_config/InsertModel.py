import pymongo
# import base64
# import bson
import sys
import os
from bson.binary import Binary
from datetime import datetime
import argparse
import gridfs
import yaml
import json


# py InsertModel.py --resultFilePath opt.yaml --modelName testmodel --img 640 --batch 20 --epochs 6 --version 2.1

parser = argparse.ArgumentParser()

parser.add_argument("--resultFilePath",
                    help="Add path to opt.yaml file")  
parser.add_argument("--modelName", help="Add model name")
parser.add_argument("--img", help="Add image size")
parser.add_argument("--batch", help="Add batch")
parser.add_argument("--epochs", help="Add epoch")

parser.add_argument("--version", help="Add version")

args = parser.parse_args()


client = pymongo.MongoClient(
    "mongodb+srv://haicauancarem:tiachop1@cluster0.dd88nyj.mongodb.net/?retryWrites=true&w=majority", 
    connectTimeoutMS=300000)
mydb = client["MLOpsData"]
mycol = mydb["weight"]
myid = mydb["seqs"]
# fs = gridfs.GridFS(mydb)

id = myid.find_one()["id"]

now = datetime.now()
binDate = now.year*10000000000 + now.month * 100000000 + \
    now.day * 1000000 + now.hour*10000 + now.minute*100 + now.second
current_time = now.strftime("%d/%m/%Y-%H:%M:%S")

resultFilePath = args.resultFilePath
img = args.img
batch = args.batch
epochs = args.epochs


modelName = args.modelName
version = args.version

# gridID = fs.put(open(resultFilePath, 'rb'))
with open(resultFilePath, "r") as f:
    configuration = yaml.safe_load(f)

with open('config.json', 'w') as json_file:
    json.dump(configuration, json_file)


output = json.dumps(json.load(open('config.json')), indent=2)
os.remove("config.json")

# y = mycol.find({"modelName": modelName}, {
#                "modelName": 1, "version": 1}).sort("version", 1)



x = mycol.insert_one({"id": id,
                      "resultFile": output,
                      "date": current_time, "binDate": binDate, "modelName": modelName,
                      "img": img, "batch": batch, "epochs": epochs,
                      "version": version, "deployed": False })

myid.find_one_and_update({}, {'$set': {"id": id + 1}})
