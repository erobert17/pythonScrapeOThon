

var allProductHrefs=[]
$('h2.product-name a').each(function(){
	var href = $(this).attr('href');
	allProductHrefs.push(href);
})
return allProductHrefs;

var allProductHrefs=[] $('h2.product-name a').each(function(){ var href = $(this).attr('href'); allProductHrefs.push(href); }); return allProductHrefs;


var name = $('.product-name h2').text(); name = price.replace(/\s{2,}/g, ' ');

var price = $('.product-shop .special-price span.price').text(); var price = price.replace(/\s{2,}/g, ' ');

var rawHtml = $('.zoomWindowContainer').html();var imgUrl =rawHtml.substring(rawHtml.indexOf('background-image: url(&quot;')+28,rawHtml.lastIndexOf("&quot;);")); return imgUrl;

"<div style="overflow: hidden; background-position: -568px -568px; text-align: center; 
background-color: rgb(255, 255, 255); width: 400px; height: 400px; float: left; 
background-size: 960px 960px; z-index: 100; border: 4px solid rgb(136, 136, 136); 
background-repeat: no-repeat; position: absolute; background-image: url(&quot;http://www.bhcosmetics.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/i/t/it_s_my_raye_raye_21_color_eyeshadow_-highlighter__contour_palette_hero_open.jpg&quot;); top: 0px; left: 480px; display: none;" class="zoomWindow jq_selected">&nbsp;</div>"