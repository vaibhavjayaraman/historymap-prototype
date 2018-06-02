function change_opacity() {
	var potential_opacity = document.getElementById("opacity_change").value;
	if (!isNaN(potential_opacity)) {
		if (0 < Number(potential_opacity) && Number(potential_opacity) <= 1) {
			opacity = Number(potential_opacity);
			change_year();
		}
		else {
			alert("Enter a Number Between 0 and 1 and resubmit");
		}
	} else {
		alert("Enter a Number Between 0 and 1 and resubmit");
	}
}

function change_wiki_range() {
	var change_range = document.getElementById("wiki_search_range_change").value;
	if (!isNaN(change_range)) {
		if (10 < Number(change_range) && Number(change_range) < 10000) {
			wiki_geo_search_radius = Number(change_range);
		}
		else {
			alert("Enter a Number Between 10 and 10000 and resubmit");
		}
	} else {
		alert("Enter a Number Between 10 and 10000 and resubmit");
	}
}
