import arcpy
import sys
import os
from sets import Set
from multiprocessing import Process, freeze_support

from line import linemain
from tools import dor_to_int,updateTable,addFld,createMaping
from calculate import calWalk

def cal_dens(usng,parcels,scratch):
	"""
	return three dicts for futher use
	"""
	
	usngAreaDict={}
	usngResDict={}
	where = arcpy.AddFieldDelimiters(scratch+ "\\parcelCentroidsSpatialJoin.shp", 'DOR_UC')
	where = arcpy.AddFieldDelimiters(scratch+ "\\parcelCentroidsSpatialJoin.shp", 'DOR_UC') + " in ('001','002','003','004','005','006','007','008','009')"
	with arcpy.da.SearchCursor(scratch+ "\\parcelCentroidsSpatialJoin.shp", ['NO_RES_UNT','landarea','LABEL','DOR_UC'], where) as cursor:
				for row in cursor:
					if row[2] not in usngResDict:
						usngResDict[row[2]] = row[0]
					else:
						usngResDict[row[2]] += row[0]

					if row[2] not in usngAreaDict:
						usngAreaDict[row[2]] = row[1]
					else:
						usngAreaDict[row[2]] += row[1]
	
	landUseMixDict = {}
	with arcpy.da.SearchCursor(scratch+"\\parcelCentroidsSpatialJoin.shp",['LABEL','DOR_UC']) as cursor:
		for row in cursor:
			val = dor_to_int(row[1])
			if row[0] not in landUseMixDict:
				landUseMixDict[row[0]] = Set()
				landUseMixDict[row[0]].add(val)
			else:
				landUseMixDict[row[0]].add(val)
				
	return usngAreaDict,usngResDict,landUseMixDict