
import arcpy
import sys
import os
from sets import Set
from multiprocessing import Process, freeze_support

from code.line import linemain
from code.calculate import calWalk
from code.res_dens import cal_dens
from code.floor_ra import cal_fl_ra
from code.tools import createMaping,updateTable,addFld
from code.globalval import Scratch, Usng,Parcels,Roads



def main():
	
	arcpy.env.overwriteOutput = True
	
	##global variables
	scratch = Scratch
	parcels = Parcels
	roads = Roads
	usng = Usng
	
	print "repairing geometry"
	arcpy.management.RepairGeometry(parcels)

	##creat parcels centroids
	print "converting parcels to centroids"
	arcpy.management.FeatureToPoint(parcels, scratch+ "\\parcelcentroids.shp", "INSIDE")

	##create field mappings
	joinFields = ['DOR_UC','NO_RES_UNT','landarea','TOT_LVG_AR','LABEL']
	
	finalMappings = createMaping(usng,parcels,joinFields)
	##conducting spatial join, joinging usng grids to parcels centroids
	print "usng joing to parcel centroids"
	arcpy.analysis.SpatialJoin(scratch+ "\\parcelCentroids.shp", usng, scratch+ "\\parcelCentroidsSpatialJoin.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", finalMappings, "INTERSECT", "", "")
	
	usngAreaDict,usngResDict,landUseMixDict = cal_dens(usng,parcels,scratch)
	#retail floor area ratio
	totalLvgDict,landAreaDict = cal_fl_ra(scratch)

	usngDesDict={}					
	for item in usngResDict:
		if item in usngAreaDict and usngAreaDict[item]!=0:
			usngDesDict[item] = usngResDict[item]*10760000 / (usngAreaDict[item] )
			
	landUseCountDict = {}
	for item in landUseMixDict:
		landUseCountDict[item] = len(landUseMixDict[item])

	landRatioDict={}
	for item in totalLvgDict:
		if item in usngAreaDict and usngAreaDict[item]!=0:
			landRatioDict[item] = totalLvgDict[item]*10760000/landAreaDict[item]
	
	pointDict = linemain(usng,roads,scratch)
	#add & update tables in the usng file
	addFld(usng,"INTER_DENS","SHORT",4,0)		
	addFld(usng,"RES_DENS","DOUBLE",6,12)
	addFld(usng,"LAND_MIX","SHORT",4,0)
	addFld(usng,"RA_FLO_RA","DOUBLE",6,12)
	updateTable(usng,"LABEL","INTER_DENS",pointDict)
	updateTable(usng,"LABEL","RES_DENS",usngDesDict)
	updateTable(usng,"LABEL","LAND_MIX",landUseCountDict)
	updateTable(usng,"LABEL","RA_FLO_RA",landRatioDict)
	#final step, calculate walkability score
	calWalk(usng,["RES_DENS","LAND_MIX","RA_FLO_RA","INTER_DENS"],"WKSCORE")


if __name__ == '__main__':
	main()
##references to input data			

