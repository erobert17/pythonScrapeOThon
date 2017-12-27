

var allProductHrefs=[]
$('p.title a').each(function(){
	var href = $(this).attr('href');
	allProductHrefs.push(href);
})
