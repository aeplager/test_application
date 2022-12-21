function StateUSAFGetInfo(){
    try{
        current_state = $( "#selState option:selected" ).text();
        urlMain = "/api_solarmodel/return_USAF?state=" + current_state         
        var ResultData = general_return_json_api(urlMain);
        var USAF_StationNames = [];
        for (var i in ResultData) {
            USAF_StationNames.push(ResultData[i].SelectorText);                
            }
        USAFautocomplete(document.getElementById("StationName"), USAF_StationNames); 
    } catch (e) {
        general_error(e);
    }
}
function SolarDealGetInfo(){
    try{
        var SolarDealID = $('#selDealName').val();
        urlMain = '/api_solarmodel/return_all?stored_procedure=[Solar].[DealGetInfo] @DealID = ' + SolarDealID
        var ResultData = general_return_json_api(urlMain);
        var ResultData_sel = ResultData[0];
        $('#txtDealName').val(ResultData_sel.DealName);
        $('#selState').val(ResultData_sel.StateAbbid);
        $('#StationName').val(ResultData_sel.USAFName);
        $('#selMarket').val(ResultData_sel.MarketID);
        $('#selSettlementPoint').val(ResultData_sel.SettlementPointID);
        $('#selSettlementZone').val(ResultData_sel.SettlementLocationID);                      
        $('#startdate').val(ResultData_sel.StartDateString);
        $('#enddate').val(ResultData_sel.EndDateString);
        var FirmContin = ResultData_sel.FirmContingent;                
        document.querySelector('input[name=FirmContinRadio][value=FirmValue]').checked = true;
        if (FirmContin.toLowerCase() == "c") {
            document.querySelector('input[name=FirmContinRadio][value=ContingentValue]').checked = true;                                        
        } 
        $('#txtCapacityFactor').val(ResultData_sel.CapacityFactor);
        $('#txtDiscountFactor').val(ResultData_sel.DiscountRate);
        $('#txtCapacity').val(ResultData_sel.Capacity);       
        // Change Graph
        urlMain = '/api_solarmodel/return_all?stored_procedure=[Solar].[ClearGraphInfo] @DealID=' + SolarDealID;
        ResultData = general_return_json_api(urlMain);
        SolarChangeDeal();
        } catch (e) {
        general_error(e);
    }
}
function SolarDealNewDeal(){
    try{
        $('#selDealName').val(0);
        $('#txtDealName').val("");
        $('#txtDealName').text("");
        //$('#selState').val(45);
        //StateUSAFGetInfo();
        //$('#StationName').val("");
        //$('#StationName').text("");
        //$('#selMarket').val(1);
        $('#selSettlementPoint').val(0);
        $('#selSettlementZone').val(0);
        var StartDateString = "2021-05-01"
        var EndDateString = "2022-05-01"
        $('#startdate').val(StartDateString);
        $('#enddate').val(EndDateString);
        document.querySelector('input[name=FirmContinRadio][value=FirmValue]').checked = true;
        $('#txtCapacityFactor').val(0);
        $('#txtDiscountFactor').val(0);
        $('#txtCapacity').val(0);          
        solarmodel_draw_chart();
    } catch (e) {
        general_error(e);
    }
}
function SolarClearGraphInfo(){
    try{
        var deal_id = 0
        if (deal_id == null) {deal_id = 0;}
        urlMain = '/api_solarmodel/change_deal?deal_id=' + deal_id
        var ResultData = general_return_json_api(urlMain);        
        solarmodel_draw_chart();
    } catch (e) {
        general_error(e);
    }       
}
function SolarChangeDeal(){
    try {
        var deal_id = $('#selDealName').val();
        if (deal_id == null) {deal_id = 0;}
        // urlMain = '/api_solarmodel/change_deal?deal_id=' + deal_id
        // var ResultData = general_return_json_api(urlMain);           
        urlMain = '/api_solarmodel/return_all?stored_procedure=[Solar].[DealGetInfo] @DealID = ' + deal_id
        var ResultData = general_return_json_api(urlMain);
        var ResultData_sel = ResultData[0];
        $('#txtDealName').val(ResultData_sel.DealName);
        $('#selState').val(ResultData_sel.StateAbbid);
        //$('#StationName').val(ResultData_sel.USAFName);
        //$('#selMarket').val(ResultData_sel.MarketID);
        $('#selSettlementPoint').val(ResultData_sel.SettlementPointID);
        $('#selSettlementZone').val(ResultData_sel.SettlementLocationID);                      
        $('#startdate').val(ResultData_sel.StartDateString);
        $('#enddate').val(ResultData_sel.EndDateString);
        var FirmContin = ResultData_sel.FirmContingent;                
        document.querySelector('input[name=FirmContinRadio][value=FirmValue]').checked = true;
        if (FirmContin.toLowerCase() == "c") {
            document.querySelector('input[name=FirmContinRadio][value=ContingentValue]').checked = true;                                        
        } 
        $('#txtCapacityFactor').val(ResultData_sel.CapacityFactor);
        $('#txtDiscountFactor').val(ResultData_sel.DiscountRate);
        $('#txtCapacity').val(ResultData_sel.Capacity);       
        // Change Graph
        // urlMain = '/api_solarmodel/return_all?stored_procedure=[Solar].[ClearGraphInfo] @DealID=' + SolarDealID;
        // ResultData = general_return_json_api(urlMain);
        solarmodel_draw_chart();
        alertify.success("Chart Updated");

    } catch (e) {
        general_error(e);
    } 
}
function SolarChangeDeal(){
    try{
        var deal_id = $('#selDealName').val();
        if (deal_id == null) {deal_id = 0;}
        // urlMain = '/api_solarmodel/change_deal?deal_id=' + deal_id
        // var ResultData = general_return_json_api(urlMain);           
        urlMain = '/api_solarmodel/return_all?stored_procedure=[Solar].[DealGetInfo] @DealID = ' + deal_id
        var ResultData = general_return_json_api(urlMain);
        var ResultData_sel = ResultData[0];
        $('#txtDealName').val(ResultData_sel.DealName);
        $('#selState').val(ResultData_sel.StateAbbid);
        $('#StationName').val(ResultData_sel.USAFName);
        $('#selMarket').val(ResultData_sel.MarketID);
        $('#selSettlementPoint').val(ResultData_sel.SettlementPointID);
        $('#selSettlementZone').val(ResultData_sel.SettlementLocationID);                      
        $('#startdate').val(ResultData_sel.StartDateString);
        $('#enddate').val(ResultData_sel.EndDateString);
        var FirmContin = ResultData_sel.FirmContingent;                
        document.querySelector('input[name=FirmContinRadio][value=FirmValue]').checked = true;
        if (FirmContin.toLowerCase() == "c") {
            document.querySelector('input[name=FirmContinRadio][value=ContingentValue]').checked = true;                                        
        } 
        $('#txtCapacityFactor').val(ResultData_sel.CapacityFactor);
        $('#txtDiscountFactor').val(ResultData_sel.DiscountRate);
        $('#txtCapacity').val(ResultData_sel.Capacity);       
        // Change Graph
        // urlMain = '/api_solarmodel/return_all?stored_procedure=[Solar].[ClearGraphInfo] @DealID=' + SolarDealID;
        // ResultData = general_return_json_api(urlMain);
        solarmodel_draw_chart();
        alertify.success("Chart Updated");

    } catch (e) {
        general_error(e);
    }
}
function SolarDealSaveDeal(){
    try{ 
        var start_date = new Date();
        var urlMain ="/api_solarmodel/update_test?"        
        var deal_id = $('#selDealName').val(); 
        var bl_new_deal = 0;
        if (deal_id == 0){ bl_new_deal=1; }
        urlMain = urlMain + "deal_id=" + deal_id;        
        urlMain = urlMain + "&deal_name=" + $('#txtDealName').val();
        urlMain = urlMain + "&deal_id=" + $('#selState').val();
        urlMain = urlMain + "&set_point_id=" + $('#selSettlementPoint').val();
        urlMain = urlMain + "&set_loc_id=" + $('#selSettlementZone').val();
        urlMain = urlMain + "&start_date=" + $('#startdate').val();
        urlMain = urlMain + "&end_date=" + $('#enddate').val();
        var FirmCont = document.querySelector('input[name=FirmContinRadio][value=FirmValue]').checked ;
        if (FirmCont == true){
            FirmCont = "Firm";
        } else {
            FirmCont = "Cont";
        }
        urlMain = urlMain + "&firm_cont=" + FirmCont;
        //document.querySelector('input[name=FirmContinRadio][value=FirmValue]').checked = true;
        urlMain = urlMain + "&cap_factor=" +  $('#txtCapacityFactor').val();
        urlMain = urlMain + "&disc_rate=" +  $('#txtDiscountFactor').val();
        urlMain = urlMain + "&capacity=" +  $('#txtCapacity').val();  
        var ResultData = general_return_json_api(urlMain);
        alertify.success(ResultData.Status)
        //alertify.success("Total Time to save in seconds took:  " + seconds);            
        start_date = new Date();        
        deal_id = ResultData[0].DealID; 
        name_change = ResultData[0].NameChange;         
        if (bl_new_deal==1){
            // Reselect Deal and Run Through            
            var end_date = new Date();
            // Refill the Selector
            urlMain = '/api_solarmodel/return_all?stored_procedure=[Solar].[DealGetInfo]'            
            general_fill_selector('selDealName',urlMain,'New Deal');                               
            $('#selDealName').val(deal_id);
            solarmodel_draw_chart(); 
            
        } else{            
            if (name_change=="YES") {
                urlMain = '/api_solarmodel/return_all?stored_procedure=[Solar].[DealGetInfo]'            
                general_fill_selector('selDealName',urlMain,'New Deal');                               
                $('#selDealName').val(deal_id);    
                SolarChangeDeal();                
            } else{
                solarmodel_draw_chart();   
            }            
        }        
        
        //seconds = Math.abs(start_date - end_date) / 1000;
        //alertify.success("Total Time to reselect save in seconds took:  " + seconds);    

    } catch (e) {
        general_error(e);
    }
}

