# -*- coding: utf-8 -*-

from glob import glob
from tqdm import tqdm
from bbox import BBox2D
from bbox import BBox2DList
from bbox.utils import nms

# In[]: BOSH
cam_preds_test = glob("testdata/det_cam_score/*.txt")
lidar_preds_test = glob("testdata/det_lidar/*.txt")

cam_preds_test.sort()
lidar_preds_test.sort()

# In[]:
conf_camera = 0.6
conf_lidar = 0.4
iou_thresh = 0.5

# In[]:
import os
import shutil

if os.path.exists('submit/fusion/'):
    shutil.rmtree('submit/fusion/')
    
os.makedirs('submit/fusion/')
    
for cpt,lpt in tqdm(zip(cam_preds_test, lidar_preds_test)):
    f = open(cpt,"r")
    lines = f.readlines()
    
    f2 = open(lpt,"r")
    lines2 = f2.readlines()
    
    bbx2ds = []
    bbx2ds2 = []
    
    bbx3ds = []
    bbx3ds2 = []
    
    dics = []
    dics2 = []
    
    for l in lines:
        vals = l.split(" ") 
        vals[-1] = vals[-1][:-1]
        typ = vals[0]
        truncated = float(vals[1])
        occluded = int(vals[2])
        alpha = float(vals[3])
        
        bbox = vals[4:8]
        bbox = [int(float(bbox[0])), int(float(bbox[1])), int(float(bbox[2])), int(float(bbox[3]))]
        
        dimensions = vals[8:11]
        dimensions = [float(dimensions[0]), float(dimensions[1]), float(dimensions[2])]
        
        location = vals[11:14]
        location = [float(location[0]), float(location[1]), float(location[2])]
        
        rotation_y = float(vals[14])
        score = float(vals[15])
        
        if score >= conf_camera:
            bbx2ds.append(BBox2D(x = (bbox[0], bbox[1], bbox[2], bbox[3]), mode=1))
            dic = {}
            dic["bbx2d"] = BBox2D(x = (bbox[0], bbox[1], bbox[2], bbox[3]), mode=1)
            dic["score"] = score
            dic["line"] = l
            dics.append(dic)
        
    for l2 in lines2:
        vals2 = l2.split(" ") 
        vals2[-1] = vals2[-1][:-1]
        typ2 = vals2[0]
        truncated2 = float(vals2[1])
        occluded2 = int(vals2[2])
        alpha2 = float(vals2[3])
        
        bbox2 = vals2[4:8]
        bbox2 = [int(bbox2[0]), int(bbox2[1]), int(bbox2[2]), int(bbox2[3])]
        
        dimensions2 = vals2[8:11]
        dimensions2 = [float(dimensions2[0]), float(dimensions2[1]), float(dimensions2[2])]
        
        location2 = vals2[11:14]
        location2 = [float(location2[0]), float(location2[1]), float(location2[2])]
        
        rotation_y2 = float(vals2[14])
        score2 = float(vals2[15])
            
        if score2 >= conf_lidar:
            bbx2ds2.append(BBox2D(x = (bbox2[0], bbox2[1], bbox2[2], bbox2[3]), mode=1))
            dic2 = {}
            dic2["bbx2d"] = BBox2D(x = (bbox2[0], bbox2[1], bbox2[2], bbox2[3]), mode=1)
            dic2["score"] = score2
            dic2["line"] = l2
            dics2.append(dic2)

    dics_all = dics + dics2

    bbx2ds = []
    confidences = []
    for dic in dics_all:
        bbx2ds.append(dic["bbx2d"])
        confidences.append(dic["score"])
        
    bbx2dlist = BBox2DList(bbx2ds, mode=1)
    new_boxes = nms(bbx2dlist, confidences, thresh=iou_thresh)
    
    list_final = []
    for i in new_boxes:
        list_final.append(dics_all[i])

    out_file = open("submit/fusion/{}".format(cpt.split('/')[-1]),"w")
      
    while len(list_final) > 0:
        asd = list_final.pop()["line"]
        asd = asd.split(" ") 
        asd[-1] = asd[-1][:-1]
        typ = asd[0]
        truncated = float(asd[1])
        occluded = int(asd[2])
        alpha = float(asd[3])
        
        bbox = asd[4:8]
        bbox = [int(float(bbox[0])), int(float(bbox[1])), int(float(bbox[2])), int(float(bbox[3]))]
        
        dimensions = asd[8:11]
        dimensions = [float(dimensions[0]), float(dimensions[1]), float(dimensions[2])]
        
        location = asd[11:14]
        location = [float(location[0]), float(location[1]), float(location[2])]
        
        rotation_y = float(asd[14])
        score = float(asd[15])
        
        merged = str(typ) + " " + str(truncated) + " " + str(occluded) + " " + str(alpha) + " " + str(bbox[0]) + \
        " " + str(bbox[1]) + " " + str(bbox[2]) + " " + str(bbox[3]) + " " + str(dimensions[0]) + " " + str(dimensions[1]) + \
        " " + str(dimensions[2]) + " " + str(location[0]) + " " + str(location[1]) + " " + str(location[2]) + \
        " " + str(rotation_y) + " " + "1.00\n"
        
        if bbox[0]<0 or bbox[2]<=bbox[0] or bbox[1]<0 or bbox[3]<bbox[1]:
            continue
        
        out_file.write(merged)
        
#        asd = list_final.pop()["line"]
#        out_file.write(" ".join(asd.split(" ")[:-1]) + ' 1.00\n') 
#        out_file.write(list_final.pop()["line"])
    out_file.close()

# In[]:




# In[]:




# In[]:




