$(document).ready(function() {
    var is_selected = false;

    load_raw_data();




//########################################
//######    ALL FUNCTIONS GO HERE   ######
//########################################
//
    function load_raw_data() {
        $.ajax({
            url:"list_raw",
            type:"GET",
            dataType:"html",
            beforeSend: function(){},
            success: function(data) {
                $("#rawList").html(data);
                single_selection();
                setup_navi();
                setup_delete();
            },
            error: function() {
                $("#rawList").html("Loading data error :/");
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
                    $("#info").html("");
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
    
    function setup_delete() {
        $(".rawTable a").click(function(){
            link = $(this).attr("href"); 

            $.ajax({
                url: link,
                type: "GET",
                beforeSend: function(){},
                success: function() {
                    load_raw_data();
                },
                error: function() {
                }
                
            });//ajax

            return false;//disable link
        });//click
    }//setup_delete()


    //##### setup navigation for different data analysis ######
    function setup_navi() {
        $("#rawProcBtn").click(function(){
            if(is_selected) {
                ptype = $("#typeSel").val()

                ajaxURL = "process/"+ptype+"/"+filename
                $.ajax({
                    url:ajaxURL,
                    type:"GET",
                    dataType:"html",
                    beforeSend: function() {
                        $("#info").html("Processing "+ filename)
                    },
                    success: function(data) {
                        $("#info").html(data);
                        //single_selection();
                        //setup_navi();
                    },
                    error: function() {
                        $("#info").html("Error in processing raw data :/");
                    }
                });


                //var atype = $(this).attr("id");
                //var url = "/router/"+atype+"/"+filename;
                //location.href = url;
            } else {
                alert("Pick up 1 item :/");
            }
        });
    }// setup_navi()

});//document ready
