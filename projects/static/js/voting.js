/*
Helper Functions
================
*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/*
Project Voting Methods
======================
*/
const UPVOTE_URL = "/project/<id>/up";
const DOWNVOTE_URL = "/project/<id>/down";

$(".upvote-button").click(function(evt) {
	var project = $(evt.target).parents(".project");
	console.log(project)
	var projectid = $(project).data("id");

	// Prepare Ajax Request
	var url = UPVOTE_URL.replace("<id>", projectid);
	var csrf = getCookie('csrftoken');
	var req = new XMLHttpRequest
	$.ajax({
		url: url, 
		headers: {
			'X-CSRFToken': csrf
		},
		method: 'POST'
	}).done(function(data) {
		if(data == "Success") {
			console.log("Successfully upvoted!");
			$(project).find(".upvote-button").addClass("mdl-button--colored");
			$(project).find(".downvote-button").removeClass("mdl-button--colored");
		} else {
			display_error("Could not upvote");
		}
	});
});
$(".downvote-button").click(function(evt) {
	var project = $(evt.target).parents(".project");
	var projectid = $(project).data("id");

	// Prepare Ajax Request
	var url = DOWNVOTE_URL.replace("<id>", projectid);
	var csrf = getCookie('csrftoken');
	var req = new XMLHttpRequest
	$.ajax({
		url: url, 
		headers: {
			'X-CSRFToken': csrf
		},
		method: 'POST'
	}).done(function(data) {
		if(data == "Success") {
			console.log($(project).children(".downvote-button"));
			$(project).find(".downvote-button").addClass("mdl-button--colored");
			$(project).find(".upvote-button").removeClass("mdl-button--colored");
			console.log("Successfully downvoted!");
		} else {
			display_error("Could not downvote");
		}
	});
});

function display_error(msg) {
	var data = {
		message: msg
	};
	document.querySelector("#toast-error-message").MaterialSnackbar.showSnackbar(data)
}