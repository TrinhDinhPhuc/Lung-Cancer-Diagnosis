#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, request, redirect, url_for, render_template
import os
import json
import glob
import numpy as np
import pandas as pd
from uuid import uuid4
import SimpleITK as sitk
import pdb
import sys
import argparse
import  cv2
from  collections  import Counter
from scipy.misc import imsave
import matplotlib.pyplot as plt
import keras
from keras.models import load_model
import tensorflow as tf
import tensorflow as tf
global graph,model
graph = tf.get_default_graph()
app = Flask(__name__)
import imageio
from PIL import Image
from gensim.summarization import summarize
from bs4 import BeautifulSoup
import requests
import re
import scipy.misc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,ForeignKey
from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)
import random

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/CBD-Life'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__='User'
    id = Column(Integer,primary_key=True,autoincrement=True)
    speciality = Column(String(20),nullable=True)
    input_type   = Column(String(20),nullable=True)
    age = Column(Integer,nullable=True)
    gender = Column(String(4),nullable=True)
    name   = Column(String(20),nullable=True)
    phone =  Column(Integer,nullable=True)
    email =  Column(String(30),nullable=True)
    input_file = Column(String(50),nullable=False)
    def __init__(self,id,speciality,input_type,age,gender,name,phone,email,input_file):
        self.id=id
        self.speciality=speciality
        self.input_type=input_type
        self.age = age
        self.gender = gender
        self.name = name
        self.phone = phone
        self.email = email
        self.input_file = input_file
    def __repr__(self):
        return ("Items(id=%d,speciality='%s',input_type='%s',age='%d',gender='%s',name='%s',phone='%d',email='%s',input_file='%s'" % (self.id,self.speciality,self.input_type,self.age,self.gender,self.name,self.phone,self.email,self.input_file))

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form
    print(form)
    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())
    upload_key = str(upload_key).replace("-","_")
    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True
    target = "D:\\npy\\uploads\\{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)
    print("=== Form Data ===")
    _input_dict = {}
    for key, value in list(form.items()):
        print(key, "=>", value)
        _input_dict[key]  = value
    print(_input_dict)
    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        upload.save(destination)
    db.session.add(User(random.randint(1,1000), _input_dict['speciality'],_input_dict['input_type'],_input_dict['age'],_input_dict['gender'],_input_dict['name'],_input_dict['phone'],_input_dict['email'],destination))
    db.session.commit()
    _link = (destination)

    print("link = ",_link)
    _save_link = ((r"\\".join(("r'"+_link+"'").split("\\"))).split(".mhd")[:-1][0]).replace("r'","")
    print("_save_link",_save_link)
    return saving_npy(_link)

def load_itk_image(filename):
    itkimage = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itkimage)
    numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
    numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))
    return numpyImage, numpyOrigin, numpySpacing

