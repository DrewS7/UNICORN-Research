from osgeo import gdal
import pandas as pd
import matplotlib.pyplot as plt
import cv2 as cv
import os, os.path

if __name__ == "__main__":
    listFiles = os.listdir("C:\Purdue\LeGrand\EO")
    numFiles = len(listFiles)

    df = pd.read_csv("C:/Purdue/LeGrand/wamitt_gotcha_csv.csv")
    imgIDs = df["track_point.fileId"]  # Pandas series of fileId column
    classesPd = df["target_type.name"]
    boxWidth = df["track.width"]
    boxLength = df["track.length"] #YOLO uses width/height, UNICORN length/width, I think height=length? Can also flip and try again
    # or just make a square. Also, not entirely sure what the values mean, could try manual truth. For now, just 15x15 pixel square.
    # Try and email authors - which dimension is which, and what units are the numbers in? Too small for pixels, too large for geospat
    trackLat = df["track_point.latitude"]
    trackLong = df["track_point.longitude"]

    trackIDsList = imgIDs.tolist()  # Pandas series to list
    classesList = classesPd.tolist()
    xCenterList = []
    yCenterList = []
    boxLengthList = []
    boxWidthList = []
    goodRows = []
    goodClasses = []

    uniqueClasses = set(classesList)
    uniqueClassesList = list(uniqueClasses)
    uniqueClassesList.sort()
    #print(len(uniqueClasses)) #21 classes
    #print(uniqueClassesList)
    uniqueIDs = set(imgIDs)
    # print(len(uniqueIDs)) #6471 unique IDs, I only have 500 images

    for i in range(0, len(imgIDs)):  #  geospatial to YOLO (norm by img size, [0,1])
        # for i in range(0, 10):
        fName = imgIDs[i]
        # Get Excel ID into format of file ID
        fName = fName + "-VIS.ntf.r0"
        fName = fName.lstrip("NITFVIS")
        fName = fName[:14] + "-" + fName[14:]

        if fName in listFiles:  # Only deal with files in tar 00
            # Open file
            fPath = "C:/Purdue/LeGrand/EO/" + fName
            dataset = gdal.Open(fPath)
            geotransform = dataset.GetGeoTransform()
            # Convert geospatial to YOLO
            truthX = trackLong[i]  # X coordinate
            truthY = trackLat[i]  # Y coordinate
            xGeoTrans = -geotransform[0] + truthX  # x translate in geospatial
            yGeoTrans = geotransform[3] - truthY  # y translate in geospatial
            xImgTrans = xGeoTrans / geotransform[1]  # x translate in pixels
            yImgTrans = yGeoTrans / -geotransform[5]  # y translate in pixels
            xImgYolo = xImgTrans / dataset.RasterXSize  # x as proportion of total image
            yImgYolo = yImgTrans / dataset.RasterYSize  # y as proportion of total image
            # Store YOLO coords
            xCenterList.append(xImgYolo)
            yCenterList.append(yImgYolo)
            # Make and store bounding box
            #bBoxX = 15 / dataset.RasterXSize
            #bBoxY = 15 / dataset.RasterXSize
            bBoxX = 4 * boxLength[i] / dataset.RasterXSize
            bBoxY = 4 * boxWidth[i] / dataset.RasterYSize
            boxLengthList.append(bBoxX)
            boxWidthList.append(bBoxY)
            # Store row of eligible image
            goodRows.append(i)
            #Get class of truth entry
            classTruth = classesList[i]
            numClassTruth = uniqueClassesList.index(classTruth)
            goodClasses.append(numClassTruth)

    print("Part 1 done")

    for idx in range(0, len(goodRows)):  # For each row for an image I have
        # for idx in range(0, 10):
        goodIndex = goodRows[idx] #Iterate through list of images I have, not all iamges
        fileName = "C:/Purdue/LeGrand/EOlabels2/" + imgIDs[goodIndex] + ".txt"  # YOLO title
        if os.path.isfile(fileName):
            with open(fileName, "a") as f:  # Append as new row to existing file
                classInt = goodClasses[idx]  # Number for class
                # YOLO annotation format
                label = (
                    "\n"
                    + str(classInt)  # Class number
                    + " "
                    + str(xCenterList[idx])  # x location
                    + " "
                    + str(yCenterList[idx])  # y location
                    + " "
                    + str(boxLengthList[idx])  # bounding box width
                    + " "
                    + str(boxWidthList[idx])  # bounding box height
                )
                f.write(label)
        else:
            with open(fileName, "w") as f:  # Write new file
                classInt = goodClasses[idx]
                label = (
                    str(classInt)
                    + " "
                    + str(xCenterList[idx])
                    + " "
                    + str(yCenterList[idx])
                    + " "
                    + str(boxLengthList[idx])
                    + " "
                    + str(boxWidthList[idx])
                )
                f.write(label)
