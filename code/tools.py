import arcpy

	
def updateTable(shpfile,label,name,labeldict):
	print "updating %s with %s" %(shpfile,name)
	with arcpy.da.UpdateCursor(shpfile, [label,name]) as cursor:
		for row in cursor:
			if row[0] in labeldict:
				row[1] = labeldict[row[0]]
			cursor.updateRow(row)

			
def addFld(shpfile,name,type,precision,scale):
	exist = False
	for fld in arcpy.ListFields(shpfile):
		if fld.name == name:
			exist = True
	if exist == False:
		print "adding %s field to %s" % (name,shpfile)
		arcpy.management.AddField(shpfile, name, type,precision,scale)

		
def createMaping(shp1,shp2,joinFields):
	#joinFields = ['DOR_UC','NO_RES_UNT','landarea','TOT_LVG_AR','LABEL']
	##add all tables
	fldMapping = arcpy.FieldMappings()
	fldMapping.addTable(shp1)
	fldMapping.addTable(shp2)
	finalMappings = arcpy.FieldMappings()
	for fld in joinFields:
		fldIdx = fldMapping.findFieldMapIndex(fld)
		fldMp = fldMapping.getFieldMap(fldIdx)
		finalMappings.addFieldMap(fldMp)
	return finalMappings


def dor_to_int(dor):
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