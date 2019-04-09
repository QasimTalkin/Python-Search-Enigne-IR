var cars = [
	{ "make":"Porsche", "model":"911S" },
	{ "make":"Mercedes-Benz", "model":"220SE" },
	{ "make":"Jaguar","model": "Mark VII" }
];

window.onload = function() {
// drop down
	document.getElementById("theButton").onclick = function() {
		alert("Hello! !");
		doWork()
	};
	document.getElementById("search_submit").onclick = function() {
		var search_q = document.getElementById("search_q").value;
		alert("user input " + search_q);
	};
}

function doWork() {
	// ajax the JSON to the server
	$.post("receiver", JSON.stringify(cars), function(){

	});
	// stop link reloading the page
 event.preventDefault();
}
//SEARCH BAR
$('.search-input').focus(function(){
	$(this).parent().addClass('focus');
  }).blur(function(){
	$(this).parent().removeClass('focus');
	})
	


//Drop down options