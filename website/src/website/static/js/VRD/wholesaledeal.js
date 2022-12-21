
function wholesale_deal_clear(){
    try{        
        $('#WholeSaleDealName').val('');        
        var current_date = new Date();
        var day = ("0" + current_date.getDate()).slice(-2);
        var month = ("0" + (current_date.getMonth() + 1)).slice(-2);               
        DateString = current_date.getFullYear() +"-"+(month)+"-"+(day);
        $('#startdate').val(DateString);
        current_date.setFullYear(current_date.getFullYear() + 1);
        day = ("0" + current_date.getDate()).slice(-2);
        month = ("0" + (current_date.getMonth() + 1)).slice(-2);               
        DateString = current_date.getFullYear() +"-"+(month)+"-"+(day);
        $('#enddate').val(DateString);
        $('#WholeSaleDealName').val('');
        $('#selWholeSaleCounterParty').val(0);
        $('#selWholeSaleSecondCounterParty').val(0);
        $('#selSettlementPoint').val(0);
        $('#selSettlementLocation').val(0);
        $('#selWholesaleBlock').val(0);
        $('#WholeSaleDealVolume').val(0);
        $('#WholeSaleDealPrice').val(0);   
        $('#WholeSaleDealFee').val(0); 
        $('#WholeSaleDealConfirmStatus').hide();
        document.querySelector('input[name=BuySellRadio][value=BuyValue]').checked = true;

        
        document.querySelector('input[name=PhysicalFinancialRadio][value=PhysicalValue]').checked = true;            
    }catch (e) {
        e= 'You received an error on startup:  ' + e;
        general_error(e);
    }
}
function wholesaledeal_dealselect(){
    try{
        // Select a deal
        var WholeSaleDealId = $('#selWholeSaleDeal').val();        
        wholesale_deal_clear();  
        if (WholeSaleDealId != 0) {            
            var urlMain = '/api_wholesaledeal/dealselection/'
            var DataUrl = WholeSaleDealId
            urlMain = urlMain + DataUrl;
            var ResultData = general_return_json_api(urlMain);                       
            for (var i in ResultData) {                                
                $('#startdate').val(ResultData[i].StartDateString);
                $('#enddate').val(ResultData[i].EndDateString);
                $('#WholeSaleDealName').val(ResultData[i].WholeSaleDealName);                
                $('#selWholeSaleCounterParty').val(ResultData[i].CounterPartyID);
                $('#selWholeSaleSecondCounterParty').val(ResultData[i].SecondCounterPartyID);
                $('#selSettlementPoint').val(ResultData[i].SettlementPointID);
                $('#selSettlementLocation').val(ResultData[i].SetLocationID);
                $('#selWholesaleBlock').val(ResultData[i].WholeSaleBlockID);
                //wholesale_deal_selector();
                $('#WholeSaleDealVolume').val(ResultData[i].VolumeMW);
                $('#WholeSaleDealPrice').val(ResultData[i].Price);
                $('#WholeSaleDealFee').val(ResultData[i].Fee);
                var confirmed = ResultData[i].Confirmed;
                // Buy or Sale
                var BuySell = ResultData[i].BuySell;                
                if (BuySell.toLowerCase() == "s") {
                    document.querySelector('input[name=BuySellRadio][value=SellValue]').checked = true;                                        
                }
                var PhysicalFinancial = ResultData[i].PhysicalFinancial;                
                if (PhysicalFinancial.toLowerCase() == "f") {
                    document.querySelector('input[name=PhysicalFinancialRadio][value=FinanicalValue]').checked = true;                                        
                }
                if ((ResultData[i].WholeSaleBlockID>=7) && (ResultData[i].WholeSaleBlockID<=9)) {
                    $("#wholesale_deal_btn_upload").prop('disabled', false);
                } else{
                    $("#wholesale_deal_btn_upload").prop('disabled', true);
                }
                if (confirmed==0){
                    $('#WholeSaleDealConfirmStatus').hide();
                } else{
                    $('#WholeSaleDealConfirmStatus').show();
                }
            }
        }
    } catch (e) {        
        general_error(e);
    }
} 
function wholesale_deal_new(){
    try{
        wholesale_deal_clear();
        $('#selWholeSaleDeal').val(0);
    } catch (e) {        
        general_error(e);
    }
}
function wholesale_deal_call_save(){
    alertify.confirm('Virtual Risk Desk', 'Are you sure you want to save this record?', function(){wholesale_deal_save() }
                , function(){ alertify.error('Nothing was saved')});
}
function wholesale_deal_save(){
    try{
        var confimed_status = $('#WholeSaleDealConfirmStatus').is(":visible");
        if (confimed_status==true){
            alertify.error("This deal is confirmed.   Saving is not allowed");
            return;
        }
        var WholeSaleDealId = $('#selWholeSaleDeal').val();
        var msg = "Please confirm that you want to save this record";
        if (WholeSaleDealId==0){ 
            msg = "Please confirm that you want to add a new record";
        }        
        if (WholeSaleDealId == 0) {
            msg = 'You have added a new record';
        } else {
            msg = 'You have saved this record';
        }                
        // Saving out deal
        var WholeSaleDealName = $('#WholeSaleDealName').val()
        var WholeSaleCounterPartyID = $('#selWholeSaleCounterParty').val();
        var WholeSaleSecondCounterPartyID = $('#selWholeSaleSecondCounterParty').val();
        var SettlementPointID = $('#selSettlementPoint').val();
        var SettlementLocationID = $('#selSettlementLocation').val();
        var WholesaleBlockID = $('#selWholesaleBlock').val();
        var VolumeMW = $('#WholeSaleDealVolume').val();
        var Price = $('#WholeSaleDealPrice').val();        
        var Fee = $('#WholeSaleDealFee').val();             
        var StartDate = $('#startdate').val();             
        var EndDate= $('#enddate').val();             
        if (VolumeMW == null) { VolumeMW = 0; }
        if (Fee == null) { Fee = 0;}
        if (Price == null) { Price = 0; }
        var CurrentDealActive = 1;
        if ($('#Active_Deal').is(':checked') != true) { CurrentDealActive = 0; }         
        var BuySell = 'Buy';
        //var rb = document.getElementsByName("buysell");        
        var BuySellChecker = document.querySelector('input[name=BuySellRadio][value=SellValue]').checked;
        if (BuySellChecker == true) {
            BuySell = "Sell"; 
        }
        var PhysicalFinancial = "Physical";
        var PhysicalFinancialChecker = false;
        //var rb = document.getElementsByName("buysell");        
        var PhysicalFinancialChecker = document.querySelector('input[name=PhysicalFinancialRadio][value=FinanicalValue]').checked;
        if (PhysicalFinancialChecker == true) {
            PhysicalFinancial = "Financial"; 
        }        
        var urlMain = '/api_wholesaledeal/updatedeal';        
        var DataUrl = '?WholeSaleDealID=' + WholeSaleDealId + '&WholesaleDealName=' + WholeSaleDealName        
        DataUrl = DataUrl + '&CounterPartyID=' + WholeSaleCounterPartyID + '&SecondCounterPartyID=' + WholeSaleSecondCounterPartyID + '&SettlementPointID=' + SettlementPointID + '&SetLocationID=' + SettlementLocationID + '&WholeSaleBlockID=' + WholesaleBlockID + '&StartDate=' + StartDate + '&EndDate=' + EndDate + '&VolumeMW=' + VolumeMW + '&Price=' + Price + '&Active=' + CurrentDealActive + '&Fee=' + Fee + '&BuySell=' + BuySell 
        DataUrl = DataUrl + '&PhysicalFinancial=' + PhysicalFinancial
        urlMain = urlMain + DataUrl;
        var ResultData = general_return_json_api_post(urlMain);
        var sts = ResultData.Status;   
        WholeSaleDealId  = ResultData.Identifier;        
        if (sts == "SUCCESS"){
            alertify.success("The record was saved");   
            // Reset the wholesale deal selector      
            urlMainBase = '/api_wholesaledeal/general/'
            urlMain = urlMainBase + 'deallist';    
            general_fill_selector('selWholeSaleDeal',urlMain,'Wholesale Deal');                  
            $('#selWholeSaleDeal').val(WholeSaleDealId);
            wholesaledeal_dealselect();
        } else {
            alertify.error("The record was not saved due to an error");
        }
    } catch (e) {        
        general_error(e);
    }
}
function wholesale_uploader_upload_files(){
    try{
        progressed = 0.0;        
        displayProcess(progressed);

        var WholeSaleDealId = $('#selWholeSaleDeal').val();
        if (WholeSaleDealId == 0) {
            alertify.error("Please save the new deal before adding a custom.   The system needs a whole sale identifier to add a custom whole saleblock");
        } else {
            document.getElementById("files").click();
            var files = document.getElementById('files').files;
        }
    } catch (e) {        
        general_error(e);
    }
}
function wholesale_deal_selector(){
    // When the custom is selected on
    // whole sale block, the whole sale custom
    // buttons are selected
    try{
        var current_wholesale = 'N/A';
        var control_name = 'selWholesaleBlock';
        current_wholesale = $("#" + control_name + " option:selected").text();
        control_name = "wholesale_deal_btn_upload";
        var wholesale_deal_id = $('#selWholeSaleDeal').val();
        var wholesale_block_id = $('#selWholesaleBlock').val();
        if ((wholesale_deal_id == 0) && (wholesale_block_id>=7) && (wholesale_block_id<=9)) {
            alertify.error("You have to save the deal before selecting custom");
            $('#selWholesaleBlock').val(0);
        } else {
            if ((current_wholesale.toLowerCase() == "custom hourly") || (current_wholesale.toLowerCase() == "custom block wide") || (current_wholesale.toLowerCase() == "custom block")) {
                $("#" + control_name).prop('disabled', false);
            } else {
                $("#" + control_name).prop('disabled', true);
            }            
        }
        
    } catch (e) {        
        general_error(e);
    }
}
function wholesale_uploader_show_file(input){
    // Upload files and send to azure function
    try{
        progressed = 0.0;
        displayProcess(progressed);
        let file = input.files[0];
        wholesale_uploader_Upload_files('whole_sale_custom');
    } catch (e) {        
        general_error(e);
    }
}

