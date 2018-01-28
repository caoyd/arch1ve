$(document).ready(function(){
    var url = window.location.pathname;
    var arr = url.split("/");
    var atype,filename,ajaxURL;

    filename = arr[3];
    atype = arr[4];
    ajaxURL = "/log2chart/chart/"+filename+"/"+atype;

    $.ajax({
        url: ajaxURL, 
        type: "GET",
        dataType: "html",
        beforeSend: function() {
            $("#container").html('<span style="font-family:Georgia;font-size:20px;color:#1B58B8;">Loading...</span>');
        },

        success: function(chart) {
            $("#container").html(chart);
        },

        error: function() {
            //alert("Error :/");
            //location.href = "/analyzer_index";
        }
    });//ajax
});

