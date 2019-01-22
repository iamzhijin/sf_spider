validateRuleTableInitialized = false;


function resetForm(){
    $('.form-horizontal')[0].reset()
    $('#validate_rules_table').bootstrapTable('removeAll');
    $('#confirmModal').modal('toggle');
}


function check_field_mappings() {
    //检查字段映射是否已经填写，如果没有，则报警
    var field_mapping = $('#field_mapping').val();
    if (field_mapping.trim().length <= 0) {
        alert_box('error', '请先填写字段映射，才可以进行清洗规则配置。');
    }
    else {
        if (isJsonFormat(field_mapping)) {
            $('.alert').alert('close');
            populateFieldSelection(field_mapping);
            $('#validateRuleSelectModal').modal();
        } else {
            alert_box('error', '字段映射必须是json格式，如：[{"name":"f1", "type":"int", "doc": "描述", "default": "默认值"}, {"name": "f2", "type": "string", "doc": "描述", "default": "默认值"}]');
        }
    }
}


function project_select() {
    $('#projectSelectModal').modal('show');
    initProjectTable();
}

function initProjectTable() {
    var url = "/crawler_manage/project/api/project_list";
    $('#project-list-table').bootstrapTable({
        method: 'POST',
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded",
        cache: true,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        //data:[{"id":8,"code":"9","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:21.889174Z","update_time":"2017-09-15T15:43:21.889335Z"},{"id":7,"code":"8","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:08.422227Z","update_time":"2017-09-15T15:43:08.422409Z"},{"id":6,"code":"7","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:42:12.488034Z","update_time":"2017-09-15T15:42:12.488139Z"},{"id":5,"code":"6","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:41:48.833986Z","update_time":"2017-09-15T15:41:48.834099Z"},{"id":4,"code":"4","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:39:48.077809Z","update_time":"2017-09-15T15:39:48.077922Z"},{"id":3,"code":"3","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:30:16.145086Z","update_time":"2017-09-15T15:30:16.145190Z"},{"id":2,"code":"2","project_name":"浙江双告知","desc":"sdf电风扇","create_time":"2017-09-15T15:14:39.129643Z","update_time":"2017-09-15T15:14:39.129797Z"},{"id":1,"code":"1","project_name":"工商爬虫","desc":"工商爬虫","create_time":"2017-09-14T14:26:01.990634Z","update_time":"2017-09-14T14:26:01.990716Z"}],
        //height: $(window).height() - 110,
        width: $(window).width(),
        showColumns: true,
        pagination: true,
        queryParams: queryParams,
        queryParamsType: "limit",
        minimumCountColumns: 2,
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        //pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        showExport: false,
        exportDataType: 'all',
        responseHandler: responseHandler,
        columns: [
            {
                field: '',
                title: 'ID',
                formatter: function (value, row, index) {
                    return index + 1;
                }
            },
            {
                field: 'code',
                title: '项目编码',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'project_name',
                title: '项目名称',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'create_time',
                title: '创建时间',
                align: 'center',
                valign: 'middle'
                ,
                formatter: function (value, row, index) {
                    return new Date(value).format('yyyy-MM-dd hh:mm:ss')
                }
            }, {
                field: 'code',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: 'operateFormatter'
            }]
    });
}

function operateFormatter(value, row, index) {
    return '<button type="button" class="btn btn-default" ' +
        'onclick="selectProject(\'' + row['code'] + '\', \''
        + row['project_name'] + '\')">选择</button>'
}
function queryParams(params) {
    var param = {
        limit: params.limit, // 页面大小
        offset: params.offset // 页码
    }
    return param;
}

function selectProject(project_id, project_name) {
    $('#project_id').val(project_id);
    $('#project_name').val(project_name);
    $('#project').val(project_id + ' ---- ' + project_name);
    $('#projectSelectModal').modal('toggle');
}

// 用于server 分页，表格数据量太大的话 不想一次查询所有数据，可以使用server分页查询，数据量小的话可以直接把sidePagination: "server"  改为 sidePagination: "client" ，同时去掉responseHandler: responseHandler就可以了，
function responseHandler(res) {
    if (res) {
        return {
            "rows": res.data,
            "total": res.size
        };
    } else {
        return {
            "rows": [],
            "total": 0
        };
    }
}

