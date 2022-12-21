function general_error(errmsg){
    // Reporting any error
    if (errmsg==''){
        errmsg = 'Error unavailable';
    }
    alertify.error('You received the following error:  ' + errmsg);
}
function general_fill_selector(selControl, urlMain, FirstRec) {
    try {
        $('#' + selControl).empty();
        var SelectorID = 0;
        var SelectorText = FirstRec;
        var ResultData = general_return_json_api(urlMain);
        $('#' + selControl).append('<option value="' + SelectorID + '"> - ' + SelectorText + ' - </option>')
        for (var i in ResultData) {
            SelectorID = ResultData[i].SelectorID;
            SelectorText = ResultData[i].SelectorText
            $('#' + selControl).append('<option value="' + SelectorID + '">' + SelectorText + '</option>')
        }
    } catch (e) {
        general_error(e);
    }
}

function general_return_json_api(urlMain) {
    try {       
        var ReturnData;
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            // Change Here To Change The Web Service Needed
            //url: "/AzureHooknLineAjax.svc/HelloWorld",
            url: urlMain,
            // Change Here To Change The Parameters Needed
            // data: "{}",
            dataType: "json",
            async: false,
            success: function (Result) {
                ReturnData = Result;
            },
            error: function (Result) {
                alertify.error(Result.statusText);
            }
        });
        return ReturnData;
    }
    catch (e) {
        general_error(e);
    }
}
async function general_return_json_api_async(urlMain){
    try {
        var ReturnData;
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            // Change Here To Change The Web Service Needed
            //url: "/AzureHooknLineAjax.svc/HelloWorld",
            url: urlMain,
            // Change Here To Change The Parameters Needed
            // data: "{}",
            dataType: "json",
            async: true,
            success: function (Result) {
                ReturnData = Result;
            },
            error: function (Result) {
                alertify.error(Result.statusText);
            }
        });
        return ReturnData;
    }
    catch (e) {
        general_error(e)
    }
}

function general_return_json_api_post(urlMain) {
    try {       
        var ReturnData;
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            // Change Here To Change The Web Service Needed
            //url: "/AzureHooknLineAjax.svc/HelloWorld",
            url: urlMain,
            // Change Here To Change The Parameters Needed
            // data: "{}",
            dataType: "json",
            async: false,
            success: function (Result) {
                ReturnData = Result;
            },
            error: function (Result) {
                alertify.error(Result.statusText);
            }
        });
        return ReturnData;
    }
    catch (e) {
        general_error(e);
    }
}
function general_get_azure_parms(){
    try{
        // Obtain the Azure Parameters
        // For uploading files
        urlMain = "/api_general/azureparms"
        return_data = general_return_json_api_post(urlMain)
        return return_data
    } catch(e){
        general_error(e);
    }
}
function general_get_unique_file_name(file_name){
    try{
        // Obtain a unique file name
        // from the server based on a date
        urlMain = '/api_general/return_unique_filename/' + file_name;
        return_data = general_return_json_api_post(urlMain)
        if (return_data.Status=="SUCCESS"){
            return return_data.file_name;
        }            
        else{
            return file_name;
        }

    } catch(e){
        general_error(e);
    }
}
    

