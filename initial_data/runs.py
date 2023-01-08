from roboflow import Roboflow
from config import *

rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(DATA_FOLDER)
dataset = project.version(VERSION).download(DATASET)

