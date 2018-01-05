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
import urllib

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

allCategoryUrls = ["https://www.opi.com/nail-products/nail-polish","https://www.opi.com/nail-products/gel", "https://www.opi.com/nail-products/long-wear", "https://www.opi.com/nail-products/dipping-powders", "https://www.opi.com/nail-products/acrylics", "https://www.opi.com/nail-care/hands-and-feet"]

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

browser = webdriver.Firefox(firefox_profile=firefox_profile)
#browser = webdriver.Firefox()
allProductsUrls=[]

for x in range(0, len(allCategoryUrls)):
	browser.get(allCategoryUrls[x])#open each product category page, which lists all prodcuts for each category
	with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
		jquery = jquery_js.read() #read the jquery from a file
		browser.execute_script(jquery) #active the jquery lib
		#keep clikcing 'show more +' button until it no longer exists.
		#browser.execute_script("function checkDisplay(){ var display = $('.btn-loadmore span:contains(SHOW MORE):nth(1)').css('display');if( display == 'block'){$('.btn-loadmore span:contains(SHOW MORE):nth(1)').click()}else{i = 100;} }for (var i = 0; i < 10; i++) { setTimeout(function(){ checkDisplay(); } , 1000);}")
		subPageHrefs = browser.execute_script("var allProductUrls = [];$('div.views-field-field-bottle-image a').each(function(){var href = $(this).attr('href');allProductUrls.push(href); });return allProductUrls;");
		#print subPageHrefs
		print len(subPageHrefs), ' subPageHrefs'
		for s in range(0, len(subPageHrefs)):
			allProductsUrls.append(subPageHrefs[s]);

allProductData=[]
alreadyScraped=[]
#with each product url stored in allProductUrls
#loop through each and collect all products
with open('alreadyScrapedProductUrls.json') as json_file:  
	alreadyScraped = json.load(json_file)

#open saved scraped data.
with open('storeScrapedData.json') as json_file:  
	allProductData = json.load(json_file)

with open('alreadyScrapedProductUrls.json') as json_file:  
	alreadyScrapedTemp = json.load(json_file)

#for x in range(0, len(alreadyScrapedTemp)):
	#alreadyScraped = alreadyScrapedTemp[x][ alreadyScrapedTemp[x].index('.com')+4: len(alreadyScrapedTemp[x]) ]

print 'alreadyScraped length ',len(alreadyScraped) 
print alreadyScraped

for x in range(0, len(allProductsUrls)):#Each page of results, all categories in one array
	
	url = urlparse.urljoin('http://www.opi.com', allProductsUrls[x])
	print 'url:::    ',url
	browser.get(url)
	
	if allProductsUrls[x] not in alreadyScraped:
		with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
			jquery = jquery_js.read() #read the jquery from a file
			browser.execute_script(jquery)
			print "Saving data"
			productName = browser.execute_script("return $('h1').text();");
			productUrl = url
			productPrice = browser.execute_script("return $('.price-info .price-box span.regular-price span.price').text();")
			productSku = browser.execute_script("var sku = $('.field-content:contains(CODE:)').text(); sku = sku.substring(sku.indexOf('CODE')+5, sku.length);return sku;");
			#productSku = browser.execute_script("return $('div.product-number span').text()")
			productImageSrc = browser.execute_script("return $('.product-photo img').attr('src');")
			#productImageSrc = rawImgHtml[rawImgHtml.index('background-image: url(&quot;')+28:rawImgHtml.index('&quot;);')]
			
			print 'productName:',productName
			print 'sku:',productSku
			print 'price:',productPrice
			print 'imgSrc:', productImageSrc
			#encoding for csv
			
			allProductData.append([productName, productUrl, productPrice, productSku, productImageSrc, 'opi']);
			alreadyScraped.append(allProductsUrls[x])
			with open('alreadyScrapedProductUrls.json', 'w') as outfile:  
				json.dump(alreadyScraped, outfile)
			with open('storeScrapedData.json', 'w') as outfile:  
				json.dump(allProductData, outfile)
	else:
		print 'already scraped!!!!!'


with open("opi.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(allProductData)
#browser.execute_script("$('#ContentPlaceHolder1_TextBoxDateFrom').click()")

browser.quit()
sys.exit()