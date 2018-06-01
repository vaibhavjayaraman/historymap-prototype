/**Removes wikipedia markers from map **/
function remove_wiki_markers() {
	wiki_markers.clearLayers();
}

/**Removes all markers from map */
function remove_markers(){
	/**As more sources come, add the calls for their removal here*/
	remove_wiki_markers();
}
