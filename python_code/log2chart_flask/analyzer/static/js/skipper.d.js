$(document).ready(function() {
    var is_selected = false;

    $.ajax({
        url:"load_raw",
        type:"GET",
        dataType:"html",
        beforeSend: function(){},
        success: function(data) {
            $("#fileList").html(data);
            single_selection();
            setup_navi();
        },
        error: function() {
            $("#fileList").html("Loading data error :/");
        }
    });



//########################################
//######    ALL FUNCTIONS GO HERE   ######
//########################################

	function clean_selection() {
		is_selected = false;
		$(":checkbox").removeAttr('checked');
	}
	
	//### Make sure only one checkbox is checked ###
	function single_selection() {
		$(':checkbox').each(function(){
			$(this).click(function(){
				if( $(this).prop("checked") ) {
					$(":checkbox").removeAttr('checked');
					$(this).prop('checked','true');
					is_selected = true;
					filename = $(this).val();
				} else {
					is_selected = false;
				}
			});//:checkbox click
		});//each
	}
    

    //##### setup navigation for different data analysis ######
    function setup_navi() {
        $(".analysis_menu a").click(function(){
            if(is_selected) {
                var atype = $(this).attr("id");
                var url = "/router/"+atype+"/"+filename;
                location.href = url;
            } else {
                alert("Choose any file please :/");
            }
        });
    }// setup_navi()


});//document ready
