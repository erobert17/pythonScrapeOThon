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

rootCategories = ['https://www.meltcosmetics.com/collections/new','https://www.meltcosmetics.com/collections/gift-ideas','https://www.meltcosmetics.com/collections/liquid-lipsticks','https://www.meltcosmetics.com/collections/lips','https://www.meltcosmetics.com/collections/pencils', 'https://www.meltcosmetics.com/collections/highlight', 'https://www.meltcosmetics.com/collections/stacks', 'https://www.meltcosmetics.com/collections/accessories']
browser = webdriver.Firefox()

allProductsUrls=[]

for x in range(0, len(rootCategories)):

	browser.get(rootCategories[x])
	#title = browser.execute_script("$('title').text();")
	with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
		jquery = jquery_js.read() #read the jquery from a file
		browser.execute_script(jquery) #active the jquery lib
		subPageHrefs = browser.execute_script("var allProductHrefs=[];$('p.title a').each(function(){var href = $(this).attr('href');allProductHrefs.push(href);});return allProductHrefs;");
		print len(subPageHrefs), ' subPageHrefs'
		for s in range(0, len(subPageHrefs)):
			allProductsUrls.append(subPageHrefs[s]);

#with each product url stored in allProductUrls
#loop through each and collect all products
allProductData=[]
for x in range(0, len(allProductsUrls)):#Each page of results, all categories in one array
	url = urlparse.urljoin('https://www.meltcosmetics.com/', allProductsUrls[x])
	print url
	browser.get(url)
	with open('jquery-3.1.0.min.js', 'r') as jquery_js: 
		jquery = jquery_js.read() #read the jquery from a file
		browser.execute_script(jquery)
		#get product data
		productName = browser.execute_script("return $('.page-title').text();")
		productUrl = url
		productPrice = browser.execute_script("return $('span.actual-price.money').text();")
		productSku = 'none'
		#productSku = browser.execute_script("return $('div.product-number span').text()")
		productImageSrc = browser.execute_script("return $('.photos a.photo.active img').attr('src');")
		#encoding for csv
		productName = u' '.join((productName)).encode('utf-8').strip()
		productPrice =  u' '.join((productPrice)).encode('utf-8').strip()
		productSku =  u' '.join((productSku)).encode('utf-8').strip()
		allProductData.append([productName, productUrl, productPrice, productSku, productImageSrc, 'meltcosmetics']);


with open("meltcosmetics.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(allProductData)
#browser.execute_script("$('#ContentPlaceHolder1_TextBoxDateFrom').click()")

browser.quit()
sys.exit()