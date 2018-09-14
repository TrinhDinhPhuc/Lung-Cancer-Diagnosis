import pydicom
import os
import pandas as pd
import numpy
import SimpleITK as sitk
import numpy as np
import glob
import csv
import os
from sklearn.model_selection import train_test_split
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import pyplot, cm
PathDicom = "E:\\subset1"
lstFilesDCM = []
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".mhd" in filename.lower():
            lstFilesDCM.append(os.path.join(dirName,filename))

def load_itk_image(filename):
    itkimage = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itkimage)
    numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
    numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))
    return numpyImage, numpyOrigin, numpySpacing
# numpyImage, numpyOrigin, numpySpacing = load_itk_image(lstFilesDCM[0])
# print (numpyImage.shape)
# print (numpyOrigin)
# print (numpySpacing)
# D:\\subset6\\1.3.6.1.4.1.14519.5.2.1.6279.6001.106630482085576298661469304872.mhd
print(load_itk_image("D:\\npy\\uploads\\5da160ab_7d9a_4e78_ad28_3dea61840734\\a.mhd"))
# import scipy.misc
# for index, i in enumerate(range(0,140,1)):
#     scipy.misc.toimage(load_itk_image(r"D:\\subset6\\1.3.6.1.4.1.14519.5.2.1.6279.6001.106630482085576298661469304872.mhd")[0][i]).save("D:\\npy\\imgs\\slices\\Img_"+str(i)+ ".jpg")
print(load_itk_image("D:\\subset6\\1.3.6.1.4.1.14519.5.2.1.6279.6001.106630482085576298661469304872.mhd"))