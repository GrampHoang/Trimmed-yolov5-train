# from config import *

# rf = Roboflow(api_key=API_KEY)
# project = rf.workspace(WORKSPACE).project(DATA_FOLDER)
# dataset = project.version(VERSION).download(DATASET)

from roboflow import Roboflow
rf = Roboflow(api_key="Zk1BC6WNlwGe7i2evhTG")
project = rf.workspace("personal-d8mlf").project("mlops_member")
dataset = project.version(2).download("yolov5")

