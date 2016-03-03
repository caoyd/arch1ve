$(document).ready(function() {
    var is_selected = false;
    load_data();


//########################################
//######    ALL FUNCTIONS GO HERE   ######
//########################################

    function load_data() {
        $.ajax({
            url:"list",
            type:"GET",
            dataType:"html",
            beforeSend: function(){},
            success: function(data) {
                $("#logData").html(data);
                single_selection();
                setup_menu();
                setup_delete();
            },
            error: function() {
                $("#logData").html("Loading data error :/");
            }
        });
    }


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
    function setup_menu() {
        $("#menu a").click(function(){
            if(is_selected) {
                var atype = $(this).attr("id");
                var url = "/log2chart/renderer/"+filename+"/"+atype;
                location.href = url;
            } else {
                alert("Pick up 1 item :/");
            }
        });
    }// setup_menu()

    function setup_delete() {
        $(".dataTable a").click(function(){
            link = $(this).attr("href");

            $.ajax({
                url: link,
                type: "GET",
                beforeSend: function(){},
                success: function() {
                    load_data();
                },
                error: function(){}

            });//ajax

            return false;//disable link

        });//click
    }


});//document ready
