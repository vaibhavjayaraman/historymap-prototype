function wikipedia_document_search() {
	//add a bunch of string processing that will allow people to not need exact article name.
	//first we should make it so that all Leading grammatical articles will not be used. 
    	var article = document.getElementById('wiki_doc_search').value;
	article = article.replace(/ /g,"_");
	var url = "https://en.wikipedia.org/w/api.php?action=query&prop=coordinates&origin=*&format=json&titles=" + article;
    	$.ajax({
		type: 'GET',
		url: url,
		datatype: "json",
		context: document.body,
		global: false,
		async: true, 
		crossdomain:true,
		success: function(data) {
			pages = data.query.pages;
			pageid = Object.keys(pages)[0]; //make create issues with multiple pages returned
			if (pageid == -1) {
				alert("The Page you request does not exist. Case sensitivity Matters. Capitalization Rules Matter. Spacing Matters");
			}
			else {
				page = pages[pageid];
				var title = page.title
				var coordinates = page.coordinates;
				console.log(page);
				article_ajax_call(WIKI_PAGE_ID_URL + pageid, title, "search");
				if (coordinates != null) {
					var lat = coordinates[0].lat;
					var lon = coordinates[0].lon;
					map.setView([lat, lon]);
					add_wiki_marker(lat, lon, pageid, title);
				}
				else {
					alert("No coordinates for this page. Perhaps try again by removing leading grammatical articles (for example The, A, etc. If you are looking for a person we are working on a feature that will allow you to seelocations that are associated with that person.)");
					//Show examples of places that are associated with this article once wikipedia deep search occurs and see if they want to go there
				}
			}
    		}
	});
}
