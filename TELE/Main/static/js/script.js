dashBoardChart = null

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

function show_BoardData(
    rest_api_url, 
    span_id,
    collumns,
    click_handler
    ){

    // GET data f REST API
    $.get(rest_api_url,function(data){

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

        // Create Bootstrap Grid for single row
        var fDivMain = $('<div>');
        fDivMain.addClass('row');
        fDivMain.attr('sensor-id', item["id"]);
        fDivMain.click(click_handler);
        fDivMain.css('cursor','pointer');
        fDivMain.mouseenter(function() {$(this).addClass("shadow")})
        fDivMain.mouseleave(function() {$(this).removeClass("shadow")})


        // Add collumns for current row
        for(var j=0;j<collumns.length;j++){
            var colDiv = $('<div>');
            colDiv.addClass(collumns[j].class);
            
            if(collumns[j].data_key === "value"){
                colDiv.text("no data");
                // add unique id i.e 'sens-id-4-val'
                colDiv.attr('id','sens-id-'+ item["id"]+'-val')

                sensor_ID = item["id"]
                url = "api/v1/sensordata/"+sensor_ID+"/";
                $.get(url,function(data){
                    if (data.length > 0){                   
                        idik = data[0].sensor
                        // get element by unique id
                        fresh_value = data[data.length-1].value
                        $val = $('#sens-id-'+ idik + '-val')                       
                        $val.text(fresh_value)
                    }

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


function show_DashBoardData(){
    $(show_BoardData(
        rest_api_url = '/api/v1/usersensors/',
        span_id = '#DashBoardData',
        collumns = [
            {name:"Name",data_key:"name",class:"col-sm-3"},
            {name:"Description",data_key:"description",class:"col-sm-6"},
            {name:"Value",data_key:"value",class:"col-sm-3"},
        ],
        click_handler = DashBoardClick
        ));
    
    var ctx = document.getElementById('myLineChart').getContext('2d');
    window.dashBoardChart = new Chart(ctx,{
        type: "line",
        color: "white",
        backgroundColor: "white",
        data: {
            // labels: [],
            datasets: [{
                // data: [],
                borderColor: "white",
                backgroundColor: "red",
                fill: false
            }],
        },
    });

}


function show_OptionBordData(){
    $(show_BoardData(
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


function sensdelete(){
    var csrftoken = getCookie('csrftoken');
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type:"DELETE",
        url:'/api/v1/usersensors/' + sensor_ID + '/',
        success: function(data){
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


function sensadd(){
        
    name = document.getElementById("NewSensorName").value;
    description = document.getElementById("NewSensorDescription").value;


    var csrftoken = getCookie('csrftoken');
        	
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type:"POST",
        url:'/api/v1/usersensors/',
        data:{
            'name': name,
            'description': description,
        },
        success: function(data){
            $(show_OptionBordData());
            $("#NewSensModal").modal('hide')
        },
        error: function (jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        },
    });

}


function OptionClick(){
    sensor_ID = $(this).attr("sensor-id")
    url = '/api/v1/usersensors/' + sensor_ID + '/'
    // get current sensor data:
    $.get(url,function(data){
        $("#sensorName").attr("placeholder",data["name"])
        $("#sensorDescription").attr("placeholder",data["description"])
    })

    $OptionsModal = $("#SensOptModal")
    $OptionsModal.modal()
    
}


function updateChart(chart, label, data){
    chart.data.labels = label;
    chart.data.datasets[0].data = data;
    chart.update();
}


function removeData(chart) {
    do{
        chart.data.labels.pop();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.pop();
        });
    } while (dashBoardChart.data.labels.length > 0);

    chart.update();
}

function plot(sensor_ID, from, to)
{
    if (from == "" && to == ""){
        url = "api/v1/sensordata/" + sensor_ID + "/";
    } else if (to == ""){
        url = "api/v1/sensordata/" + sensor_ID+"/" + "?from=" + from;
    } else if (from == ""){
        url = "api/v1/sensordata/" + sensor_ID+"/" + "?to=" + to;
    } else{
        url = "api/v1/sensordata/" + sensor_ID+"/" + "?from=" + from + "&to=" + to;
    }
    
    $.get(url,function(data){
        var mylabels = []
        var mydata = []
        data.forEach(x => mylabels.push(x.timestamp))
        data.forEach(x => mydata.push(x.value))

        updateChart(window.dashBoardChart,mylabels,mydata)
    })
}


function replotchart(){
    from = $('#FilterFrom').val()
    to = $('#FilterTo').val()
    sensor_ID = $('#myLineChart').attr("displayed-sensor-id")
    plot(sensor_ID, from, to)
    $('#ChartModModal').modal('hide')
}

function DashBoardClick(){
    sensor_ID = $(this).attr("sensor-id")
    // save current sesnor id as html attrubute
    $('#myLineChart').attr("displayed-sensor-id", sensor_ID)
    // plot sensor chart
    $(plot(sensor_ID));
    var sens = $(this).children()[1].textContent
    $("#ChartTitle").text(sens)

    // add settings button
    var $OptionButton = $("#ChartSettings");
    $OptionButton.html(''); // Clear element
    var button = $('<input type="button" value="Settings"/>');
    button.addClass("btn btn-default")
    button.attr('data-toggle','modal')
    button.attr('data-target','#ChartModModal')   
    $OptionButton.append(button)
    $('#chart_mod_title').text("Settings: " + sens)

}


$(document).ready(function(){
    console.log("Siema zaczynamy")
    
    // Init
    DashBoard = document.getElementById("DashBoard").hidden = true;
    options = document.getElementById("Options").hidden = true;

    // Setup Callbacks
    $("#DashBoard_Link").click(function(event){
        event.preventDefault()
        $Logo = $("#logo")[0].hidden = true;  
        $DashBoard = $('#DashBoard')[0].hidden = false;
        $Options = $('#Options')[0].hidden = true;
    
        // Change css for DashBoard parent container
        $Cont1 = $('#Cont1')
        $Cont1.removeClass("bg-1").addClass("bg-4")
    
        $(show_DashBoardData());
    
    });

    $("#Options_Link").click(function(event){
        event.preventDefault()
        $Logo = $("#logo")[0].hidden = true;
        $DashBoard = $('#DashBoard')[0].hidden = true;
        $Options = $('#Options')[0].hidden = false;
    
        // Change css for DashBoard parent container
        $Cont1 = $('#Cont1')
        $Cont1.removeClass("bg-1").addClass("bg-4")
    
        $(show_OptionBordData());
    
    });

    $("#sensor_update").click(sensupdate);
    $("#sensor_delete").click(sensdelete);
    $("#sensor_create").click(sensadd);
    $("#chart_mod").click(replotchart);

})