
import arcpy
import sys
from sets import Set

def DOR_UC_TO_INT(dor):
	rt = 0
	try:
		val = int(dor)
	except Exception:
		val=0
		print "can not process %s"%(dor)
		
	if val<=9:
		rt = 1
	elif val>9 and val<=39:
		rt = 2
	elif val >39 and val<=49:
		rt =3
	elif val >49 and val <=69:
		rt =4
	else:
		rt =5
	
	return rt
	

arcpy.env.overwriteOutput = True

##global variables
scratch = r"C:\\Users\\GIS_Tech\\Desktop\\Walkability\\ScratchWorkspace"


##references to input data
parcels = r"C:\\Users\\GIS_Tech\\Desktop\\Walkability\\InputData\\Leon_starterfile.shp"
roads = r"C:\\Users\\GIS_Tech\\Desktop\\Walkability\\InputData\\Street_segments.shp"
usng = r"C:\\Users\\GIS_Tech\\Desktop\\Walkability\\InputData\\USNG_Leon.shp"

##we neeed to get the Resdiential Density - number of residential =
##units per USNG cell / total land are zoned residential per USNG cell
##imprvoemnts to be made would be to divide the parcel area based on overlap with grid rather than just using the parcel centroid.
numResUnits = {}
areaOfParcels = {}
usngDict={}
usngAreaDict={}
usngResDict={}
##repair geometry of parcels
print "repairing geometry"
#arcpy.management.RepairGeometry(parcels)

##creat parcels centroids
print "converting parcels to centroids"
arcpy.management.FeatureToPoint(parcels, scratch+ "\\parcelcentroids.shp", "INSIDE")

##create field mappings
joinFields = ['DOR_UC','NO_RES_UNT','landarea','TOT_LVG_AR','LABEL']
##add all tables
fldMapping = arcpy.FieldMappings()
fldMapping.addTable(parcels)
fldMapping.addTable(usng)
finalMappings = arcpy.FieldMappings()
for fld in joinFields:
    fldIdx = fldMapping.findFieldMapIndex(fld)
    fldMp = fldMapping.getFieldMap(fldIdx)
    finalMappings.addFieldMap(fldMp)

##conducting spatial join, joinging usng grids to parcels centroids
print "usng joing to parcel centroids"
arcpy.analysis.SpatialJoin(scratch+ "\\parcelCentroids.shp", usng, scratch+ "\\parcelCentroidsSpatialJoin.shp", "JOIN_ONE_TO_ONE", "KEEP_ALL", finalMappings, "INTERSECT", "", "")

##
where = arcpy.AddFieldDelimiters(scratch+ "\\parcelCentroidsSpatialJoin.shp", 'DOR_UC')


where = arcpy.AddFieldDelimiters(scratch+ "\\parcelCentroidsSpatialJoin.shp", 'DOR_UC') + " in ('001','002','003','004','005','006','007','008','009')"
with arcpy.da.SearchCursor(scratch+ "\\parcelCentroidsSpatialJoin.shp", ['NO_RES_UNT','landarea','LABEL','DOR_UC'], where) as cursor:

            for row in cursor:
                if row[2] not in usngDict:
                    usngResDict[row[2]] = row[0]
                else:
                    usngResDict[row[2]] += row[0]

                if row[2] not in usngAreaDict:
                    usngAreaDict[row[2]] = row[1]
                else:
                    usngAreaDict[row[2]] += row[1] 
					
					
#land use mix
landUseMixDict = {}
with arcpy.da.SearchCursor(scratch+"\\parcelCentroidsSpatialJoin.shp",['LABEL','DOR_UC']) as cursor:
	for row in cursor:
		val = DOR_UC_TO_INT(row[1])
		#print row,row[0],row[1]
		if row[0] not in landUseMixDict:
			landUseMixDict[row[0]] = Set()
			landUseMixDict[row[0]].add(val)
		else:
			landUseMixDict[row[0]].add(val)
			
print "landUseMixDict", landUseMixDict

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

					
					
resFld = False
resNumFld = False
resAreaFld = False
landUseMix = False
totalLvg = False
for fld in arcpy.ListFields(usng):
	#print fld.name
	if fld.name == "RES_DENS":
		resFld = True
	if fld.name == "RES_UNT":
		resNumFld = True
	if fld.name == "RES_AREA":
		resAreaFld = True
	if fld.name == "LAND_MIX":
		landUseMix = True
	if fld.name == "RA_FLO_RA":
		totalLvg = True
#sys.exit(0)                        
print usngResDict
print ""
print usngAreaDict

##add field for Residential Density to usng
if resFld == False:
    print "adding residential density field to USNG"
    arcpy.management.AddField(usng, "RES_DENS", "DOUBLE", 6, 12)
if resNumFld == False:
	print "adding residential number field to USNG"
	arcpy.management.AddField(usng, "RES_UNT", "SHORT",4,0)
if resAreaFld == False:
	print "adding residential area field to USNG"
	arcpy.management.AddField(usng, "RES_AREA", "LONG",10,0)
if landUseMix == False:
	print "adding land use mix field to USNG"
	arcpy.management.AddField(usng, "LAND_MIX", "SHORT",4,0)
if totalLvg == False:
	print "adding ratail floor ratio field to USNG"
	arcpy.management.AddField(usng, "RA_FLO_RA", "DOUBLE",6,12)

print "updating USNG with residential density calculation"
with arcpy.da.UpdateCursor(usng, ['LABEL','RES_DENS','RES_UNT','RES_AREA','LAND_MIX','RA_FLO_RA']) as cursor:
	for row in cursor:
	
		if row[0] in usngResDict and row[0] in usngAreaDict:
			#if usngAreaDict(row[1]) in usngResDict:
			row[1] = usngResDict[row[0]]*10760000 / (usngAreaDict[row[0]] ) #transfer sqft to 1km sq 
			row[2] = int(usngResDict[row[0]])
			row[3] = usngAreaDict[row[0]]
			row[1] = row[2]*10760000/row[3]
			print usngAreaDict[row[0]],row[0],usngResDict[row[0]]
			
		if row[0] in landUseMixDict:
			row[4] = len(landUseMixDict[row[0]])
			
		if row[0] in totalLvgDict and row[0] in landAreaDict:
			row[5] = totalLvgDict[row[0]]*10760000/landAreaDict[row[0]]
			
		cursor.updateRow(row)




            