function wholesale_uploader_Upload_files(FileType) {
    try {
        var files = document.getElementById('files').files;        
        fileslength = files.length;
        if (fileslength > 0) {            
            var FileName = files[0].name;
            FileNameForImport = general_get_unique_file_name(FileName);
            files[0].name = FileNameForImport;
            var dt = new Date();
            AzureParms = general_get_azure_parms();
            //var UserName = ReturnUserName();
            var AzureStorageName = AzureParms.AzureStorageName;
            var sas = AzureParms.SASKey;
            var blobUri = AzureParms.blobUri;
            container = AzureParms.AzureContainer;
            FileType = FileType.toUpperCase();
            FileType = FileType.trim();
            if (FileType == 'whole_sale_custom') {
                FileName = files[0].name;
                // Update DB for File Status
                iFileCount = files.length;
                for (iFile = 0; iFile < iFileCount; iFile++) {
                    FileName = files[iFile].name;
                    //var FileID = LogFileUploadStatus(0, FileNameForImport, 'UPLD', FileType, UserName);
                    // Change the files
                    iFile = 0;
                    uploadBlobByStream_wholesaledeal(false, files[iFile], FileNameForImport, AzureParms);
                }
                msg = "Uploading proceeding";
                alertify.success(msg);
                FileNameUpload = FileNameForImport;            
            } else {
                FileType = FileType.toUpperCase();
                FileType = FileType.trim();
                iFile = 0;
                uploadBlobByStream_wholesaledeal(false, files[iFile], FileNameForImport, AzureParms);
                msg = "Uploading proceeding";
                alertify.success(msg);
                FileNameUpload = FileNameForImport;
            }
            files = null;
            document.getElementById("files").value = null;

            progressed = 10.0;
            displayProcess(progressed);
        } else {
            files = null;
            document.getElementById("files").value = null;       
            alertify.error("Please select a file before pressing upload");
        }

    }
    catch (e) {
        general_error(e)
    }
}
function uploadBlobByStream_wholesaledeal(checkMD5, files, filename, AzureParms) {
    try {
        var file = files;
        //var AzureStorageName = AzureParms.AzureStorageName;
        //var sas = AzureParms.SASKey;
        //var blobUri = AzureParms.blobUri;
        //container = AzureParms.AzureContainer;

        var blobService = getBlobService(AzureParms);
        if (!blobService)
            return;
        //var btn = document.getElementById("upload-button");
        //btn.disabled = true;
        //btn.innerHTML = "Uploading";
        // Make a smaller block size when uploading small blobs
        var blockSize = file.size > 1024 * 1024 * 32 ? 1024 * 1024 * 4 : 1024 * 512;
        var options = {
            storeBlobContentMD5: checkMD5,
            blockSize: blockSize
        };
        blobService.singleBlobPutThresholdInBytes = blockSize;
        var finishedOrError = false;
        var container = 'testuploadcontainer';
        var dt = new Date();


        //#var speedSummary = blobService.createBlockBlobFromBrowserFile(container, fileList[i]["FileID"], selectedFiles[i].fileObject, options, function (error, result, response) 


        var speedSummary = blobService.createBlockBlobFromBrowserFile(AzureParms.AzureContainer,
            filename,
            file,
            (error, result) => {
                if (error) {
                    // Handle blob error
                } else {
                    console.log('Upload is successful');
                    //await delay(2000);
                    setInterval(wholesale_uploader_import_table(), 2000);
                    //ImportIntoValidationTableNew();
                }
            });

        speedSummary.on('progress', function () {
            var process = speedSummary.getCompletePercent();
            displayProcess(process);
        });
    }
    catch (e) {
        general_error(e)
    }
}
function wholesale_uploader_import_table() {
    try {
        var FileName = FileNameForImport;
        var sheet_name = "Sheet1";
        sts = wholesaledeal_update_import_status("Beginning processing...")
        var file_name = FileName;
        file_name = file_name.toLowerCase();
        var ln = file_name.length;
        var start = ln - 4;
        var end = ln;
        var short_type = file_name.substring(start, ln);
        start = ln - 5;
        var long_type = file_name.substring(start, ln);
        var sheet_name = "SH";
        // Hide All But One         
        //generic_uploader_hide_all_tabs();
        if (short_type == ".xls" || short_type == ".xlm" || long_type == ".xlsx" || long_type == ".xlsm") {
            // Obtain sheet names
            file_name = file_name.toLowerCase();            
            var urlMain = '/api_general/return_excel_sheets/file_name=' + file_name;                        
            var ResultData = general_return_json_api(urlMain);
            // Clear the selector
            var selControl = "selSheets";
            $('#' + selControl).empty();
            SelectorID = 0 ;
            SelectorText ='- Select Sheet -'
            $('#' + selControl).append('<option value="' + SelectorID + '">' + SelectorText + '</option>')            
            for (var iRows in ResultData) {                
                SelectorID = iRows;
                SelectorText = ResultData[iRows].SheetName;                                
                $('#' + selControl).append('<option value="' + SelectorID + '">' + SelectorText + '</option>')
            }
            alertify.success(ResultData);

            $("#myModalCustom").modal('show');
            
            // Set Here
        } else {
            var tab_id = 1;
            //generic_uploader_hide_all_tabs();
            var sheet_name = 'CSV';
            //$('#tab_header_' + tab_id.toString()).text(sheet_name);   
            var wholesaledeal_id = $('#selWholeSaleDeal').val();
            wholesaledeal_uploader_custom()
            //run_id = wholesale_deal_run_data_factory_pull(FileName, sheet_name, wholesaledeal_id );
            //var tab_id_arr = []
            //var run_id_arr = [];
            //run_id_arr.push(run_id);
            //tab_id_arr.push(1);
            //var iLimiter = 1;
            //set_run_checkerV2(run_id_arr, tab_id_arr, iLimiter);
            // Set Here
        }
    } catch (e) {
        $("#DataFactoryProcessing").text("Error in processing...")
        general_error(e)
    }
}
function wholesaledeal_uploader_custom(){
    try{
        // Establish Variables        
        var wholesaledeal_id = $('#selWholeSaleDeal').val();
        var file_name = FileNameUpload;
        var sheet_name = 'CSV'        
        file_name_test = file_name.trim().toUpperCase()
        ln = file_name_test.length
        // File Type
        
        file_extension = file_name_test.substring(ln-3,ln);        
        var file_type = 'Excel'
        if (file_extension.toLowerCase() == "csv"){
            file_type = 'CSV'
        }
        // Sheet Name
        var sheet_name = 'CSV'         
        if (file_type!="CSV"){
            sheet_name = $('#selSheets option:selected').text();
        }                
        // Block Type 
        var import_type_id = $('#selWholesaleBlock option:selected').val();        
        var block_type = 'N/A'
        if (import_type_id == 7){
            //Custom Hourly
            block_type ='WholeSaleBlockCustom'
            alertify.success("Uploading of custom blocks will be released in near future");
            return
        } else if (import_type_id == 8) {
            //Custom Block 
            block_type ='WholeSaleBlockCustomBlock'
            alertify.success("Uploading of custom blocks will be released in near future");
            return
        } else{
            //Custom Block Wide
            block_type ='WholeSaleBlockCustomBlockWide'
            alertify.success("Uploading of custom blocks will be released in near future");
            return
        }
        var urlMain = '/api_wholesaledeal/import_custom_data';        
        var DataUrl = '?file_name=' + file_name + '&wholesale_deal_id=' + wholesaledeal_id
        DataUrl = DataUrl + '&sheet_name=' + sheet_name + '&block_type=' + block_type
        DataUrl = DataUrl + '&file_type=' + file_type
        urlMain = urlMain + DataUrl;
        var ResultData = general_return_json_api(urlMain);                       
        var sts = ResultData.Status;     
        var run_response = ResultData.run_response;
        async_check_function(run_response); 
        if (sts == "SUCCESS"){
            alertify.success("The record was saved");        
        } else {
            alertify.error("The record was not saved due to an error");
        }    
        $("#myModalCustom").modal('hide');        
    } catch (e) {    
        general_error(e)
    }
}
function wholesaledeal_update_import_status(Msg) {
    $("#DataFactoryProcessing").text("Beginning processing...")    
    return "SUCCESS"
}
function wholesaledeal_confirmdeal_alert(){
    try{
        alertify.confirm('Deal Confirmation', 'Confirm Message', function(){ wholesale_deal_confirm() }
                , function(){ alertify.error('Cancel')});
    } catch (e) {    
        general_error(e)
    }
}
function wholesale_deal_confirm(){
    try{
        var wholesaledeal_id = $('#selWholeSaleDeal').val();
        var urlMain = '/api_wholesaledeal/confirm_deal';        
        var DataUrl = '?wholesale_deal_id=' + wholesaledeal_id
        urlMain = urlMain + DataUrl;
        var ResultData = general_return_json_api(urlMain);    
        if (ResultData.Status=="SUCCESS"){
            alertify.success("Deal Is Confirmed");
        }else{
            alertify.error("Insufficient Rights Deal Not Saved");
        }
        
        

        } catch (e) {    
        general_error(e)
    }
}

