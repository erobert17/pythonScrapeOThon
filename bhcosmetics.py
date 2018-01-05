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
import unicodedata

reload(sys)
sys.setdefaultencoding('utf8')

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

alreadyScraped=[]
allProductData=[]
#open array of all product urls
with open('storeScrapedUrls.json') as json_file:  
	alreadyScraped = json.load(json_file)

#open saved scraped data.
with open('storeScrapedData.json') as json_file:  
	allProductData = json.load(json_file)

rootCategories = ['http://www.bhcosmetics.com/eyes','http://www.bhcosmetics.com/brushes','http://www.bhcosmetics.com/face','http://www.bhcosmetics.com/lips','http://www.bhcosmetics.com/brows','http://www.bhcosmetics.com/studio-pro','http://www.bhcosmetics.com/accessories']
browser = webdriver.Firefox()

allProductsUrls=[]

for x in range(0, len(rootCategories)):
	print rootCategories[x]
	browser.get(rootCategories[x])#open each product category page, which lists all prodcuts for each category
	with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
		jquery = jquery_js.read() #read the jquery from a file
		browser.execute_script(jquery) #active the jquery lib
		subPageHrefs = browser.execute_script("var allProductHrefs=[];$('h2.product-name a').each(function(){ var href = $(this).attr('href'); allProductHrefs.push(href); }); return allProductHrefs; ");
		#print subPageHrefs
		print len(subPageHrefs), ' subPageHrefs'
		for s in range(0, len(subPageHrefs)):
			allProductsUrls.append(subPageHrefs[s]);

#with each product url stored in allProductUrls
#loop through each and collect all products

for x in range(0, len(allProductsUrls)):#Each page of results, all categories in one array
	url = allProductsUrls[x]
	print 'url:::    ',url
	delay = 5
	if url not in alreadyScraped:
		browser.get(url)
		with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
			jquery = jquery_js.read() #read the jquery from a file
			browser.execute_script(jquery)
			try:
				myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dddddaaaa')))
				#get product data
			except TimeoutException:
				print 'breadcrumb name not found'
			print "Saving data"
			#allHtmlFirst = browser.execute_script("return $('body').html();")
			allHtml = browser.page_source
			allHtml = allHtml[allHtml.index('<div itemprop="name">')+21:len(allHtml)]
			productName = allHtml[0:allHtml.index('</div>')]
			#productName = browser.execute_script("var name = $('div.breadcrumbs li.product').text(); name = name.replace(/\s{2,}/g, ' '); return name;")
			productName = ' '.join(productName.split())
			print 'productName:',productName
			productName = name.replace('&amp', ' and ')
			productName = name.replace(',', '')
			productUrl = url
			productPrice = browser.execute_script("var price =  $('.product-shop .special-price span.price').text(); price = price.replace(/\s{2,}/g, ' '); return price;")
			productPrice = ' '.join(productPrice.split())
			productSku = 'none'
			#productSku = browser.execute_script("return $('div.product-number span').text()")
			rawImgHtml = browser.execute_script("var rawHtml = $('.zoomWindowContainer').html();var imgUrl =rawHtml.substring(rawHtml.indexOf('background-image: url(&quot;')+28,rawHtml.lastIndexOf('&quot;);')); return imgUrl;")
			#productImageSrc = rawImgHtml[rawImgHtml.index('background-image: url(&quot;')+28:rawImgHtml.index('&quot;);')]
			productImageSrc = rawImgHtml
			print productImageSrc
			#encoding for csv
			productName = productName.encode('ascii', 'ignore').decode('ascii')
			productPrice =  productPrice.encode('ascii', 'ignore').decode('ascii')
			productSku =  productSku.encode('ascii', 'ignore').decode('ascii')
			allProductData.append([productName, productUrl, productPrice, productSku, productImageSrc, 'bhcosmetics']);
			alreadyScraped.append(productUrl)
			with open('storeScrapedUrls.json', 'w') as outfile:  
				json.dump(alreadyScraped, outfile)
			with open('storeScrapedData.json', 'w') as outfile:  
				json.dump(allProductData, outfile)

with open("bhcosmetics.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(allProductData)
#browser.execute_script("$('#ContentPlaceHolder1_TextBoxDateFrom').click()")

browser.quit()
sys.exit()