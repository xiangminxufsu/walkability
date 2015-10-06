import arcpy
import sys
import os
from tools import createMaping,addFld,updateTable

def linemain(usng,roads,scratch):
	print "starting subprocess"
	arcpy.env.overwriteOutput = True
	unsplitRd = os.path.join(scratch,"unsplitRd.shp")
	arcpy.UnsplitLine_management(roads, unsplitRd,["NAME"])

	infeatures = [unsplitRd,unsplitRd]
	outfeatures = scratch+"\\streets_intersection.shp"
	arcpy.Intersect_analysis (infeatures,outfeatures,  "ONLY_FID", "", "POINT")

	xy_tol = "0.02 Miles"
	arcpy.DeleteIdentical_management(outfeatures, ["SHAPE"], xy_tol)



	pointFeature = outfeatures
	##create field mappings
	joinFields = ['LABEL']
	finalMapings = createMaping(usng,pointFeature,joinFields)
	##conducting spatial join, joinging usng grids to parcels centroids
	print "usng joing to parcel centroids"
	interJoin = scratch+ "\\intersectionSpatialJoin.shp"
	arcpy.analysis.SpatialJoin(pointFeature, usng,interJoin , "JOIN_ONE_TO_ONE", "KEEP_ALL", finalMapings, "INTERSECT", "", "")

	pointDict = {}
	with arcpy.da.SearchCursor(interJoin, ['LABEL']) as cursor:
		for row in cursor:
			if row[0] not in pointDict :
				pointDict[row[0]] = 1
			else:
				pointDict[row[0]] += 1
				
	addFld(usng,"INTER_DENS","SHORT",4,0)
	updateTable(usng,"LABEL","INTER_DENS",pointDict)
	print "ending subprocess"
	return pointDict