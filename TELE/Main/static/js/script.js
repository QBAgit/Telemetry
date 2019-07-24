function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


/**
 * Create <span> with Bootstrap Grid based on data
 * from REST API
 * @param {url to fetch data i.e. '/api/v1/usersensors/'} rest_api_url 
 * @param {destination html element ID i.e. '#OptionSens'} span_id 
 * @param {list of objects defining collumns. i.e [{name:"ID",data_key:"id",class:"col-sm-3"}]} collumns 
 * @param {function name to handlle signle table row click event} click_handler
 */

function show_BordData(
    rest_api_url, 
    span_id,
    collumns,
    click_handler
    ){

    // GET data f REST API
    $.get(rest_api_url,function(data){
    console.log("Dupo Debug show_BordData:")
    console.log(data)

    // document element Container to fill with data
    var $main = $(span_id);
    $main.html(''); // Clear element

    var fDivTitles = $('<div>'); //Row Div container
    fDivTitles.addClass('row');

    // Header with collumn titles
    for(var i=0;i<collumns.length;i++){
        var colDiv = $('<div>');
        colDiv.addClass(collumns[i].class);
        colDiv.text(collumns[i].name);
        fDivTitles.append(colDiv)
    }

    // add to Container
    $main.append(fDivTitles);

    // Itterate with data - create rows
    for(var i=0;i<data.length;i++){
        var item = data[i];
        console.log(item);

        // Create Bootstrap Grid for single row
        var fDivMain = $('<div>');
        fDivMain.addClass('row');
        fDivMain.attr('sensor-id', item["id"]);
        fDivMain.click(click_handler);
        fDivMain.css('cursor','pointer');

        // Add collumns for current row
        for(var j=0;j<collumns.length;j++){
            var colDiv = $('<div>');
            colDiv.addClass(collumns[j].class);
            
            if(collumns[j].data_key === "value"){
                sensor_ID = item["id"]
                url = "api/v1/sensordata/"+sensor_ID+"/";
                $.get(url,function(data){
                    console.log(data);
                    // colDiv.text(data[0]);
                })
            }
            else{
                colDiv.text(item[collumns[j].data_key]);
            }

            fDivMain.append(colDiv);
        }

        // add to Container
        $main.append(fDivMain);
        }
      
    });
}


function show_DashBordData(){
    $(show_BordData(
        rest_api_url = '/api/v1/usersensors/',
        span_id = '#DashBordData',
        collumns = [
            {name:"Name",data_key:"name",class:"col-sm-3"},
            {name:"Description",data_key:"description",class:"col-sm-6"},
            {name:"Value",data_key:"value",class:"col-sm-3"},
        ],
        click_handler = DashBordClick
        ));
}


function show_OptionBordData(){
    $(show_BordData(
        rest_api_url = '/api/v1/usersensors/',
        span_id = '#OptionSens',
        collumns = [
            {name:"ID",data_key:"id",class:"col-sm-3"},
            {name:"Name",data_key:"name",class:"col-sm-3"},
            {name:"Description",data_key:"description",class:"col-sm-6"}
        ],
        click_handler = OptionClick
        ));
}


function sensupdate(){
    console.log("Dupo Debug sensupdate()")
    name = document.getElementById("sensorName").value;
    description = document.getElementById("sensorDescription").value;

    var csrftoken = getCookie('csrftoken');
        	
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type:"PUT",
        url:'/api/v1/usersensors/' + sensor_ID + '/',
        data:{
            'name': name,
            'description': description,
        },
        success: function(data){
            console.log("Dupo Debug sensupdate PUT AJAX data")
            console.log(data);
            $(show_OptionBordData());
            $("#SensOptModal").modal('hide')
        },
        error: function (jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        },
    });
}


function OptionClick(){
    console.log("Dupo Debug OptionClick")
    console.log($(this));
    sensor_ID = $(this).attr("sensor-id")
    console.log(sensor_ID)
    url = '/api/v1/usersensors/' + sensor_ID + '/'
    // get current sensor data:
    $.get(url,function(data){
        $("#sensorName").attr("placeholder",data["name"])
        $("#sensorDescription").attr("placeholder",data["description"])
    })

    $OptionsModal = $("#SensOptModal")
    $OptionsModal.modal()
    
}


function DashBordClick(){
    console.log("Dupo Debug DashBordClick")
    console.log($(this));
}


$(document).ready(function(){
    console.log("Siema zaczynamy")
    
    // Init
    dashbord = document.getElementById("DashBord").hidden = true;
    options = document.getElementById("Options").hidden = true;

    // Setup Callbacks
    $("#DashBord_Link").click(function(event){
        event.preventDefault()
        $Logo = $("#logo")[0].hidden = true;  
        $DashBord = $('#DashBord')[0].hidden = false;
        $Options = $('#Options')[0].hidden = true;
    
        // Change css for Dashbord parent container
        $Cont1 = $('#Cont1')
        $Cont1.removeClass("bg-1").addClass("bg-4")
    
        $(show_DashBordData());
    
    });

    $("#Options_Link").click(function(event){
        event.preventDefault()
        $Logo = $("#logo")[0].hidden = true;
        $DashBord = $('#DashBord')[0].hidden = true;false
        $Options = $('#Options')[0].hidden = false;
    
        // Change css for Dashbord parent container
        $Cont1 = $('#Cont1')
        $Cont1.removeClass("bg-1").addClass("bg-4")
    
        $(show_OptionBordData());
    
    });

    $("#sensor_update").click(sensupdate);
})


