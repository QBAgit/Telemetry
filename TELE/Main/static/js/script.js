function show_BordData(
    rest_api_url, 
    span_id,
    collumns,
    click_handler
    ){

    // example usage
    // rest_api_url = '/api/v1/usersensors/';
    // span_id = '#OptionSens'
    // collumn_names = {co1_1:"ID",col_2:"Name",col_3:"Description"}
    // data_keys = {co1_1:"id",col_2:"name",col_3:"description"}

    // GET data f REST API
    $.get(rest_api_url,function(data){
    console.log("Dupo Debug show_BordData:")
    console.log(data)

    // document element Container to fill with data
    var $main = $(span_id);
    $main.html(''); // Clear element

    var fDivTitles = $('<div>'); //Row Div container
    fDivTitles.addClass('row');

    for(var i=0;i<collumns.length;i++){
        var colDiv = $('<div>');
        colDiv.addClass(collumns[i].class);
        colDiv.text(collumns[i].name);
        fDivTitles.append(colDiv)
    }

    // add to Container
    $main.append(fDivTitles);

    // Itterate with data
    for(var i=0;i<=data.length;i++){
        var item = data[i];
        console.log(item);

            // Create Bootstrap Grid
        var fDivMain = $('<div>'); //Row Div container
        fDivMain.addClass('row');
        fDivMain.attr('sensor-id', item["id"]);
        fDivMain.click(click_handler);
        fDivMain.css('cursor','pointer');

        for(var j=0;j<collumns.length;j++){
            var colDiv = $('<div>');
            colDiv.addClass(collumns[j].class);
            colDiv.text(item[collumns[j].data_key]);
            fDivMain.append(colDiv)
        }

        // add to Container
        $main.append(fDivMain);
        }
      
    });
}

function OptionClick(){
    console.log("Dupo Debug OptionClick")
    console.log($(this));
}

function DashBordClick(){
    console.log("Dupo Debug DashBordClick")
    console.log($(this));
}

$(document).ready(function(){
    console.log("Siema zaczynamy")
    
    dashbord = document.getElementById("DashBord").hidden = true;
    options = document.getElementById("Options").hidden = true;

    var $Dashbord_link = $("#DashBord_Link");
    $Dashbord_link.click(function(event){
        event.preventDefault()
        $Logo = $("#logo")[0].hidden = true;  
        $DashBord = $('#DashBord')[0].hidden = false;
        $Options = $('#Options')[0].hidden = true;

        // Change css for Dashbord parent container
        $Cont1 = $('#Cont1')
        $Cont1.removeClass("bg-1").addClass("bg-4")

        $(show_BordData(
            rest_api_url = '/api/v1/usersensors/',
            span_id = '#DashBordData',
            collumns = [
                {name:"Name",data_key:"name",class:"col-sm-3"},
                {name:"Description",data_key:"description",class:"col-sm-6"},
            ],
            click_handler = DashBordClick
            ));
    })

    var $Options_Link = $("#Options_Link");
    $Options_Link.click(function(event){
        event.preventDefault()
        $Logo = $("#logo")[0].hidden = true;
        $DashBord = $('#DashBord')[0].hidden = true;false
        $Options = $('#Options')[0].hidden = false;

        // Change css for Dashbord parent container
        $Cont1 = $('#Cont1')
        $Cont1.removeClass("bg-1").addClass("bg-4")

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
    })
})