/**
 * Created by linshirong on 2017/9/16.
 */

function resetForm(){
    $('.form-horizontal')[0].reset()
    $('#confirmModal').modal('toggle');
}

function validateAndSubmitForm() {
    project_id = $("#project_id").val();
    crawler_id = $("#crawler_id").val();
    crawler_name = $("#crawler_name").val();
    crawler_app = $("#crawler_app").val();
    field_mapping = $("#field_mapping").val();
    need_clean = $("#need_clean").val();
    clean_app = $("#clean_app").val();
    clean_parameters = $('#clean_parameters').val();

    var checkID = /^[A-Za-z0-9_-]+$/;
    validate = false;
    if(project_id == null || project_id.trim().length <=0){
        alert_box('error','请选择项目！');
        return;
    }else if(!checkID.test(project_id)){
        alert_box('error','项目编码只能是字母、数字、下划线、中横线！');
        return;
    }
    if(crawler_id == null || crawler_id.trim().length <=0){
        alert_box('error','请填写爬虫编码！');
        return;
    }else if(!checkID.test(crawler_id)){
        alert_box('error','爬虫编码只能是字母、数字、下划线、中横线！');
        return;
    }
    if(crawler_name == null || crawler_name.trim().length <=0){
        alert_box('error','爬虫名字不可以为空！');
        return;
    }

    if(!isJsonFormat(field_mapping)){
        alert_box('error', '字段映射必须是json格式，如：[{"name":"f1", "type":"int", "doc": "描述", "default": "默认值"}, {"name": "f2", "type": "string", "doc": "描述", "default": "默认值"}]');
        return;
    }
    var checkClean = /^[a-z][a-zA-Z0-9_]*(\.[a-z][a-zA-Z0-9_]*)*\.[A-Z][a-zA-Z0-9_]*/;

    if(clean_parameters.length>0 && !checkClean.test(clean_parameters)){
        alert_box("error", "请填写正确的类名，包含包名");
        return;
    }

    $("#project_id").val(project_id.trim());
    $("#crawler_id").val(crawler_id.trim());
    $("#crawler_name").val(crawler_name.trim());
    $("#field_mapping").val(field_mapping.trim());
    $("#clean_parameters").val(clean_parameters.trim());

    $('#crawler_create').submit();

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