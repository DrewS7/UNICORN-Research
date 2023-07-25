# example script on how to read a NITF file in Python
# tested with UNICRON 2008 data that has been truthed
# converted to Python 3.X tested with Python 3.7 from
# Anaconda 12/2018

from osgeo import gdal
import sys
import pandas as pd
import matplotlib.pyplot as plt
#import cv2 as cv # only needed if you want to convert the image

if __name__ == "__main__":
	fName = "20080816144140-01004700-VIS.ntf.r0" #If change r number, need to change string in rstrip
	#fPath = "X:/EO/" + fName #From data depot
	fPath = "C:/Purdue/LeGrand/EO/" + fName #From my downloads
	dataset = gdal.Open(fPath)
	if dataset is None:
		print("dataset is None that is bad")
		sys.exit(2)
	print('Driver: %s / %s' % (dataset.GetDriver().ShortName, dataset.GetDriver().LongName))
	print('Size is %d x %d x %d' % (dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount))
	print('Projection is %s' % (dataset.GetProjection()))

	geotransform = dataset.GetGeoTransform()
	if not geotransform is None:
		print('Origin = (%s, %s)' % (str(geotransform[0]), str(geotransform[3]))) #NOT printing to full precision
		print('Pixel Size = (%.60g, %f)' % (geotransform[1] ,geotransform[5])) #Also not printing to full precision

	band = dataset.GetRasterBand(1)

	print('Band Type= %s' % (gdal.GetDataTypeName(band.DataType)))

	min = band.GetMinimum()
	max = band.GetMaximum()
	if min is None or max is None:
		(min,max) = band.ComputeRasterMinMax(1)
	print('Min=%.3f, Max=%.3f' % (min, max))

	if band.GetOverviewCount() > 0:
		print('Band has %d overviews' % (band.GetOverviewCount()))

	if not band.GetRasterColorTable() is None:
		print('Band has a color table with %d entries' % (band.GetRasterColorTable().GetCount()))

	# Read the data from the NITF file and place into a numpy array
	# ReadAsArray(self, xoff=0, yoff=0, win_xsize=None, win_ysize=None, 
	# buf_xsize=None, buf_ysize=None, buf_obj=None)	
	# band.XSize is how many pixels in left to right
	# band.YSize is how many pixels up to down
	# this grabs the OSU stadium in frame ~/data/CLIF2007/20071028142502-01000100-VIS.ntf.r0
	# you can display the entire frame but matplot lib is slow
	#scanlineArray = band.ReadAsArray(6000, 5000, 1000, 1000, 
	#	1000, 1000)
	#
	# reads the entire image at full resolution, this will put the track on the
	# correct vehicle
	scanlineArray = band.ReadAsArray(0, 0, dataset.RasterXSize, 
		dataset.RasterYSize, dataset.RasterXSize, dataset.RasterYSize)
	print(scanlineArray.shape)
	print(type(scanlineArray[0][0]))
	# this line saves the image data as a jpg a good way to do conversion, if 
	# you want to get the data out of the NITF file format, you can use OpenCV
	# and imwrite the image out as a jpeg file
	# cv.imwrite("/Users/rovitotv/temp/output.jpg", scanlineArray)

	plt.imshow(scanlineArray, cmap=plt.cm.gray)

	#What do they mean with track length/width? Can't be pixels, bc different resolutions, can't be geospatial bc too big

	fNameExcel = (fName.replace("-", ""))
	fNameExcel = fNameExcel.rstrip("0") #Otherwise strip ending numbers as well
	fNameExcel = fNameExcel.rstrip("VIS.ntf.r")
	fNameExcel = "NITFVIS" + fNameExcel
	print(fNameExcel)

	#df = pd.read_csv("X:/truth/wamitt_gotcha_csv.csv") Why can't I access the .csv file in network drive?
	#What did start parse stuff mean that I got rid of?

	df = pd.read_csv("C:/Purdue\LeGrand/wamitt_gotcha_csv.csv")
	trackIDs = df["track_point.fileId"] #Pandas series of fileId column
	trackIDsList = trackIDs.tolist() #Pandas series to list
	fIndices = [0]
	done = 0 #Check if passed last occurance
	i = 0 #index in array
	extra = 0 #Prevent rechecking
	
	while done == 0:
		try: 
			fIndices.append(trackIDsList.index(fNameExcel, fIndices[i]+extra))
			i += 1
			extra = 1
		except: #index will throw error when get past last occurance
			done = 1
	del fIndices[0]

	color = df["color.color"]
	trackLat = df["track_point.latitude"]
	trackLong = df["track_point.longitude"]

	if extra == 1:
		for i in range(0, len(fIndices)): #Also need to make sure actually got fIndices from above
			truthX = trackLong[fIndices[i]] #X coordinate
			truthY = trackLat[fIndices[i]] #Y coordinate

			xGeoTrans = -geotransform[0] + truthX #x translate in geospatial
			yGeoTrans = geotransform[3] - truthY #y translate in geospatial

			xImgTrans = xGeoTrans / geotransform[1] #x translate in pixels
			yImgTrans = yGeoTrans / -geotransform[5] # y translate in pixels		

			plt.plot(xImgTrans, yImgTrans, marker = "o", markeredgecolor = color[fIndices[i]], markerfacecolor = "None")
	else:
		print("No truth data")

	plt.show()