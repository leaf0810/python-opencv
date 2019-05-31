import matplotlib.patches as patches
import matplotlib.pyplot as plt
import cv2
import os
import glob
import xml.etree.ElementTree as ET
import copy

def getvalue(path,tag,key):
    tree = ET.parse(path)
    nodelist=tree.findall(tag)
    obj={}
    objects=[]

    for node in nodelist:
        name=node.find(key).text
        child_nodelist=node.findall('bndbox')
        for child in child_nodelist:
            xmin=child.find('xmin').text
            ymin=child.find('ymin').text
            xmax=child.find('xmax').text
            ymax=child.find('ymax').text

            obj['name']=name
            obj['xmin']=xmin
            obj['ymin']=ymin
            obj['xmax']=xmax
            obj['ymax']=ymax
        
        objects.append(copy.deepcopy(obj))
    #print(objects)
    return objects
    
#getvalue("total_labels/138.xml",'object','name')

imgdir=("images/")
imgs=glob.glob(os.path.join(imgdir,'*'))
for imgpathname in imgs:
    _,imgname=os.path.split(imgpathname)
    labelname=os.path.splitext(imgname)[0]+".xml"
    labelfile="image_label/%s"%labelname
    objects=getvalue(labelfile,'object','name')
    
    img=cv2.imread(imgpathname)

    for obj in objects:
        xmin=int(obj['xmin'])
        ymin=int(obj['ymin'])
        xmax=int(obj['xmax'])
        ymax=int(obj['ymax'])
        
        cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (0,255,0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        text = obj['name']
        cv2.putText(img, text, (xmin, ymin), font, 0.7, (0,0,255), 1)
    cv2.imwrite("image_rec/%s_rec.jpg"%os.path.splitext(imgname)[0], img)
