/**
 * Created by linshirong on 2017/9/26.
 */


function validateAndSubmitForm() {
    var host = $("#host").val();
    var port = $("#port").val();
    var type = $("#type").val();
    var username = $("#username").val();
    var password = $("#password").val();

    var hostCheck = /^[A-Za-z_][A-Za-z0-9_-]+(\.[A-Za-z_][A-Za-z0-9_-]+)*$/;
    var ipCheck = /^[0-9]+(\.[0-9]+){3}$/;
    if(!hostCheck.test(host) && !ipCheck.test(host)){
        alert_box('error','服务器地址错误。服务器地址必须为域名或者IP！');
        return;
    }


    if(isNaN(port) || parseInt(port) <= 0){
        alert_box('error','服务器端口必须为大于0的数字');
        return;
    }

    var url = "/crawler_manage/server/create_submit";
    $.ajax({
        url: url,
        type: "post",
        data: {
            "host": host,
            "port": port,
            "type": type,
            "username": username,
            "password": password,
        },
        success: function(result){
            //alert(result);
            $('#server_create')[0].reset();
            alert_box("success", result.msg);
        },
        error: function(result){
            alert_box("error", result.msg);
        },
        dataType: 'json',
        timeout: 60* 1000,
    });
}

function resetForm(){
    $('#server_create')[0].reset();
    $('#confirmModal').modal('toggle');
}