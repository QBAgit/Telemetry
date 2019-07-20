function show_main(){
    // GET user data using REST API
    $.get('/api/v1/userfdata/',function(fdata){
        console.log("Dupo Debug Dashbord:")
        console.log(fdata)

        // document element Container to fill with data
        var $main = $('#DashBordData');
        $main.html(''); // Clear element

        var fDivTitles = $('<div>'); //Row Div container
        fDivTitles.addClass('row');

        var fDiv1 = $('<div>'); //Col Div container
        fDiv1.addClass('col-sm-3');
        fDiv1.text("Name");

        var fDiv2 = $('<div>'); //Col Div container
        fDiv2.addClass('col-sm-6');
        fDiv2.text("Description");

        var fDiv3 = $('<div>'); //Col Div container
        fDiv3.addClass('col-sm-3');
        fDiv3.text("Value");

        // add to Main Div
        fDivTitles.append(fDiv1,fDiv2,fDiv3);

        // add to Container
        $main.append(fDivTitles);

        // Itterate with data
        for(var i=0;i<fdata.length;i++){
            var f = fdata[i];

            // Create Bootstrap Grid
            var fDivMain = $('<div>'); //Row Div container
            fDivMain.addClass('row');

            var fDiv1 = $('<div>'); //Col Div container
            fDiv1.addClass('col-sm-3');
            fDiv1.text(f['name']);
            fDiv1.attr('fdata-id', f['id']);
            fDiv1.css('cursor','pointer');
            fDiv1.click(function(){
                // Action when single f data item clicked
                alert($(this))
            })

            var fDiv2 = $('<div>'); //Col Div container
            fDiv2.addClass('col-sm-6');
            fDiv2.text(f['description']);

            var fDiv3 = $('<div>'); //Col Div container
            fDiv3.addClass('col-sm-3');
            fDiv3.text(f['value']);

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
        $(show_main);

    })

    var $Options_Link = $("#Options_Link");
    $Options_Link.click(function(event){
        event.preventDefault()
        $Logo = $("#logo")[0].hidden = true;
        $DashBord = $('#DashBord')[0].hidden = true;false
        $Options = $('#Options')[0].hidden = false;
    })


})