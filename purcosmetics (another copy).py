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
import json

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

browser = webdriver.Firefox()
allProductsUrls=[]

browser.get('https://www.purcosmetics.com/makeup/shop-all')#open each product category page, which lists all prodcuts for each category
with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
	jquery = jquery_js.read() #read the jquery from a file
	browser.execute_script(jquery) #active the jquery lib
	subPageHrefs = browser.execute_script("var allProductHrefs=[]; $('h2.product-name a').each(function(){ var href = $(this).attr('href'); allProductHrefs.push(href); }); return allProductHrefs;");
	#print subPageHrefs
	print len(subPageHrefs), ' subPageHrefs'
	for s in range(0, len(subPageHrefs)):
		allProductsUrls.append(subPageHrefs[s]);

#with each product url stored in allProductUrls
#loop through each and collect all products
allProductData=[]
alreadyScraped=[]
for x in range(0, len(allProductsUrls)):#Each page of results, all categories in one array
	url = allProductsUrls[x]
	print 'url:::    ',url
	browser.get(url)

	if 1 == 1:
		with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
			jquery = jquery_js.read() #read the jquery from a file
			browser.execute_script(jquery)
			print "Saving data"
			productName = browser.execute_script("var name = $('.product-name h2').text(); name = name.replace(/\s{2,}/g, ' '); return name;");
			print 'productName:',productName
			productUrl = url
			productPrice = browser.execute_script(" var price = $('.price-box span.price:first').text(); price = price.replace(/\s{2,}/g, ' '); return price;")
			productSku = 'none'
			#productSku = browser.execute_script("return $('div.product-number span').text()")
			rawImgHtml = browser.execute_script("return $('ul.product-image-gallery-images-slider li.product-image-gallery-images-img img').attr('src');")
			#productImageSrc = rawImgHtml[rawImgHtml.index('background-image: url(&quot;')+28:rawImgHtml.index('&quot;);')]
			productImageSrc = rawImgHtml
			print productImageSrc
			#encoding for csv
			productName = u' '.join((productName)).encode('utf-8').strip()
			productPrice =  u' '.join((productPrice)).encode('utf-8').strip()
			productSku =  u' '.join((productSku)).encode('utf-8').strip()
			allProductData.append([productName, productUrl, productPrice, productSku, productImageSrc, 'purcosmetics']);
			alreadyScraped.append(productUrl)
			with open('storeScrapedUrls.json', 'w') as outfile:  
				json.dump(alreadyScraped, outfile)

with open("bhcosmetics.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(allProductData)
#browser.execute_script("$('#ContentPlaceHolder1_TextBoxDateFrom').click()")

browser.quit()
sys.exit()