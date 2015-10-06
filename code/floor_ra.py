import arcpy
import sys
import os
from sets import Set
from multiprocessing import Process, freeze_support

from line import linemain
from tools import updateTable,addFld,createMaping

def cal_fl_ra(scratch):
	"""
	return two dict related to retail floor ratio
	"""
	#retail floor area ratio
	totalLvgDict = {}
	landAreaDict = {}
	where = arcpy.AddFieldDelimiters(scratch+ "\\parcelCentroidsSpatialJoin.shp", 'DOR_UC')
	where = where+" in ('010','011','012','013','014','015','016','017','018','019',\
						'020','021','022','023','024','025','026','027','028','029',\
						'030','031','032','033','034','035','036','037','038','039')"

	with arcpy.da.SearchCursor(scratch+ "\\parcelCentroidsSpatialJoin.shp", ['TOT_LVG_AR','landarea','LABEL','DOR_UC'], where) as cursor:

				for row in cursor:
					if row[2] not in totalLvgDict:
						totalLvgDict[row[2]] = row[0]
					else:
						totalLvgDict[row[2]] += row[0]

					if row[2] not in landAreaDict:
						landAreaDict[row[2]] = row[1]
					else:
						landAreaDict[row[2]] += row[1]
						
	return totalLvgDict,landAreaDict