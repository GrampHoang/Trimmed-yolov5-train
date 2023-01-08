from roboflow import Roboflow
from config import *

rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project(DATA_FOLDER)
dataset = project.version(5).download(DATASET)