def getdata(nodule_info):
    mhd_file = nodule_info[5]
    itk_img = sitk.ReadImage(mhd_file)
    img_array = sitk.GetArrayFromImage(itk_img)  # z,y,x ordering
    origin_xyz = np.array(itk_img.GetOrigin())   # x,y,z  Origin in world coordinates (mm)
    spacing_xyz = np.array(itk_img.GetSpacing()) # spacing of voxels in world coor. (mm)
    center_xyz = (nodule_info[1], nodule_info[2], nodule_info[3])
    nodule_xyz = ((center_xyz - origin_xyz) // spacing_xyz).astype(np.int16)
    nodule = img_array[nodule_xyz[2], nodule_xyz[1] - 16:nodule_xyz[1]+16, nodule_xyz[0] - 16:nodule_xyz[0]+16]
    nodule = np.array(nodule)
    return nodule

def getsuid(filename):
    file = filename.split('\\')[-1]
    file = file.split('.mhd')[0]
    return file

def saving_npy(direction,methods=['GET', 'POST']):
    filename = getsuid(direction)
    filename = filename.split("/")[-1]
    datasub = candidates[0:0]
    for j in range(candidates.shape[0]):
        if (candidates.seriesuid[j] == filename):
            datasub = datasub.append(candidates.loc[j])
    datasub['file'] = "D:\\subset6\\" + datasub.seriesuid + ".mhd"
    datapos = datasub[datasub['class']==1]
    dataneg = datasub[datasub['class']==0]
    dataneg = dataneg.sample(n = datapos.shape[0], random_state = 42)
    path=''
    for j in range(datapos.shape[0]):
        ineed = getdata(datapos.iloc[j])
        path = "D:\\npy\\uploads\\save_npy\\1" + "\\" + "\\" +datapos.iloc[j][0]+str(datapos.iloc[j][1])+str(datapos.iloc[j][1])+str(datapos.iloc[j][2])+str(datapos.iloc[j][3])+".npy"
        np.save(path,ineed)
    for j in range(datapos.shape[0]):
        ineed = getdata(dataneg.iloc[j])
        path = "D:\\npy\\uploads\\save_npy\\0" + "\\" + "\\" +dataneg.iloc[j][0]+str(dataneg.iloc[j][1])+str(dataneg.iloc[j][1])+str(dataneg.iloc[j][2])+str(dataneg.iloc[j][3])+".npy"
        np.save(path,ineed)
    print("path:  ",path)
    a = np.load(path)
    plt.imshow(a, cmap=plt.cm.gray)
    imsave(path.replace(".npy",".png"), a)
    img = cv2.imread(path.replace(".npy",".png"))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=1)
    plt.imshow(sure_bg)
    sum=0
    for i in range(32):
        if Counter( sure_bg[i])[0] !=0:
            sum+=Counter( sure_bg[i])[0]
    _diameter_mm = sum *0.264583 * 0.65
    _img=[]
    _img.append(np.load(path))
    img = np.array(_img)
    img = img.astype('float32')
    print(img.shape)
    img = img.reshape(img.shape[0], 32, 32, 1)
    print(img.shape)
    with graph.as_default():
        y = model.predict_classes(img)
    print(y)
    if  y[0] == 0 and _diameter_mm <= 0:
        prediction = "Normal"
        treatment = "Stay healthy :) "
    elif y[0] == 0 and _diameter_mm > 0 and _diameter_mm <10:
        prediction = "Stage 1"
        treatment = summarize(state_2, word_count=100).replace("\n", "")
    else:
        prediction = "stage 2 "
        treatment = summarize(state_1, word_count=100).replace("\n", "")
    return render_template("elements.html",calculate_diameter=round(_diameter_mm,2),prediction=prediction,treatment=treatment)


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))

parser = argparse.ArgumentParser(description="Uploadr")
parser.add_argument(
    "--port", "-p",
    type=int,
    help="Port to listen on",
    default=5000,
)
args = parser.parse_args()

if __name__ == '__main__':
    flask_options = dict(
        debug   =True,
        port    =args.port,
        threaded=True,
    )
    candidates = pd.read_csv('F:\data\Luna Analysis\CSVFILES\candidates_V2.csv')
    model = load_model("C:\\Users\\PhucCoi\\Documents\\ML-by-CBD-Robotics\\Deep Learning\\Week5 Lung cancer part 2\\CNN_model.h5")
    website_url = requests.get("https://www.cancer.org/cancer/small-cell-lung-cancer/treating/by-stage.html").text
    soup = BeautifulSoup(website_url, 'lxml')
    all_texts = (soup.find('div', {'class': 'col-md-9 col-sm-12'}))
    _list = [2, 3, 4, 5, 6, 7]
    states_dict = {(all_texts.find_all('h3')[0].text): list(map(lambda a: all_texts.find_all('p')[a].text, _list))}
    _list = [6, 7, 8, 9, 10, 11, 12]
    states_dict[(all_texts.find_all('h3')[1].text)] = list(map(lambda a: all_texts.find_all('p')[a].text, _list))
    state_1 = ((str((states_dict['Stage I cancers'])).replace("'", "")).replace("]", "")).replace("[", "")
    state_2 = (((str((states_dict['Other limited stage cancers'])).replace("'", "")).replace("]", "")).replace("[","")).replace("\\n    ", "")
    app.run(**flask_options)