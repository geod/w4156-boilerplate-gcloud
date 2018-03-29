$("#startbutton").click(function() {
	$('html, body').animate({
	    scrollTop: $("#register-container").offset().top
	}, 350);
})

$("#register-button").click(function() {
	window.location.href = "listform/index.html"
})