$(document).ready(function() {

	var host_id;
	var is_selected = false;
	var host_ip_addr;

	//Load host list 
	$.ajax({
		url: "host_list_html",
		data: {
			filter_param : "yes"
		},
		type: "GET",
		dataType: "html",
		beforeSend: function(){},
		success: function(data) {
			$("#host_list").html(data);		
			singleSelection();
		},
		error: function() {
			alert("Load host list error :/");
		}
	});

	$("#probe_btn").click(function(){
		alert(host_id);
	});

	$("#state_btn").click(function(){
		alert("hi");
	});

/*############################################
#########  ALL FUNCTIONS GO HERE    ##########
/*##########################################*/

	function cleanSelection() {
		is_selected = false;
		$(":checkbox").removeAttr('checked');
	}
	//### Make sure only one checkbox is checked ###
	function singleSelection() {
		$(':checkbox').each(function(){
			$(this).click(function(){
				if( $(this).prop("checked") ) {
					$(":checkbox").removeAttr('checked');
					$(this).prop('checked','true');
					is_selected = true;
					host_id = $(this).val();
					//host_ip_addr = $(this).parent().parent().siblings(":first").html();
					host_ip_addr = $(this).parent().parent().siblings().first().html();
				} else {
					is_selected = false;
				}
			});//:checkbox click
		});//each
	}

});//document ready
