API_KEY = "Zk1BC6WNlwGe7i2evhTG"
WORKSPACE = "personal-d8mlf"
DATA_FOLDER = "mlops-demo-project"
DATASET = 'yolov5'
VERSION = "1"


#!python train.py --img 480 --batch 1 --epochs 1 --data /DATA_FOLDER + "-" + VERSION/data.yaml --weights yolov5l.pt

# img: kich co cua hinh, resize hinh de cho dong nhat model, detect.py cung su dung img khi du doan -> tang chinh xac.  Khi train thuong dung 480->640, cang lon thi cang can nhieu RAM, cang chinh xac, toc do cang cham
# batch: train nhieu hinh cung 1 luc, so ko nen lon qua ko nen nho qua. Binh thuong thi de -1 cho auto, demo de 1 de sure keo du RAM
# epochs: so lan train qua toan bo dataset, vd dataset co 5 hinh, 5 epoch = moi buc hinh train 5 lan (di qua het dataset moi bat dau lai tu dau)
# data: file chua path toi folder train data, test data va validation. Va chua so luong classes can detect
# weights: file trong so, su dung yolov5l.pt co san trong repo

#Ngoai ra con nhieu param nua co the tham khao trong train.py
