import arcpy
import sys
import os

arcpy.env.overwriteOutput = True
##global variables
scratch = r"C:\\Users\\GIS_Tech\\Desktop\\Walkability\\ScratchWorkspace"


##references to input data
parcels = r"C:\\Users\\GIS_Tech\\Desktop\\Walkability\\InputData\\Leon_starterfile.shp"
roads = r"C:\\Users\\GIS_Tech\\Desktop\\Walkability\\InputData\\Street_segments.shp"
usng = r"C:\\Users\\GIS_Tech\\Desktop\\Walkability\\InputData\\USNG_Leon.shp"
unsplitRd = scratch+"\\streets_unsplit.shp"

arcpy.UnsplitLine_management(roads, unsplitRd,["NAME"])
