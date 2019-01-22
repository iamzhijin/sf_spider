/**
 * Created by linshirong on 2017/9/15.
 */


function resetForm(){
    $("#project_id").val('');
    $("#project_name").val('');
    $("#project_desc").val('');
    $('#confirmModal').modal('toggle');
}

function validateAndSubmitForm() {
    project_id = $("#project_id").val();
    project_name = $("#project_name").val();
    es_table = $("#es_table").val();
    project_desc = $("#project_desc").val();

    var checkID = /^[A-Za-z0-9_-]+$/;
    validate = false;
    if(project_id == null || project_id.trim().length <=0){
        alert_box('error','项目编码不可以为空！');
        return;
    }else if(!checkID.test(project_id)){
        alert_box('error','项目编码只能是字母、数字、下划线、中横线！');
        return;
    }
    if(es_table == null || es_table.trim().length <=0){
        alert_box('error','es地址不可以为空！');
        return;
    }
    if(project_name == null || project_name.trim().length <=0){
        alert_box('error','项目名字不可以为空！');
        return;
    }
    if(project_desc == null || project_desc.trim().length <= 0){
        alert_box('error','项目描述不可以为空！');
        return;
    }

    $("#project_id").val(project_id.trim());
    $("#project_name").val(project_name.trim());
    $("#es_table").val(es_table.trim());
    $("#project_desc").val(project_desc.trim());

    $('#project_create').submit();

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