// General Functions for Wholesale Screen
async function async_check_function(run_id) { 
    try{
        $('#wholesale_deal_datafactorprocessing_div').show();
        var wait_seconds = 5000;   
        var result1 = await resolve_after_n_seconds(run_id, wait_seconds);         
        // Check status of programs
        for (i= 1; i<10; i++){
            result1 = await resolve_after_n_seconds(run_id, wait_seconds);                
            if (result1 !="INPROC") {                
                if (result1 == "SUCCESS"){
                    alertify.success("File Successfully Processed");                                 
                } else{
                    alertify.error("File Failed To Process");       
                }
                $('#wholesale_deal_datafactorprocessing_div').hide();
                break;
            }
        }    
    } catch (e) {    
        general_error(e)
        $('#wholesale_deal_datafactorprocessing_div').hide();
    }
}



function resolve_after_n_seconds(run_id, wait_seconds) {
    return new Promise(resolve => {
        setTimeout(() => {
            // Check Status
            urlMain = "/api_general/return_datafactory_run_status"
            dataMain = "?run_id=" + run_id;
            urlMain = urlMain + dataMain;
            var ResultData = general_return_json_api(urlMain);      
            var sts = ResultData.Status;
            var sts_response = "INPROC"
            if (sts == "SUCCESS"){
                sts = ResultData.run_status;
                if (sts=="Succeeded"){
                    sts_response ="SUCCESS";
                } else if (sts=="Failed"){
                    sts_response ="FAILURE";
                } else {
                    sts_response = "INPROC";
                }
            }            
            resolve(sts_response);            
        }, wait_seconds);
    });
}
