$(document).ready(function() {
	


	var host_id;
	var is_selected = false;
	var host_ip_addr;

	//Load host list 
	$.ajax({
		url: "host_list_html",
		data: {},
		type: "GET",
		dataType: "html",
		success: function(data) {
			$("#host_list").html(data);		
			singleSelection();
		},
		error: function() {
			alert("Load host list error :/");
		}
	});



	$("#add_host_btn").click(function(){
		$(this).prop("disabled","true");
		$.ajax({
			url: "add_host",
			data: {
				ip_param			: $("#ip_html").val(),
				hostname_param		: $("#hostname_html").val(),
				login_usr_param		: $("#login_usr_html").val(), 
				login_psd_param		: $("#login_psd_html").val(), 
				port_param			: $("#port_html").val(),
				distr_param			: $("#distr_html").val(), 
				note_param			: $("#note_html").val() 
			},
			type: "POST",
			dataType:"html",//html,json
			beforeSend: function() {
			},
			success: function(data) {
				$("#host_list").html(data);
				singleSelection();
				$("#add_host_btn").removeAttr('disabled');
			},
			error: function() {
				alert("Add host error");
			},
		});//ajax

	});//add_host_btn click

	



	//###### Find out which host to delete ######
	$("#delete_host_btn").click(function(){
		if(is_selected) {
			$("#host_to_delete").html(host_ip_addr);
			$("#delete_host_modal").modal('show');
		} else {
			alert("Select a host please : /");
		}
	});//delete_host_btn click

	$("#delete_cancel_btn").click(function(){
		cleanSelection();	
	});//delete_cancel_btn click

	//###### Process with delete ######
	$("#delete_confirm_btn").click(function(){
		$.ajax({
			url: "delete_host",
			data: {
				host_id_param:	host_id	
			},
			type: "POST",
			dataType: "html",
			beforeSend: function(){
				$("#delete_host_modal").modal('hide');
				$(".modal-backdrop.fade.in").remove()
			},	
			success: function(data){
				$("#host_list").html(data);
				singleSelection();
			},
			error: function(){
				alert("Error happened when deleting host");
			}
		});//ajax
	});//delete_confirm_btn click	
	



/*
	$("#modify_host_btn").click(function(){
		if(is_selected) {
			$("#modify_host_modal").modal('show');

			$.ajax({
				url: "host_modify_html",
				data: {},
				type: "GET",
				dataType: "html",
				beforeSend: function(){
				},
				success: function(data){
					$("#modify_host_modal_body").html(data);
				},
				error: function(){
					alert("Error happened when loading modify host html : /");
				}
		});//ajax
		} else {
			alert("Select a host please : /");
		}
	});//modify_host_btn click

	$("#modify_cancel_btn").click(function(){
		cleanSelection();	
	});
*/

	$("#verify_host_btn").click(function(){
		//determineSelected();
		$(this).prop("disabled","true");
		if(is_selected) {
			$("#verify_host_modal").modal('show');
			var loader_html = '<img src="image/loader.gif"></img>';
			$.ajax({
				url: "verify_host",
				data: {
					host_id_param: host_id
				},
				type: "POST",
				dataType: "html",
				beforeSend: function() {
					$("#verify_host_modal_body").html(loader_html);
				},
				success: function(data) {
					$("#verify_host_modal_body").html(data);
					$("#verify_host_btn").removeAttr('disabled');
				},
				error: function() {
					alert("Error happened when verifying host :/");
				}
			});//ajax

		} else {
			alert("Select a host please : /");
		}
	});//verify_host_btn click
	$("#verify_ok_btn").click(function(){
		cleanSelection();

		$.ajax({
			url: "host_list_html",
			data: {},
			type: "GET",
			dataType: "html",
			beforeSend: function() {},
			success: function(data) {
				$("#host_list").html(data);
				singleSelection();
			},
			error: function() {
				alert("Error happened when reloading host list");
			}
		});//ajax
	});

/*#########################################
######    ALL FUNCTIONS GO HERE   #########
######################################## */

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
