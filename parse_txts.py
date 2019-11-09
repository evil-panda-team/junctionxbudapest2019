# -*- coding: utf-8 -*-

import numpy as np
import cv2
import json
from glob import glob
from tqdm import tqdm
import math

# In[]: BOSH
cam_preds_train = glob("traindata/det_cam_score/*.txt")
lidar_preds_train = glob("traindata/det_lidar/*.txt")
gt_train = glob("traindata/labels/*.txt")

cam_preds_test = glob("testdata/det_cam_score/*.txt")
lidar_preds_test = glob("testdata/det_lidar/*.txt")

cam_preds_train.sort()
lidar_preds_train.sort()
gt_train.sort()

cam_preds_test.sort()
lidar_preds_test.sort()

# In[]: KITTI
gt_kitti = glob("data_object_label_2/training/label_2/*.txt")

gt_kitti.sort()

# In[]:
f = open(cam_preds_train[213],"r")
lines = f.readlines() 
l = lines[0]
vals = l.split(" ") 
typ = vals[0]
truncated = vals[1]
occluded = vals[2]
alpha = vals[3]
bbox = vals[4:8]
dimensions = vals[8:11]
location = vals[11:14]
rotation_y = vals[14]
score = vals[15]

# In[]:
truncateds = []
occludeds = []
alphas = []
bboxes = []
dimensionses = []
locations = []
rotation_ys = []
scores = []
for cpt in tqdm(gt_kitti):
    f = open(cpt,"r")
    lines = f.readlines()
    for l in lines:
        vals = l.split(" ") 
        vals[-1] = vals[-1][:-1]
        typ = vals[0]
        truncated = float(vals[1])
        occluded = int(vals[2])
        alpha = float(vals[3])
        if not(-math.pi <= alpha <= math.pi):
            print(cpt)
#        assert -math.pi <= alpha <= math.pi
        bbox = vals[4:8]
        dimensions = vals[8:11]
        location = vals[11:14]
        rotation_y = vals[14]
#        score = float(vals[15])
        
        truncateds.append(truncated)
        occludeds.append(occluded)
        alphas.append(alpha)
        bboxes.append(bbox)
        dimensionses.append(dimensions)
        locations.append(location)
        rotation_ys.append(rotation_y)
#        scores.append(score)
        
# In[]:
scores = np.array(occludeds)
print(scores.min())
print(scores.max())
print(scores.mean())
print(scores.std())

# In[]:
th = 50
for gtk in tqdm(gt_kitti):
    f = open(gtk,"r")
    lines = f.readlines()

    for l in lines:
        vals = l.split(" ") 
        typ = vals[0]
        bbox = vals[4:8]
        if typ != 'Car':
            continue
        else:
            for gtt in gt_train:
                f2 = open(gtt,"r")
                lines2 = f2.readlines()
                for l2 in lines2:
                    vals2 = l2.split(" ")
                    bbox2 = vals2[4:8]
                    if (float(bbox[0]) - th <= float(bbox2[0]) <= float(bbox[0]) + th) and (float(bbox[1]) - th <= float(bbox2[1]) <= float(bbox[1]) + th)  and (float(bbox[2]) - th <= float(bbox2[2]) <= float(bbox[2]) + th) and (float(bbox[3]) - th <= float(bbox2[3]) <= float(bbox[3]) + th):
                        print("HAHAHAHAHAHAHAHAHA")
                        print(l)
                        print(l2)
                        print(gtk)
                        print(gtt)
                        break

# In[]:




# In[]:




# In[]:




# In[]:




