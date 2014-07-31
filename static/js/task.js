/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);

// they are not used in the stroop code but may be useful to you

// All pages to be loaded
var pages = [
	"form.html",
	"success.html"
];

psiTurk.preloadPages(pages);


/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
********************/

checkcodesuccess = function (bonus) {
	psiTurk.showPage('success.html');
	d3.select('#bonusamount').select(".bignumber").text('$'+bonus);
}

checkcodefail = function () {
	d3.select('.badcode').style("display","inline-block");
}

checkcode = function() {
	console.log("checking code");

	var parts = window.location.search.substr(1).split("&");
	var $_GET = {};
	for (var i = 0; i < parts.length; i++) {
	    var temp = parts[i].split("=");
	    $_GET[decodeURIComponent(temp[0])] = decodeURIComponent(temp[1]);
	}


	$.ajax({
		dataType: "json",
		type: "POST",
		data: {uniqueid: uniqueId, workerid: $_GET['workerId'], code: $("#completecode").val()},
		url: "/check_secret_code",
		success: function(data) {
			checkcodesuccess(data.bonus);
		},
		error: function () {
			checkcodefail();
		}
	});
}

completehit = function() {
	psiTurk.completeHIT();
}
// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
	// Load the stage.html snippet into the body of the page
	psiTurk.showPage('form.html');
	$('#myalert').on('click', function () {
		d3.select('.badcode').style("display","none");
	});

});
