# !/usr/bin/env python
#  coding: utf-8
from datetime import datetime, timedelta
import sys
print sys.path
import re
import os
import urlparse
import csv
import json
import urllib


#browser = webdriver.Firefox()
allProductsUrls=[]


with open('storeData.json') as json_file:  
	data = json.load(json_file)

print len(data)

for x in range(0, len(data)):
	print data[x]

"""
with open("opi.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(allProductData)
"""

sys.exit()