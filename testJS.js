
var sku = $('.field-content:contains(CODE:)').text()
sku = sku.substring(sku.index('CODE')+5, sku.length);

var allProductUrls = [];
$('div.views-field-field-bottle-image a').each(function(){
	var href = $(this).attr('href');
	allProductUrls.push(href);
});


var allProductUrls = [];$('div.views-field-field-bottle-image a').each(function(){var href = $(this).attr('href');allProductUrls.push(href); });return allProductUrls;


function checkDisplay(){
	var display = $('.btn-loadmore span:contains(SHOW MORE):nth(1)').css('display');
	if( display == 'block'){
		$('.btn-loadmore span:contains(SHOW MORE):nth(1)').click()
	}else{
		console.log('display changed');
		i = 100;
	}
}


for (var i = 0; i < 10; i++) {
	setTimeout(function(){ 
		checkDisplay();
	 }, 1200);
}


function checkDisplay(){ var display = $('.btn-loadmore span:contains(SHOW MORE):nth(1)').css('display');if( display == 'block'){$('.btn-loadmore span:contains(SHOW MORE):nth(1)').click()}else{i = 100;} }for (var i = 0; i < 10; i++) {setTimeout(function(){ checkDisplay();}, 1000);}