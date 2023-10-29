import cv2 as cv
import os, os.path
from PIL import Image
from itertools import product
import math

pathTrain = "C:/Purdue/LeGrand/WIP/datasets/validNormal/images/"  # train or valid
listFiles = os.listdir(pathTrain)

pathChips = "C:/Purdue/LeGrand/WIP/datasets/xViewPNG/valid/imagesPNG/"  # train or valid
chipNames = os.listdir(pathChips)

for i in range(0, len(listFiles)):
    # for i in range(0, 1):
    img = Image.open(pathTrain + listFiles[i])
    w, h = img.size
    dW = math.floor(w / 4)
    dH = math.floor(h / 4)
    labelName = 0

    with open(
        "C:/Purdue/LeGrand/WIP/datasets/validNormal/labels/"  # train or valid
        + listFiles[i].rstrip(".tiff")
        + ".txt"
    ) as fo:
        lines = fo.readlines()
        # Image is divided into 16, left -> right, top -> bottom. Attach bbox to corresponding chip as long as whole box fits in chip
        for j in range(0, len(lines)):
            if lines[j] == "\n":
                continue
            line = lines[j].split()
            line = [float(k) for k in line]
            if ((line[1] - line[3]) < (dW / w)) and ((line[1] - line[3]) < (dW / w)):
                if ((line[2] - line[4]) < (dH / h)) and (
                    (line[2] + line[4]) < (dH / h)
                ):
                    labelName = chipNames[(i - 1) * 16]
                elif (
                    ((line[2] - line[4]) > (dH / h))
                    and ((line[2] + line[4]) > (dH / h))
                ) and (
                    ((line[2] - line[4]) < 2 * (dH / h))
                    and ((line[2] + line[4]) < 2 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 4]
                elif (
                    ((line[2] - line[4]) > 2 * (dH / h))
                    and ((line[2] + line[4]) > 2 * (dH / h))
                ) and (
                    ((line[2] - line[4]) < 3 * (dH / h))
                    and ((line[2] + line[4]) < 3 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 8]
                elif (
                    ((line[2] - line[4]) > 3 * (dH / h))
                    and ((line[2] + line[4]) > 3 * (dH / h))
                ) and (
                    ((line[2] - line[4]) < 4 * (dH / h))
                    and ((line[2] + line[4]) < 4 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 12]

            elif (
                ((line[1] - line[3]) > (dW / w)) and ((line[1] - line[3]) > (dW / w))
            ) and (
                ((line[1] - line[3]) < 2 * (dW / w))
                and ((line[1] - line[3]) < 2 * (dW / w))
            ):
                if ((line[2] - line[4]) < (dH / h)) and (
                    (line[2] + line[4]) < (dH / h)
                ):
                    labelName = chipNames[(i - 1) * 16 + 1]
                elif (
                    ((line[2] - line[4]) > (dH / h))
                    and ((line[2] + line[4]) > (dH / h))
                ) and (
                    ((line[2] - line[4]) < 2 * (dH / h))
                    and ((line[2] + line[4]) < 2 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 5]
                elif (
                    ((line[2] - line[4]) > 2 * (dH / h))
                    and ((line[2] + line[4]) > 2 * (dH / h))
                ) and (
                    ((line[2] - line[4]) < 3 * (dH / h))
                    and ((line[2] + line[4]) < 3 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 9]
                elif (
                    ((line[2] - line[4]) > 3 * (dH / h))
                    and ((line[2] + line[4]) > 3 * (dH / h))
                ) and (
                    ((line[2] - line[4]) < 4 * (dH / h))
                    and ((line[2] + line[4]) < 4 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 13]

            elif (
                ((line[1] - line[3]) > 2 * (dW / w))
                and ((line[1] - line[3]) > 2 * (dW / w))
            ) and (
                ((line[1] - line[3]) < 3 * (dW / w))
                and ((line[1] - line[3]) < 3 * (dW / w))
            ):
                if ((line[2] - line[4]) < (dH / h)) and (
                    (line[2] + line[4]) < (dH / h)
                ):
                    labelName = chipNames[(i - 1) * 16 + 2]
                elif (
                    ((line[2] - line[4]) > (dH / h))
                    and ((line[2] + line[4]) > (dH / h))
                ) and (
                    ((line[2] - line[4]) < 2 * (dH / h))
                    and ((line[2] + line[4]) < 2 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 6]
                elif (
                    ((line[2] - line[4]) > 2 * (dH / h))
                    and ((line[2] + line[4]) > 2 * (dH / h))
                ) and (
                    ((line[2] - line[4]) < 3 * (dH / h))
                    and ((line[2] + line[4]) < 3 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 10]
                elif (
                    ((line[2] - line[4]) > 3 * (dH / h))
                    and ((line[2] + line[4]) > 3 * (dH / h))
                ) and (
                    ((line[2] - line[4]) < 4 * (dH / h))
                    and ((line[2] + line[4]) < 4 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 14]

            elif (
                ((line[1] - line[3]) > 3 * (dW / w))
                and ((line[1] - line[3]) > 3 * (dW / w))
            ) and (
                ((line[1] - line[3]) < 4 * (dW / w))
                and ((line[1] - line[3]) < 4 * (dW / w))
            ):
                if ((line[2] - line[4]) < (dH / h)) and (
                    (line[2] + line[4]) < (dH / h)
                ):
                    labelName = chipNames[(i - 1) * 16 + 3]
                elif (
                    ((line[2] - line[4]) > (dH / h))
                    and ((line[2] + line[4]) > (dH / h))
                ) and (
                    ((line[2] - line[4]) < 2 * (dH / h))
                    and ((line[2] + line[4]) < 2 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 7]
                elif (
                    ((line[2] - line[4]) > 2 * (dH / h))
                    and ((line[2] + line[4]) > 2 * (dH / h))
                ) and (
                    ((line[2] - line[4]) < 3 * (dH / h))
                    and ((line[2] + line[4]) < 3 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 11]
                elif (
                    ((line[2] - line[4]) > 3 * (dH / h))
                    and ((line[2] + line[4]) > 3 * (dH / h))
                ) and (
                    ((line[2] - line[4]) < 4 * (dH / h))
                    and ((line[2] + line[4]) < 4 * (dH / h))
                ):
                    labelName = chipNames[(i - 1) * 16 + 15]
            if labelName == 0:
                continue
            fileName = (
                "C:/Purdue/LeGrand/WIP/datasets/xViewPNG/valid/chipLabels/"  # train or valid
                + labelName
                + ".txt"
            )

            label = lines[j].split()
            # Scale down width/height by 16 bc 16 chips
            label[3] = float(label[3]) / 16
            label[4] = float(label[4]) / 16
            # Scale x/y coords to be right proportion relative to new chips, 0.25 bc 16 chips
            label[1] = (float(label[1]) % 0.25) / 0.25
            label[2] = (float(label[2]) % 0.25) / 0.25
            # Formatting
            label[0] = int(label[0])
            label = str(label) + "\n"
            label = label.replace(",", "").replace("[", "").replace("]", "")

            if os.path.isfile(fileName):
                with open(fileName, "a") as f:  # Append as new row to existing file
                    f.write(label)
            else:
                with open(fileName, "w") as f:  # Write new file
                    f.write(label)
