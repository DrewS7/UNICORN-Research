import random
import os, os.path
import shutil  # Need to pip install this I think

listFiles = os.listdir("C:/Purdue/LeGrand/EO")
numFiles = len(listFiles)
numR0Files = int(numFiles / 6)  # Ignore r set duplicates

# Pick random images for validate set, I decided on 85-15 split
numValImgs = int(0.15 * numR0Files)
valSet = random.sample(range(0, numR0Files), numValImgs)

# List all images and labels
listJpgs = os.listdir("C:/Purdue/LeGrand/EOjpg")
listLabels = os.listdir("C:/Purdue/LeGrand/EOlabels2")

# Starting and ending paths
pathBase = "C:/Purdue/LeGrand/"
pathJpg0 = pathBase + "EOjpg/"
pathJpgF = pathBase + "EOvalImgs/"
pathLabel0 = pathBase + "EOlabels2/"
pathLabelF = pathBase + "EOvalLabels/"

# Move selected imgs/lables to val folders
for i in valSet:
    valImg = listJpgs[i]
    valLabel = listLabels[i]
    shutil.move(pathJpg0 + valImg, pathJpgF + valImg)
    shutil.move(pathLabel0 + valLabel, pathLabelF + valLabel)
