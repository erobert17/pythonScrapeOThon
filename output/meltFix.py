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
from numpy import genfromtxt

csvData = pe.get_array(file_name='meltcosmetics.csv') # done
#csvData = genfromtxt('meltcosmetics.csv', delimiter=',')

def removeSpaces(string):
	string = string.replace('  ','*-*')
	string = string.replace(' ','')
	string = string.replace('*-*', ' ')
	return string
allProductData = []
allProductData.append(['name', 'product url', 'price', 'sku','imgUrl','company']);
print len(csvData)
for x in xrange(0,len(csvData)):
	print x
	url = csvData[x][4]
	url = url[2:len(url)]
	if '.jpg' in csvData[x][4]:
		url = url[0:url.index('.jpg') +4]
		csvData[x][4] = url
	elif '.png' in csvData[x][4]:
		url = url[0:url.index('.png') +4]
		csvData[x][4] = url

	print csvData[x][4]


	name = csvData[x][0]
	name = removeSpaces(name)
	pUrl = csvData[x][1]
	price = csvData[x][2]
	sku = csvData[x][0]
	sku = sku.lower()
	sku = removeSpaces(sku)
	sku = sku.replace(' ','_')
	imgUrl = csvData[x][4]
	company = csvData[x][5]

	print 'name:',csvData[x][0]
	print 'pUrl:',csvData[x][1]
	print 'price:',csvData[x][2]
	print 'sku:',csvData[x][3]
	print 'imgUrl:',csvData[x][4]
	print 'company:',csvData[x][5]
	allProductData.append([name, pUrl, price, sku,imgUrl,company]);

with open("meltcosmetics2.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(allProductData)

sys.exit()