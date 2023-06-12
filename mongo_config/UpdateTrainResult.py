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


# py UpdateTrainResult.py --modelName testmodel

parser = argparse.ArgumentParser()

parser.add_argument("--modelName", help="Add model name")


args = parser.parse_args()

client = pymongo.MongoClient(
    "mongodb+srv://haicauancarem:tiachop1@cluster0.dd88nyj.mongodb.net/?retryWrites=true&w=majority",
    connectTimeoutMS=300000,
    serverSelectionTimeoutMS=300000
)
mydb = client["MLOpsData"]
mycol = mydb["training"]

modelName = args.modelName

result = mycol.find_one({})
temp = result["modelNameList"]
temp = list(filter(lambda element: element != modelName, temp))
mycol.find_one_and_update({}, {'$set': {"modelNameList": temp}})


