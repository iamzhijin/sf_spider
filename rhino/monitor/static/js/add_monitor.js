/**
 * Created by linshirong on 2017/9/15.
 */


function resetForm(){
    $("#monitor_province").val('');
    $("#monitor_entName").val('');
    $("#monitor_content").val('');
    $('#confirmModal').modal('toggle');
}

function validateAndSubmitForm() {
    monitor_province = $("#monitor_province").val();
    monitor_entName = $("#monitor_entName").val();
    monitor_content = $("#monitor_content").val();

    validate = false;
    if(monitor_province == null || monitor_province.trim().length <=0){
        alert_box('error','省份不可以为空！');
        return;
    }

    if(monitor_entName == null || monitor_entName.trim().length <=0){
        alert_box('error','企业名称不可以为空！');
        return;
    }
    if(monitor_content == null || monitor_content.trim().length <= 0){
        alert_box('error','爬虫内容不可以为空！');
        return;
    }

    $("#monitor_province").val(monitor_province.trim());
    $("#monitor_entName").val(monitor_entName.trim());
    $("#monitor_content").val(monitor_content.trim());

    $('#monitor_create').submit();

    /*$.ajax({
        url: "crawler_manage/project/create_validate",
        async: false,
        success: function () {
            
        },
        dataType: "json",
        timeout: 10*1000,
        data: {
            "project_id": project_id,
            "project_name": project_name,
            "project_desc": project_desc
        }
    })*/
}


