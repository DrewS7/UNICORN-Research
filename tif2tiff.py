import cv2 as cv
import os, os.path

listFiles = os.listdir("C:/Purdue/LeGrand/WIP/datasets/train/images")
for i in range(0, len(listFiles)):
    fNameOld = listFiles[i]
    fNameNew = fNameOld.rstrip(".tif")
    fNameNew = fNameNew + ".tiff"
    fNameOld = "C:/Purdue/LeGrand/WIP/datasets/train/images/" + fNameOld
    fNameNew = "C:/Purdue/LeGrand/WIP/datasets/train/images/" + fNameNew
    os.rename(fNameOld, fNameNew)

listFiles = os.listdir("C:/Purdue/LeGrand/WIP/datasets/valid/images")
for i in range(0, len(listFiles)):
    fNameOld = listFiles[i]
    fNameNew = fNameOld.rstrip(".tif")
    fNameNew = fNameNew + ".tiff"
    fNameOld = "C:/Purdue/LeGrand/WIP/datasets/valid/images/" + fNameOld
    fNameNew = "C:/Purdue/LeGrand/WIP/datasets/valid/images/" + fNameNew
    os.rename(fNameOld, fNameNew)
