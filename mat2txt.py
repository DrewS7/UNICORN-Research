import pandas as pd
import cv2 as cv
import os, os.path

dfTargets = pd.read_csv("C:/Users/Drew/Downloads/matTargets.csv")
dfIDs = pd.read_csv("C:/Users/Drew/Downloads/matIDs.csv")

#Csv column names wrong bc misread docs
IDs = dfIDs["ids"]
classes = dfTargets["classes"]
xLeft = dfTargets["xcenter"]
yTop = dfTargets["ycenter"]
xRight = dfTargets["xbox"]
yBot = dfTargets["ybox"]
uniqueIDs = set(IDs)
uniqueIDsSorted = list(uniqueIDs)
uniqueIDsSorted.sort()
dimensions = []

#From properties, images different dimensions
for i in uniqueIDsSorted:
    imgName = "C:/Purdue/LeGrand/WIP/datasets/trainGoodXview/images/" + str(i) + ".tif"
    if os.path.isfile(imgName):
        img = cv.imread("C:/Purdue/LeGrand/WIP/datasets/trainGoodXview/images/" + str(i) + ".tif")
        dimensions.append(img.shape)
    else:
        img = cv.imread("C:/Purdue/LeGrand/WIP/datasets/validGoodXview/images/" + str(i) + ".tif")
        dimensions.append(img.shape)
#width is dimensions[i][1], height is dimensions[i][0]

xCenter = []
yCenter = []
xWidth = []
yHeight = []

#xyxy2xywh my version
for i in range(0, len(xLeft)):
#for i in range(0, 10):
    xCenterTemp = (xLeft[i] + xRight[i]) / 2
    xCenter.append(xCenterTemp)
    yCenterTemp = (yTop[i] + yBot[i]) / 2
    yCenter.append(yCenterTemp)
    xWidthTemp = xRight[i] - xLeft[i]
    xWidth.append(xWidthTemp)
    yHeightTemp = -(yTop[i] - yBot[i])
    yHeight.append(yHeightTemp)
#Normalize values
for i in range(0, len(xLeft)):
#for i in range(0, 10):
    imgID = IDs[i]
    imgPos = uniqueIDsSorted.index(imgID)

    xCenter[i] = xCenter[i] / dimensions[imgPos][1]
    yCenter[i] = yCenter[i] / dimensions[imgPos][0]
    xWidth[i] = xWidth[i] / dimensions[imgPos][1]
    yHeight[i] = yHeight[i] / dimensions[imgPos][0]

print("Done numbers")

#From convTruthUNICORN
for idx in range(0, len(xLeft)):
#for idx in range(0, 10):
    fileRoot = "C:/Purdue/LeGrand/WIP/xViewLabels/"
    fileName = fileRoot + str(IDs[idx]) + ".txt"
    if os.path.isfile(fileName):
        with open(fileName, "a") as f:  # Append as new row to existing file
            classInt = classes[idx]  # Number for class
            # YOLO annotation format
            label = (
                "\n"
                + str(classInt)  # Class number
                + " "
                + str(xCenter[idx])  # x location
                + " "
                + str(yCenter[idx])  # y location
                + " "
                + str(xWidth[idx])  # bounding box width
                + " "
                + str(yHeight[idx])  # bounding box height
            )
            f.write(label)
    else:
        with open(fileName, "w") as f:  # Write new file
            classInt = classes[idx]  # Number for class
            # YOLO annotation format
            label = (
                "\n"
                + str(classInt)  # Class number
                + " "
                + str(xCenter[idx])  # x location
                + " "
                + str(yCenter[idx])  # y location
                + " "
                + str(xWidth[idx])  # bounding box width
                + " "
                + str(yHeight[idx])  # bounding box height
            )
            f.write(label)