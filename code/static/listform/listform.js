$("#startbutton").click(function() {
	$('html, body').animate({
	    scrollTop: $("#listing-container").offset().top
	}, 350);
})

$("#listing-button").click(function() {
	window.location.href = "listings/index.html"
})