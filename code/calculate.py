#calculate walkability
from sets import Set
import arcpy
import sys

def calWalk(shpfile,atrList,newfield):
	usng  = shpfile
	
	allfield = Set()
	for fld in arcpy.ListFields(usng):
		allfield.add(fld.name)
	for x in atrList:
		if x not in allfield:
			print "could not find %s in usng" %(x)
			sys.exit(0)
	
	#find the max value first, then divid the max, multiply 25
	maxList=[0 for x in atrList]
	#print "maxList", maxList
	with arcpy.da.SearchCursor(usng, atrList) as cursor:
		for row in cursor:
			for i in range(0,len(atrList)):
				maxList[i] = max(maxList[i],row[i])
	#print maxList
	#add the walkscore field
	if newfield not in allfield:
		arcpy.management.AddField(usng, newfield, "FLOAT")
		
	with arcpy.da.UpdateCursor(usng, atrList+[newfield]) as cursor:
		for row in cursor:
			row[-1] = 0
			for i in range(0,len(maxList)):
				#print row[i],maxList[i]
				val = float(row[i])/maxList[i]*25
				row[-1] = row[-1] + val
			cursor.updateRow(row)
		
if __name__ == '__main__':
	calWalk(None,["RES_DENS","LAND_MIX","RA_FLO_RA","INTER_DENS"],"WKSCORE")