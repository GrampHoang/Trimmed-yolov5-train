import pymongo
# import base64
# import bson
import sys
# import os
from bson.binary import Binary
from datetime import datetime
import argparse

# py insertFile.py --weightFilePath yolov5n.pt --modelName testmodel --img 640 --batch 20 --epochs 6
# 3 cái path có thể là document/.../yolov5n.pt đc nha

parser = argparse.ArgumentParser()

parser.add_argument("--weightFilePath",
                    help="Add the path of your weight file. Eg: ./path_to_file/file_name")  # yolov5.pt
parser.add_argument("--modelName", help="Add model name")
parser.add_argument("--img", help="Add image size")
parser.add_argument("--batch", help="Add batch")
parser.add_argument("--epochs", help="Add epoch")
parser.add_argument("--version", help="Add version")

args = parser.parse_args()


client = pymongo.MongoClient(
    "mongodb+srv://haicauancarem:tiachop1@cluster0.dd88nyj.mongodb.net/?retryWrites=true&w=majority")
mydb = client["MLOpsData"]
mycol = mydb["weight"]
myid = mydb["seqs"]

id = myid.find_one()["id"]

now = datetime.now()
binDate = now.year*10000000000 + now.month * 100000000 + \
    now.day * 1000000 + now.hour*10000 + now.minute*100 + now.second
current_time = now.strftime("%d/%m/%Y-%H:%M:%S")

weightFilePath = args.weightFilePath
img = args.img
batch = args.batch
epochs = args.epochs
modelName = args.modelName
version = args.version

with open(weightFilePath, "rb") as f:
    encodedWeightFile = Binary(f.read())

y = mycol.find({"modelName": modelName}, {
               "modelName": 1, "version": 1}).sort("version", 1)

x = mycol.insert_one({"id": id, "weightFilePath": weightFilePath, "weightFileName": weightFilePath.split(
    "/")[-1], "weightFile": encodedWeightFile,
    "date": current_time, "binDate": binDate, "img": img, "batch": batch, "epochs": epochs, "modelName": modelName,
    "version": version})

myid.find_one_and_update({}, {'$set': {"id": id + 1}})
