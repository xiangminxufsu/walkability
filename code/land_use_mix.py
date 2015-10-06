import arcpy
import sys
import os
from sets import Set
from multiprocessing import Process, freeze_support

from line import linemain
from tools import DOR_UC_TO_INT,updateTable,addFld,createMaping
from calculate import calWalk

def cal_mix(usng,parcel,scratch):
	