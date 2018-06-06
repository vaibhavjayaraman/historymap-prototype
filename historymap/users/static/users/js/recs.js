/*These functions assume that corresponding variables are produced via a script element in html to which this file is attached to.
 */

function list_item_to_item_collab_filter() {
	console.log(current_user);
	if (current_user != null) {
		if (item_collab_filter == null) {
			item_collab_filter = "N/A. We are working on this feature right now!";
		}
		document.getElementById("item_collab_recs").innerHTML = 
			"People Who Viewed Articles You Viewed Also Viewed: " + item_collab_filter;
	}
}

list_item_to_item_collab_filter();
