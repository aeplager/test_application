function wholesaledealclose_dealselect(){
    try{
        var WholeSaleDealId = $('#selWholeSaleDeal').val();
        var urlMain = '/api_wholesaledeal/dealselection/' + WholeSaleDealId;
        var ResultData = general_return_json_api_post(urlMain);
        for (var i in ResultData) {  
            var closedate_main = ResultData[i].CloseDateString;
            var basedate = new Date();
            var basedate_string = '';
            if (closedate_main == null){
                var mnth = basedate.getMonth();
                var dy = basedate.getDay()
                if (mnth < 10) {mnth = '0' + mnth;}
                if (dy < 10) {dy = '0' + dy;}
                basedate_string = basedate.getFullYear() + '-' + mnth + '-' + dy;                
            } else{
                basedate_string = ResultData[i].CloseDateString;
            }
            $('#closedate').val(basedate_string);            
            var closeprice = ResultData[i].ClosePrice;
            var price_validation = $.isNumeric( closeprice)
            if ((closeprice!=null) && (price_validation==true)) {
                $('#WholeSaleDealClosePrice').val(closeprice);
            } else {
                $('#WholeSaleDealClosePrice').val(0);
            }
            var bookprice = ResultData[i].ClosePrice;
            price_validation = $.isNumeric( bookprice)
            if ((bookprice!=null) && (price_validation==true)) {
                $('#WholeSaleDealBookPrice').val(bookprice);
            } else {
                $('#WholeSaleDealBookPrice').val(0);
            }
            $('#WholeSaleDealName').val(ResultData[i].WholeSaleDealName);
            // Setting Confirmed And Closed
            var confirmed = ResultData[i].Confirmed;                        
            document.querySelector('input[name=ConfirmedRadio][value=Confirmed]').checked = true;
            if (confirmed == false) {
                document.querySelector('input[name=ConfirmedRadio][value=UnConfirmed]').checked = true;                                           
            }
            var closed = ResultData[i].Closed;                        
            document.querySelector('input[name=CloseRadio][value=Unclosed]').checked = true;                                        
            if (closed == true) {
                document.querySelector('input[name=CloseRadio][value=Closed]').checked = true;    
            }
        }
    } catch (e) {    
        general_error(e)
    }
}
function wholesaledealclose_confirmsave(){
    alertify.confirm('Deal Close Confirmation', 'Confirm Message', function(){ wholesaledealclose_savedeal() }
                , function(){ alertify.error('Cancel')});
}
function wholesaledealclose_savedeal(){
    try{

        var WholeSaleDealId = $('#selWholeSaleDeal').val();
        if (WholeSaleDealId==0){
            alertify.error("Please select a deal before closing a deal");
        } else {
            var book_price = $('#WholeSaleDealBookPrice').val();
            var close_price = $('#WholeSaleDealClosePrice').val();
            var close_date = $('#closedate').val();
            var confirmed = document.querySelector('input[name=ConfirmedRadio][value=Confirmed]').checked;
            var closed = document.querySelector('input[name=CloseRadio][value=Closed]').checked;                                        
            // Obtain Deal Information
            urlMain = '/api_wholesaledeal/dealselection/' + WholeSaleDealId;
            var ResultData = general_return_json_api_post(urlMain);
            var blFound = false;
            for (var i in ResultData) {  
                blFound = true;
                closed_current = ResultData[i].Closed;
                confirmed_current = ResultData[i].Confirmed;
                break;
            }
            if ((confirmed==false) && (closed==true)){                
                alertify.error("A deal needs to be confirmed before it can be closed.")                
            } else {
                sts = "SUCCESS"
                if (confirmed_current!=confirmed){
                    // Update Confirmed
                    //wholesale_deal_id = request.args.get('wholesale_deal_id', 0) # use default value repalce 'None'        
                    //confirm_status = request.args.get('confirm_status', 1) # use default value repalce 'None'
                    var confirmed_send = 0;
                    if (confirmed == true) {
                        confirmed_send = 1;
                    }
                    var urlMain = '/api_wholesaledeal/confirm_deal';        
                    var DataUrl = '?wholesale_deal_id=' + WholeSaleDealId + "&confirm_status=" + confirmed_send;
                    urlMain = urlMain + DataUrl;
                    var ResultData = general_return_json_api(urlMain);    
                    sts = ResultData.Status;
                    if (sts = "SUCCESS"){
                        alertify.success("Successfully confirmed deal");
                    } else {
                        alertify.error("Error in confirming deal");
                    }                    
                } 
                // Close Deal                
                if (sts=="SUCCESS"){
                    var closed_send = 0;
                    if (closed=true) {closed_send = 1;}
                    var urlMain = '/api_wholesaledeal/wholesaledealclose';
                    var dataUrl = '?wholesale_deal_id=' + WholeSaleDealId + "&BookPrice=" + book_price;
                    dataUrl = dataUrl + "&ClosePrice=" + close_price + "&CloseDate=" + close_date;
                    dataUrl = dataUrl + "&Closed=" + closed_send
                    urlMain = urlMain + dataUrl;
                    var ResultData = general_return_json_api(urlMain);  
                    sts =  ResultData.Status;
                    if (sts = "SUCCESS"){
                        alertify.success("Successfully closed deal");
                    } else {
                        alertify.error("Error in closed deal");
                    }                    
                    
                }
            }

        }

    } catch (e) {    
        general_error(e)
    }
}

