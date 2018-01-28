$(document).ready(function() {

	$("#host_probe_btn").click(function(){
		$(this).prop("disabled","true");
		var loader_html = '<img src="image/loader.gif"></img>';
		$.ajax({
			url: "probe_host_info",
			data: {
				ip_param		: $("#ip_html").val(),
				login_usr_param		: $("#login_usr_html").val(), 
				login_psd_param		: $("#login_psd_html").val(), 
				port_param		: $("#port_html").val() 
			},
			type: "POST",
			dataType:"json",
			beforeSend: function() {
				$("#info").html(loader_html);
			},
			success: function(data) {
				var i=0;
				var tb='<table class="table table-striped">';
				$.each(data,function(k,v) {
					if(i%2) {
						tb += "<tr class='success'><td>"+k+"</td><td>"+v+"</td></tr>";
					} else {
						tb += "<tr><td>"+k+"</td><td>"+v+"</td></tr>";
					}
					i++;
				});
				tb +="</table>";
				
				$("#info").html(tb);
				$("#host_probe_btn").removeAttr('disabled');
			},
			error: function() {
				alert("Something must be wrong:\nInput error ?\nSession timeout ?");
			},
			complete: function(){}
		});//ajax
	});//click

});//document ready
