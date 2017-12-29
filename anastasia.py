# !/usr/bin/env python
#  coding: utf-8
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from selenium import webdriver
from datetime import datetime, timedelta
import sys
print sys.path
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import re
import os
import urlparse
import csv


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def extract_between(text, sub1, sub2, nth=1):
    """
    extract a substring from text between two given substrings
    sub1 (nth occurrence) and sub2 (nth occurrence)
    arguments are case sensitive
    """
    #  prevent sub2 from being ignored if it's not there
    if sub2 not in text.split(sub1, nth)[-1]:
        return None
    return text.split(sub1, nth)[-1].split(sub2, nth)[0]

rootCategories = ['http://www.anastasiabeverlyhills.com/holiday-2017/','http://www.anastasiabeverlyhills.com/best-sellers/','http://www.anastasiabeverlyhills.com/brows/','http://www.anastasiabeverlyhills.com/makeup/','http://www.anastasiabeverlyhills.com/brushes-and-tools/', 'http://www.anastasiabeverlyhills.com/more/']
browser = webdriver.Firefox()

pagigationLinks=[]

for x in range(0, len(rootCategories)):

	browser.get(rootCategories[x])
	#title = browser.execute_script("$('title').text();")
	with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
		jquery = jquery_js.read() #read the jquery from a file
		browser.execute_script(jquery) #active the jquery lib
		subPageHrefs = browser.execute_script("var subPageHrefs=[];$('.pagination li a').each(function(){var href = $(this).attr('href');subPageHrefs.push(href);});return subPageHrefs;");
		print len(subPageHrefs), ' subPageHrefs'
		print subPageHrefs
		for s in range(0, len(subPageHrefs)):
			pagigationLinks.append(subPageHrefs[s]);

#with pagigation urls for each category saved in
#loop through each and collect all products
allProductData=[]
for x in range(0, len(pagigationLinks)):#Each page of results, all categories in one array
	browser.get(pagigationLinks[x])
	with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
		thisPagesProductUrls = browser.execute_script("var allProductUrls=[];$('.product-name a.name-link').each(function(){ var productUrl = $(this).attr('href'); allProductUrls.push(productUrl); }); return allProductUrls;")
		for p in range(0, len(thisPagesProductUrls)):
			print 'Opening ', thisPagesProductUrls[p]
			url = urlparse.urljoin('http://www.anastasiabeverlyhills.com', thisPagesProductUrls[p])
			browser.get(url);
			#get product data
			productName = browser.execute_script("return $('h1.product-name').text();")
			productUrl = url
			productPrice = browser.execute_script("return $('#product-content span.price-sales').text();")
			productSku = browser.execute_script("return $('div.product-number span').text()")
			productImageSrc = browser.execute_script("var ttt = $('a.product-image.main-image img.zoomImg').attr('src'); return ttt;")
			#encoding for csv
			productName = u' '.join((productName)).encode('utf-8').strip()
			productPrice =  u' '.join((productPrice)).encode('utf-8').strip()
			productSku =  u' '.join((productSku)).encode('utf-8').strip()
			allProductData.append([productName, productUrl, productPrice, productSku, productImageSrc, 'anastasiabeverlyhills']);

with open("anastasiabeverlyhills.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(allProductData)
#browser.execute_script("$('#ContentPlaceHolder1_TextBoxDateFrom').click()")

browser.quit()
sys.exit()