function populateFieldSelection(field_mapping) {
    $("#rule_fields").empty();
    $.each($.parseJSON(field_mapping), function(n, obj){
        $("#rule_fields").append('<option value="' + obj.name +'">' + obj.name +'</option>');
    });
}

function populateValidateRulesTable(data) {
    if (validateRuleTableInitialized == false) {
        $('#validate_rules_table').bootstrapTable({
            //method:'POST',
            dataType: 'json',
            contentType: "application/x-www-form-urlencoded",
            cache: true,
            striped: true,                              //是否显示行间隔色
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            //url: url,
            data: data,
            //data:[{"id":8,"code":"9","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:21.889174Z","update_time":"2017-09-15T15:43:21.889335Z"},{"id":7,"code":"8","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:08.422227Z","update_time":"2017-09-15T15:43:08.422409Z"},{"id":6,"code":"7","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:42:12.488034Z","update_time":"2017-09-15T15:42:12.488139Z"},{"id":5,"code":"6","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:41:48.833986Z","update_time":"2017-09-15T15:41:48.834099Z"},{"id":4,"code":"4","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:39:48.077809Z","update_time":"2017-09-15T15:39:48.077922Z"},{"id":3,"code":"3","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:30:16.145086Z","update_time":"2017-09-15T15:30:16.145190Z"},{"id":2,"code":"2","project_name":"浙江双告知","desc":"sdf电风扇","create_time":"2017-09-15T15:14:39.129643Z","update_time":"2017-09-15T15:14:39.129797Z"},{"id":1,"code":"1","project_name":"工商爬虫","desc":"工商爬虫","create_time":"2017-09-14T14:26:01.990634Z","update_time":"2017-09-14T14:26:01.990716Z"}],
            //height: $(window).height() - 110,
            //width:$(window).width(),
            showColumns: false,
            pagination: false,
            queryParams: queryParams,
            queryParamsType: "limit",
            minimumCountColumns: 2,
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 20,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            uniqueId: "uuid",                     //每一行的唯一标识，一般为主键列
            showExport: false,
            exportDataType: 'all',
            responseHandler: responseHandler,
            columns: [
                {
                    field: 'id',
                    title: 'ID',
                    formatter: function (value, row, index) {
                        return index + 1;
                    }
                },
                {
                    field: 'field_name',
                    title: '字段名',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                }, {
                    field: 'desc',
                    title: '规则描述',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                }, {
                    field: 'type',
                    title: '规则类型',
                    align: 'center',
                    valign: 'middle',
                    formatter: function (value, row, index) {
                        switch (value) {
                            case '0':
                                return '正则表达式';
                            case '1':
                                return '日期验证';
                            case '2':
                                return '浮点数验证';
                            case '3':
                                return '整数验证';
                            case '4':
                                return '非空验证';
                        }


                    }
                }, {
                    field: 'rule',
                    title: '规则实现',
                    align: 'center',
                    valign: 'middle',
                    /*formatter: 'operateFormatter'*/
                }, {
                    field: 'uuid',
                    title: '操作',
                    align: 'center',
                    valign: 'middle',
                    formatter: 'ruleOperateFormatter'
                }]
        });
        validateRuleTableInitialized = true;
    } else {
        $('#validate_rules_table').bootstrapTable('removeAll');
    }
}

function ruleOperateFormatter(value, row, index){
    return "<button type=\"button\" class=\"btn btn-default btn-sm\" " +
        " onclick=deleteRow('" + value +"')" +
        ">删除</button>"
}

function deleteRow(value){
    var vls = [];
    vls.push(value);
    $('#validate_rules_table').bootstrapTable('removeByUniqueId', value);
}


function validRuleSelect(type) {
    if(type == 0){ //正则匹配
        $('#rule_label').text('正则表达式');
        $('#rule').attr('placeholder','正则表达式');
        $('#rule').css("display", "block");
        $('#type_select').css('display', 'none');
        $('#rule_type').val(0);
    }else{
         $('#rule_label').text('类型匹配');
        $('#rule').attr('placeholder','类型匹配');
        $('#rule').css('display', 'none');
        $('#type_select').css('display', 'block');
        $('#rule_type').val(1);
    }
}

function resetValidateForm() {
    $("#rule_fields").val('').trigger('change')
    $('#validate_rule_form')[0].reset();
}

function typeSelect(type){
    var rule_type = type;
    //$('#rule').val(rule);
    $('#rule_type').val(rule_type);
}

