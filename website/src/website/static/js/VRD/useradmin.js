function useradmin_user_select(){
    try{        
        email = $("#selUserEmail option:selected" ).text();
        urlMain = '/api_usermgt/useraccount?'        
        dataMain = "user_account=" + email
        urlMain = urlMain + dataMain
        var ResultData = general_return_json_api_post(urlMain);
        for (var iRows in ResultData) {                
            $('#txtUserEmail').val(ResultData[iRows].Email)
            $('#selUserType').val(ResultData[iRows].UserAccountTypeID)
            $('#admin_firstname').val(ResultData[iRows].FirstName)
            $('#admin_lastname').val(ResultData[iRows].LastName)
            $("#UserMgtActive").prop( "checked", true );
            $("#UserMgtPasswordReset").prop( "checked", false );
            $("#UserMgtSuperUser").prop( "checked", false );
            if (ResultData[iRows].Active!=1){
                $("#UserMgtActive").prop( "checked", false)
            }
            if (ResultData[iRows].SuperUser==1){
                $("#UserMgtSuperUser").prop( "checked", true)
            }
            if (ResultData[iRows].ResetPassword!=1){
                $("#UserMgtPasswordReset").prop( "checked", true)
            }                     
            break
        }
    } catch (e) {        
        general_error(e);
    }
}
function useradmin_user_base(){
    try{
        $("#selUserEmail").val(0);
        $('#txtUserEmail').val("")
        $('#selUserType').val(0)
        $('#admin_firstname').val("")
        $('#admin_lastname').val("")
        $("#UserMgtActive").prop( "checked", true );
        $("#UserMgtPasswordReset").prop( "checked", false );
        $("#UserMgtSuperUser").prop( "checked", false );

    } catch (e) {        
        general_error(e);
    } 
}
function useradmin_user_update(){
    try{
        email_id = $("#selUserEmail").val();
        var email = $('#txtUserEmail').val();
        var email_compare = $("#selUserEmail option:selected" ).text()
        if ((email_id != 0) && (email != email_compare)) {
            alertify.error("The email is the user name and cannot be changed");            
        } else {
            var user_type_id  = $('#selUserType').val();
            var first_name = $('#admin_firstname').val();
            var last_name = $('#admin_lastname').val();
            var resetpwd = 0;
            var active  = 0;
            var super_user = 0
            if ($("#UserMgtPasswordReset").prop("checked") == true){resetpwd = 1;}
            if ($("#UserMgtActive").prop( "checked") == true) {active = 1;}
            if ($("#UserMgtSuperUser").prop( "checked") == true) {super_user = 1;}
            urlMain = '/api_usermgt/updateuser?';
            dataMain = 'email=' + email + "&user_type_id=" + user_type_id;
            dataMain = dataMain + "&first_name=" + first_name + "&last_name=" + last_name;
            dataMain = dataMain + "&resetpwd=" + resetpwd + "&active=" + active;
            dataMain = dataMain + "&super_user=" + super_user;
            urlMain = urlMain + dataMain;            
            var ResultData = general_return_json_api(urlMain);  
            var sts = ResultData.Status;
            if (sts == "SUCCESS") {
                alertify.success(sts);
            } else{
                alertify.error(sts);
            }
        }
        
    } catch(e){
        general_error(e);
    }

}
function useradmin_update_password(){
    try{
        var password1 = $('#txtPassword1').val();
        var password2 = $('#txtPassword2').val();
        // Trim the passwords
        password1 = password1.trim();
        password2 = password2.trim();
        // Validate Passwords Equal
        if (password1!=password2){
            alertify.error("Please make sure that the passwords are the same");
        } else if (password1.length<=7){
            alertify.error("Please make your passwords at least 7 characters long");
        } else {
            urlMain = '/api_usermgt/passwordreset';
            dataMain = '?password1=' + password1 + '&password2=' + password2;
            urlMain = urlMain + dataMain;
            var ResultData = general_return_json_api(urlMain);  
            var sts = ResultData.Status;
            if (sts=="SUCCESS"){
                alertify.success("Your password has been successfully changed.");
            } else {
                alertify.error("Password reset failed with error:  " + sts);
            }
                
        }


    } catch(e){
        general_error(e)
    }
}
function passwordresetandsendemailvalidate(){
    try{
        msg = "Are you sure you want to reset the password of  " +  $('#email').val();
        alertify.confirm(msg, 'Confirm Message', function(){ passwordresetandsendemail() }
        , function(){ alertify.error('Cancel')});
    } catch(e){
        general_error(e)
    }
}
function passwordresetandsendemail(){
    try{
        var email = $('#email').val();
        var urlMain = "/api_usermgt/passwordresetandsendemail";
        var dataMain = "?email=" + email;
        var urlMain = urlMain + dataMain;
        var ResultData = general_return_json_api(urlMain);  
        var sts = ResultData.Status;
        if (sts == "SUCCESS") {
            alertify.success("A Reset password has been sent to the email:  " + email);
        } else{
            alertify.error("You had an error in resetting the password");
        }
    } catch(e){
        general_error(e)
    }
}