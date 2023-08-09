from osgeo import gdal
import sys
import pandas as pd
import matplotlib.pyplot as plt
import cv2 as cv  # only needed if you want to convert the image

if __name__ == "__main__":
    fName = "20080816144140-01004700-VIS.ntf.r0"  # If change r number, need to change string in rstrip
    fPath = "C:/Purdue/LeGrand/EO/" + fName  # From my downloads
    dataset = gdal.Open(fPath)
    if dataset is None:
        print("dataset is None that is bad")
        sys.exit(2)
    print(
        "Driver: %s / %s"
        % (dataset.GetDriver().ShortName, dataset.GetDriver().LongName)
    )
    print(
        "Size is %d x %d x %d"
        % (dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount)
    )
    print("Projection is %s" % (dataset.GetProjection()))

    geotransform = dataset.GetGeoTransform()
    if not geotransform is None:
        print(
            "Origin = (%s, %s)" % (str(geotransform[0]), str(geotransform[3]))
        )  # NOT printing to full precision
        print(
            "Pixel Size = (%.60g, %f)" % (geotransform[1], geotransform[5])
        )  # Also not printing to full precision

    band = dataset.GetRasterBand(1)

    print("Band Type= %s" % (gdal.GetDataTypeName(band.DataType)))

    min = band.GetMinimum()
    max = band.GetMaximum()
    if min is None or max is None:
        (min, max) = band.ComputeRasterMinMax(1)
    print("Min=%.3f, Max=%.3f" % (min, max))

    if band.GetOverviewCount() > 0:
        print("Band has %d overviews" % (band.GetOverviewCount()))

    if not band.GetRasterColorTable() is None:
        print(
            "Band has a color table with %d entries"
            % (band.GetRasterColorTable().GetCount())
        )

    scanlineArray = band.ReadAsArray(
        0,
        0,
        dataset.RasterXSize,
        dataset.RasterYSize,
        dataset.RasterXSize,
        dataset.RasterYSize,
    )
    plt.imshow(scanlineArray, cmap=plt.cm.gray)

    fNameExcel = fName.replace("-", "")
    fNameExcel = fNameExcel.rstrip("0")  # Otherwise strip ending numbers as well
    fNameExcel = fNameExcel.rstrip("VIS.ntf.r")

    fNameExcel = "NITFVIS" + fNameExcel

    df = pd.read_csv("C:/Purdue\LeGrand/wamitt_gotcha_csv.csv")
    trackIDs = df["track_point.fileId"]  # Pandas series of fileId column
    trackIDsList = trackIDs.tolist()  # Pandas series to list
    fIndices = [0]
    done = 0  # Check if passed last occurance
    i = 0  # index in array
    extra = 0  # Prevent rechecking

    while done == 0:
        try:
            fIndices.append(trackIDsList.index(fNameExcel, fIndices[i] + extra))
            i += 1
            extra = 1
        except:  # index will throw error when get past last occurance
            done = 1
    del fIndices[0]

    color = df["color.color"]
    trackLat = df["track_point.latitude"]
    trackLong = df["track_point.longitude"]
    ids = df["track.id"]
    idsList = list(ids)

    idsTest = [idsList.index(8532), idsList.index(8531)]

    extra = 1
    if extra == 1:
        # for i in range(0, len(fIndices)): #Also need to make sure actually got fIndices from above
        for i in idsTest:
            truthX = trackLong[i]  # X coordinate
            truthY = trackLat[i]  # Y coordinate

            xGeoTrans = -geotransform[0] + truthX  # x translate in geospatial
            yGeoTrans = geotransform[3] - truthY  # y translate in geospatial

            xImgTrans = xGeoTrans / geotransform[1]  # x translate in pixels
            yImgTrans = yGeoTrans / -geotransform[5]  # y translate in pixels

            plt.plot(
                xImgTrans,
                yImgTrans,
                marker="o",
                markeredgecolor=color[i],
                markerfacecolor="None",
            )
    else:
        print("No truth data")

    plt.show()