function solarmodel_draw_chart() {
    try {
        var start_date = new Date();
        //vrd_graphing_drawChart_monthlyprices();
        // Obtain table data 
        deal_id = $('#selDealName').val();
        if (deal_id==null){
            deal_id=0
        }            
        
        urlMain = '/api_solarmodel/change_deal?deal_id=' + deal_id
        //var ResultData = general_return_json_api(urlMain);   
        urlMain = '/api_solarmodel/obtaintable?deal_id=' + deal_id
        var ResultData = general_return_json_api(urlMain);        
        //alertify.success("Acquisition of Data Time in seconds took:  " + seconds);              
        var dataTable_table = new google.visualization.DataTable();
        dataTable_table.addColumn('string', 'Descption');
        dataTable_table.addColumn('number', 'Value');
        var arrAppend = [];
        
        for (var i in ResultData) {
            var arrRow = [];
            arrRow.push(ResultData[i].Descrip);
            arrRow.push(ResultData[i].Val);
            dataTable_table.addRow(arrRow);
        }    
        var number_formatter = new google.visualization.NumberFormat({ pattern: '#,###.##' });
        var date_formatter = new google.visualization.DateFormat('short')
        //number_formater.format(dataTable_table, 1);     
        number_formatter.format(dataTable_table, 1);
        var view = new google.visualization.DataView(dataTable_table);
        view.setColumns([0, 1,
            {
                calc: "stringify",
                sourceColumn: 1,
                type: "string",
                role: "annotation"
            }]);
        var table = new google.visualization.Table(document.getElementById('graphs_left'));
               
        table.draw(dataTable_table, { showRowNumber: true, width: '100%', height: '100%' });
        // Graph          
        urlMain = '/api_solarmodel/obtaingraph?deal_id=' + deal_id
        var ResultData = general_return_json_api(urlMain);  
        var arrAppend = [];        
        var  dataTable_graph = new google.visualization.DataTable();
        //dataTable_graph.addColumn('string', 'Description'); 
        var monthYearFormatter = new google.visualization.DateFormat({ pattern: "MMM yyyy" });  
        dataTable_graph.addColumn("date","Date");
        dataTable_graph.addColumn("number","Volume");
        monthYearFormatter.format(dataTable_graph, 0);
        // Filling Google Table
        var hTicks = [];
        var bl_ticks= 0;
        for (var i in ResultData) {
            var arrRow = [];
            var ddate = new Date(ResultData[i].Yr, ResultData[i].Mnth, ResultData[i].DayofdDate);                        
            hTicks.push(ddate);
            arrRow.push(ddate);
            arrRow.push(ResultData[i].volumeMWH);
            dataTable_graph.addRow(arrRow);
        }    
        var linearOptions = {
                title: 'Volume MWh',
                legend: 'none',                
                hAxis: {
                  title: 'Date',
                  ticks: hTicks,
                  format: 'MM/dd/YYYY'
                }
              };            
        number_formatter.format(dataTable_graph, 1);  
        //date_formatter.format(dataTable_graph,0);
        var graph_right = new google.visualization.ColumnChart(document.getElementById('graphs_right'));
        //graph_right.draw(dataTable_graph, { showRowNumber: true, width: '100%', height: '100%' });                        
        graph_right.draw(dataTable_graph, linearOptions);
        var end_date = new Date();
        var seconds = Math.abs(start_date - end_date) / 1000;
        //alertify.success("Total Time in seconds took:  " + seconds);    
    }
    catch (e) {
        general_error(e);
    }
}
// autocomplete
function USAFautocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function (e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    if (inp.value != undefined) {
                        alertify.success("Selected Value is " + inp.value);
                        //FacilityGetInfo(inp.value);
                        //FacilityGetInfo('',inp.value);
                        $('#txtStationName').html("State");
                    } else {                        
                        //FacilityGetInfo('', inp.value);
                    }
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });
    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }
    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}
