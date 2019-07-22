function show_BordData(
    rest_api_url, 
    span_id,
    collumn_names,
    data_keys,
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

    var fDiv1 = $('<div>'); //Col Div container
    fDiv1.addClass('col-sm-3');
    fDiv1.text(collumn_names.COL_1);

    var fDiv2 = $('<div>'); //Col Div container
    fDiv2.addClass('col-sm-3');
    fDiv2.text(collumn_names.COL_2);

    var fDiv3 = $('<div>'); //Col Div container
    fDiv3.addClass('col-sm-6');
    fDiv3.text(collumn_names.COL_3);

    // add to Main Div
    fDivTitles.append(fDiv1,fDiv2,fDiv3);

    // add to Container
    $main.append(fDivTitles);

    // Itterate with data
    for(var i=0;i<data.length;i++){
        var item = data[i];

        // Create Bootstrap Grid
        var fDivMain = $('<div>'); //Row Div container
        fDivMain.addClass('row');
        fDivMain.click(click_handler)

        var fDiv1 = $('<div>'); //Col Div container
        fDiv1.addClass('col-sm-3');
        fDiv1.text(item[data_keys.COL_1]);
        fDiv1.attr('data-id', item[data_keys.COL_1]);
        fDiv1.css('cursor','pointer');
        // fDiv1.click(click_handler)

        var fDiv2 = $('<div>'); //Col Div container
        fDiv2.addClass('col-sm-3');
        fDiv2.text(item[data_keys.COL_2]);

        var fDiv3 = $('<div>'); //Col Div container
        fDiv3.addClass('col-sm-6');
        fDiv3.text(item[data_keys.COL_3]);

        // add to Main Div
        fDivMain.append(fDiv1,fDiv2,fDiv3);

        // add to Container
        $main.append(fDivMain);
    }   
    });
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

        // Wywolanie
        $(show_BordData(
            rest_api_url = '/api/v1/usersensors/',
            span_id = '#DashBordData',
            collumn_names = {COL_1:"Name",COL_2:"Description",COL_3:"Value"},
            data_keys = {COL_1:"name",COL_2:"description",COL_3:"value"},
            click_handler = function(){
                console.log($(this))
            }
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

        // Wywolanie
        $(show_BordData(
            rest_api_url = '/api/v1/usersensors/',
            span_id = '#OptionSens',
            collumn_names = {COL_1:"ID",COL_2:"Name",COL_3:"Description"},
            data_keys = {COL_1:"id",COL_2:"name",COL_3:"description"},
            click_handler = function(){
                console.log($(this))
            }
            ));
    })
})