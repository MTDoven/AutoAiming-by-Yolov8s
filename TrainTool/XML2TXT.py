import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = ['train', 'test', 'val']
classes = ['person','self']
imgsz = 640

def convert(box):
    dw = 1./imgsz
    dh = 1./imgsz
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x, y, w, h)

def convert_annotation(image_id):
    in_file = open('../DataSet/Annotations/%s.xml' % (image_id), encoding='utf-8')
    out_file = open('../DataSet/labels/%s.txt' % (image_id), 'w', encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    if size != None:
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            print(image_id, cls, b)
            bb = convert(b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()
print(wd)

for image_set in sets:
    if not os.path.exists('../DataSet/labels/'):
        os.makedirs('../DataSet/labels/')
    image_ids = open('../DataSet/ImageSets/%s.txt' % (image_set)).read().strip().split()
    list_file = open('../DataSet/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write('../DataSet/images/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()
