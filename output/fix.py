# !/usr/bin/env python
#  coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sys
print sys.path
import re
import os
import urlparse
import csv
import pyexcel as pe     # pip install pyexcel
import pyexcel.ext.xls   # pip install pyexcel-xls


csvData = pe.get_array(file_name="purcosmetics.csv") # done\

def removeSpaces(string):
	string = string.replace('  ','*-*')
	string = string.replace(' ','')
	string = string.replace('*-*', ' ')
	return string

allProductData = []
allProductData.append(['name', 'product url', 'price', 'sku','imgUrl','company']);
print len(csvData)
for x in xrange(0,len(csvData)):

	name = csvData[x][0]
	name = removeSpaces(name)
	pUrl = csvData[x][1]
	price = csvData[x][2]
	sku = csvData[x][3]
	if sku == 'none' or sku == 'n o n e':
		sku = name
		sku = sku.lower()
		sku = sku.replace(' ','_')
		sku = sku.replace('  ','_')
	sku = sku.replace(' ','')
	imgUrl = csvData[x][4]
	company = csvData[x][5]

	print 'name:',csvData[x][0]
	print 'pUrl:',csvData[x][1]
	print 'price:',csvData[x][2]
	print 'sku:',csvData[x][3]
	print 'imgUrl:',csvData[x][4]
	print 'company:',csvData[x][5]
	allProductData.append([name, pUrl, price, sku,imgUrl,company]);

with open("purcosmetics2.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(allProductData)

sys.exit()