function validRuleForm(){
    var rule_desc = $('#rule_desc').val();
    var rule_fields = $('#rule_fields').val();
    var rule_type = $('#rule_type').val();
    var rule = $('#rule').val();
    var valid = true;
    if(rule_desc && rule_desc.trim().length <= 0 ){
        valid = false;
        alert_box("error", "规则描述不可以为空");
    }
    if(!rule_fields || rule_fields.length < 0 ){
        valid = false;
        alert_box("error", "请添加字段");
    }
    if(rule_type == '0' && rule.trim().length <= 0) {
        valid = false;
        alert_box("error", "请填写正则表达式")
    }

    return valid;
}

function validAndSaveRule(){
    if(validRuleForm()){
        var rule_fields = $('#rule_fields').val();
        var datas = []
        for(index in rule_fields){
            data = {
                'uuid': Math.uuid(),
                'field_name': rule_fields[index],
                'desc': $('#rule_desc').val(),
                'type': $('#rule_type').val(),
                'rule': $('#rule').val()
            }
            datas.push(data);

        }
        $('#validate_rules_table').bootstrapTable('append', datas);
        $('#validateRuleSelectModal').modal('toggle');
    }
}

function saveRuleAndContinue() {
    if(validRuleForm()){
        var rule_fields = $('#rule_fields').val();
        var datas = []
        for(index in rule_fields){
            data = {
                'uuid': Math.uuid(),
                'field_name': rule_fields[index],
                'desc': $('#rule_desc').val(),
                'type': $('#rule_type').val(),
                'rule': $('#rule_type').val() == '0' ? $('#rule').val() : ""
            }
            datas.push(data);

        }
        $('#validate_rules_table').bootstrapTable('append', datas);
        resetValidateForm();
    }

}



function validateAndSubmitTaskForm() {
    var deploy_target = $("#deploy_target").val();
    var processor_id = $("#processor_id").val();
    var processor_name = $("#processor_name").val();
    var project_id = $("#project_id").val();
    var clean_app = $("#clean_app").val();
    var clean_parameters = $('#clean_parameters').val();
    var field_mapping = $("#field_mapping").val();

    var checkID = /^[A-Za-z0-9_-]+$/;
    validate = false;

    if(processor_id == null || processor_id.trim().length <=0){
        alert_box('error','请填写清洗程序编码！');
        return;
    }else if(!checkID.test(processor_id)){
        alert_box('error','清洗程序编码只能是字母、数字、下划线！');
        return;
    }

    if(processor_name == null || processor_name.trim().length <=0){
        alert_box('error','请填写清洗程序名字！');
        return;
    }

    if(project_id == null || project_id.trim().length <=0){
        alert_box('error','请选择项目！');
        return;
    }else if(!checkID.test(project_id)){
        alert_box('error','项目编码只能是字母、数字、下划线、中横线！');
        return;
    }

    // if(clean_app == null || clean_app.trim().length <=0){
    //     alert_box('error','请上传清洗程序！');
    //     return;
    // }


    var checkClean = /^[a-z][a-zA-Z0-9_]*(\.[a-z][a-zA-Z0-9_]*)*\.[A-Z][a-zA-Z0-9_]*/;

    if(clean_parameters.length <= 0) {
        alert_box("error", "请填写清洗程序的类名，包含包名");
        return;
    }
    else if (clean_parameters.length>0 && !checkClean.test(clean_parameters)){
        alert_box("error", "请填写正确的类名，包含包名");
        return;
    }

    if(!isJsonFormat(field_mapping)){
        alert_box('error', '字段映射必须是json格式，如：[{"name":"f1", "type":"int", "doc": "描述", "default": "默认值"}, {"name": "f2", "type": "string", "doc": "描述", "default": "默认值"}]');
        return;
    }

    var data = $('#validate_rules_table').bootstrapTable('getData')
    $('#validate_rules').val(JSON.stringify(data));


    if(deploy_target == null || deploy_target.trim().length <= 0 )
    {
        alert_box("error", "请填写发布目标！");
        return;
    }

    var check_deploy_target = /^[\w-]+:[\w-]+\/[\w-]+(,[\w-]+:[\w-]+\/[\w-]+)*$/;
    if(!check_deploy_target.test(deploy_target)){
        alert_box("error", "请填写正确索引名和类型名，多个资源用逗号分割");
        return;
    }

    $('#processor_form').submit();
}