import random
import os, os.path
import shutil  # Need to pip install this I think

listFiles = os.listdir("C:/Purdue/LeGrand/EO")
numFiles = len(listFiles)
numR0Files = numFiles / 6  # Ignore r set duplicates

# Pick random images for validate set, I decided on 85-15 split
numValImgs = round(0.15 * numR0Files)
valSet = random.sample(range(numR0Files), numValImgs)
print(valSet)

# List all images and labels
listJpgs = os.listdir("C:/Purdue/LeGrand.EOjpg")
listLabels = os.listdir("C:/Purdue/LeGrand/EOlabels")

# Starting and ending paths
pathBase = "C:/Purdue/LeGrand/"
pathJpg0 = pathBase + "EOjpg"
pathJpgF = pathBase + "EOvalImgs"
pathLabel0 = pathBase + "EOlabels"
pathLabelF = pathBase + "EOvalLabels"

# Move selected imgs/lables to val folders
for i in valSet:
    valImg = listJpgs[i]
    valLabel = listLabels[i]
    shutil.move(pathJpg0 + valImg, pathJpgF + valImg)
    shutil.move(pathLabel0 + valLabel, pathLabelF + valLabel)
