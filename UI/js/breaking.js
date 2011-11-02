function fetchAndAppendNews(){
	console.log('fetching');
	$.getJSON("listOfNews.php", function(data) {
		console.log(data);
		breakingNewsToBeFetched = data.news.length;
		for(i = 0; i < data.news.length; i++) {
			console.log('fetchingNews' + data.news[i]);
			$("#makeMeScrollable").smoothDivScroll("addContent", 'proxy.php?id=' + data.news[i], "first");
		}
	});
}

$(function(){
	$("div#makeMeScrollable").smoothDivScroll({ 
		autoScroll: "onstart" , 
		autoScrollDirection: "endlessloopright", 
		autoScrollStep: 1, 
		autoScrollInterval: 15,	
		visibleHotSpots: "always"
	});
	fetchAndAppendNews();
});