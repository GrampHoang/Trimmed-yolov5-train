# from config import *
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--API_KEY",help="Add API_KEY")  
parser.add_argument("--WORKSPACE", help="Add WORKSPACE")
parser.add_argument("--DATA_FOLDER", help="Add DATA_FOLDER")
parser.add_argument("--VERSION", help="Add VERSION")
parser.add_argument("--DATASET", help="Add DATASET")

args = parser.parse_args()

APIKEY = args.API_KEY
WORKSPACE = args.WORKSPACE
DATA_FOLDER = args.DATA_FOLDER
VERSION = args.VERSION
DATASET = args.DATASET


from roboflow import Roboflow
rf = Roboflow(api_key=APIKEY)
project = rf.workspace(WORKSPACE).project(DATA_FOLDER)
dataset = project.version(VERSION).download(DATASET)

# from roboflow import Roboflow
# rf = Roboflow(api_key="Zk1BC6WNlwGe7i2evhTG")
# project = rf.workspace("personal-d8mlf").project("mlops_member")
# dataset = project.version(2).download("yolov5")

