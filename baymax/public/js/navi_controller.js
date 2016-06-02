$(document).ready(function() {
	$("#navi li").each(function(){
		$(this).click(function(){
			$(this).addClass("active").siblings().removeClass("active");
		});
	});

	$("#loader").hide();

	//Host Info
	$("#host_probe_nav").click( function(){ loadHTML("host_probe_html") });

	//Remote Command 
	$("#remote_command_nav").click( function(){ loadHTML("remote_command_html") });

	//Host Management 
	$("#host_mng_nav").click( function(){loadHTML("host_mng_html")});

});//document ready


//###### Function used to load html ######
function loadHTML(uri) {
	var loader_html = '<img src="image/loader.gif"></img>';

	$.ajax({
		url: uri,
		data: {},
		type: "GET",
		dataType:"html",
		beforeSend: function() {
			$("#right_content").html(loader_html);
		},
		success: function(data) {
			$("#right_content").html(data);
		},
		error: function() {
			alert("Error loading uri page");
		},
		complete: function() {
			//nothing
		}
	});//ajax
}
