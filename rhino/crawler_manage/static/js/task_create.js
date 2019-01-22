/**
 * Created by linshirong on 2017/9/18.
 */

validateRuleTableInitialized = false;

function resetForm() {
    $('.form-horizontal')[0].reset()
    $('#task_detail_div').removeClass('in');
    $('#detail_field_mapping_table').bootstrapTable('removeAll');
    $('#confirmModal').modal('toggle');
}

// 选择爬虫
function showSelectCrawlerModal() {
    $('#crawlerSelectModal').modal('show');
    populateCrawlerListTable();
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
        $('#validate_rules_table').bootstrapTable('append', data);
    }
}

function populateCrawlerListTable() {
    var url = "/crawler_manage/crawler/api/crawler_list";
    $('#crawler-list-table').bootstrapTable({
        method: 'POST',
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded",
        cache: true,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        //data:[{"id":8,"code":"9","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:21.889174Z","update_time":"2017-09-15T15:43:21.889335Z"},{"id":7,"code":"8","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:08.422227Z","update_time":"2017-09-15T15:43:08.422409Z"},{"id":6,"code":"7","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:42:12.488034Z","update_time":"2017-09-15T15:42:12.488139Z"},{"id":5,"code":"6","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:41:48.833986Z","update_time":"2017-09-15T15:41:48.834099Z"},{"id":4,"code":"4","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:39:48.077809Z","update_time":"2017-09-15T15:39:48.077922Z"},{"id":3,"code":"3","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:30:16.145086Z","update_time":"2017-09-15T15:30:16.145190Z"},{"id":2,"code":"2","project_name":"浙江双告知","desc":"sdf电风扇","create_time":"2017-09-15T15:14:39.129643Z","update_time":"2017-09-15T15:14:39.129797Z"},{"id":1,"code":"1","project_name":"工商爬虫","desc":"工商爬虫","create_time":"2017-09-14T14:26:01.990634Z","update_time":"2017-09-14T14:26:01.990716Z"}],
        //height: $(window).height() - 110,
        //width:$(window).width(),
        showColumns: false,
        pagination: true,
        queryParams: queryParams,
        queryParamsType: "limit",
        minimumCountColumns: 2,
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 20,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
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
                field: 'id',
                title: '爬虫编码',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'crawler_name',
                title: '爬虫名称',
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                field: 'create_time',
                title: '创建时间',
                align: 'center',
                valign: 'middle',
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

function ruleOperateFormatter(value, row, index) {
    return "<button type=\"button\" class=\"btn btn-default btn-sm\" " +
        " onclick=deleteRow('" + value + "')" +
        ">删除</button>"
}

function deleteRow(value) {
    var vls = [];
    vls.push(value);
    $('#validate_rules_table').bootstrapTable('removeByUniqueId', value);
}

function operateFormatter(value, row, index) {
    return '<button type="button" class="btn btn-default btn-sm" ' +
        'onclick="selectCrawler(\'' + row['id'] + '\', \''
        + row['project_name'] + '\')">选择</button>'
}

function populateFieldMappingTable(data) {
    if (detail_field_mapping_table_exists == null || detail_field_mapping_table_exists == false) {
        $('#detail_field_mapping_table').bootstrapTable({
            //method:'POST',
            dataType: 'json',
            contentType: "application/x-www-form-urlencoded",
            cache: true,
            striped: true,                              //是否显示行间隔色
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            //url: url,
            data: data,
            //data:[{"id":8,"code":"9","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:21.889174Z","update_time":"2017-09-15T15:43:21.889335Z"},{"id":7,"code":"8","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:08.422227Z","update_time":"2017-09-15T15:43:08.422409Z"},{"id":6,"code":"7","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:42:12.488034Z","update_time":"2017-09-15T15:42:12.488139Z"},{"id":5,"code":"6","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:41:48.833986Z","update_time":"2017-09-15T15:41:48.834099Z"},{"id":4,"code":"4","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:39:48.077809Z","update_time":"2017-09-15T15:39:48.077922Z"},{"id":3,"code":"3","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:30:16.145086Z","update_time":"2017-09-15T15:30:16.145190Z"},{"id":2,"code":"2","project_name":"浙江双告知","desc":"sdf电风扇","create_time":"2017-09-15T15:14:39.129643Z","update_time":"2017-09-15T15:14:39.129797Z"},{"id":1,"code":"1","project_name":"工商爬虫","desc":"工商爬虫","create_time":"2017-09-14T14:26:01.990634Z","update_time":"2017-09-14T14:26:01.990716Z"}],
            //height: $(window).height() - 250,
            //width:$(window).width(),
            showColumns: false,
            pagination: false,
            queryParams: queryParams,
            queryParamsType: "limit",
            minimumCountColumns: 2,
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 1000,                       //每页的记录行数（*）
            //pageList: [10, 20],        //可供选择的每页的行数（*）
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
                    field: 'name',
                    title: '字段名',
                    align: 'center',
                    valign: 'middle'
                }, {
                    field: 'doc',
                    title: '字段描述',
                    align: 'center',
                    valign: 'middle'
                }, {
                    field: 'type',
                    title: '类型',
                    align: 'center',
                    valign: 'middle'
                }, {
                    field: 'default',
                    title: '默认值',
                    align: 'center',
                    valign: 'middle'
                }]
        });
        detail_field_mapping_table_exists = true;
    }
    else {
        detail_field_mapping_table_exists = true;
        $('#detail_field_mapping_table').bootstrapTable('load', data);
    }

}

function populateCrawlerDetailForm(crawlerData) {
    $('#crawler_id').val(crawlerData.id);
    $('#crawler_name').val(crawlerData.crawler_name);
    $('#project_id').val(crawlerData.project_id);
    $('#project_name').val(crawlerData.project_name);
    $('#crawler_app').val(crawlerData.crawler_app);
    $('#clean_app').val(crawlerData.clean_app);
    $('#clean_parameters').val(crawlerData.clean_parameters);
    if (crawlerData.clean_method == 'common') {
        $('#processor_id').val(crawlerData.processor_id);
        $('#processor_name').val(crawlerData.processor_name);
        $('#deploy_target').val(crawlerData.deploy_target);
    }else{
        $('#processor_id').val('');
        $('#processor_name').val('');
        $('#deploy_target').val('');
    }

    //$('#detail_field_mapping').val(crawlerData.fields_mapping);
    //$('#detail_create_time').val(crawlerData.create_time);
    //$('#detail_update_time').val(crawlerData.update_time);
}

function selectCrawler(crawlerId) {

    var crawlerDetail = $('#crawler-list-table').bootstrapTable('getRowByUniqueId', crawlerId);
    crawler_data = crawlerDetail;
    populateCrawler(crawler_data);
    $('#crawlerSelectModal').modal('toggle');

}

function populateCrawler(crawlerDetail) {
    populateCrawlerDetailForm(crawlerDetail);
    var field_mapping = crawlerDetail.fields_mapping;
    populateFieldMappingTable($.parseJSON(field_mapping));
    var validateRules = [];


    populateFieldSelection(field_mapping);

    if (crawlerDetail.clean_method == 'common') {
        $('#processor_panel').addClass("in");
        $('#processor_panel').css("display", "block");
        $('#deploy_target').attr("readonly","readonly")
        validateRules = $.parseJSON(crawler_data['validate_rules']);
        $('#clean_method_1').css("display", "none");
        $('#clean_method_2').css("display", "block");
    }else{
        $('#processor_panel').removeClass("in");
        $('#processor_panel').css("display", "none");
        $('#deploy_target').removeAttr("readonly")
        $('#clean_method_2').css("display", "none");
        $('#clean_method_1').css("display", "block");
    }

    populateValidateRulesTable(validateRules);
    $('#task_detail_div').addClass('in');

}

function populateFieldSelection(field_mapping) {
    $("#rule_fields").empty();
    $.each($.parseJSON(field_mapping), function (n, obj) {
        $("#rule_fields").append('<option value="' + obj.name + '">' + obj.name + '</option>');
    });
}
function queryParams(params) {
    var param = {
        limit: params.limit, // 页面大小
        offset: params.offset // 页码
    }
    return param;
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

function validateAndSubmitTaskForm() {
    deploy_target = $("#deploy_target").val();
    crawler_id = $("#crawler_id").val();

    if (crawler_id == null || crawler_id.trim().length <= 0) {
        alert_box('error', '请选择爬虫！');
        return;
    }

    if (deploy_target == null || deploy_target.trim().length <= 0) {
        alert_box("error", "请填写发布目标！");
        return;
    }

    var checkID = /^[\w-]+:[\w-]+\/[\w-]+(,[\w-]+:[\w-]+\/[\w-]+)*$/;
    if (!checkID.test(deploy_target)) {
        alert_box("error", "请填写正确索引名和类型名，多个资源用逗号分割");
        return;
    }
    var checkParam = /^([A-Za-z0-9_-]+=[A-Za-z0-9_-]+,?)*$/;
    var crawler_parameters = $('#crawler_parameters').val();
    var clean_parameters = $('#clean_parameters').val();
    if (!checkParam.test(crawler_parameters.replace(/\s/g), '')) {
        alert_box("error", "请填写正确的参数，多个参数用逗号分割");
        return;
    }
    var checkClean = /^[a-z][a-zA-Z0-9_]*(\.[a-z][a-zA-Z0-9_]*)*\.[A-Z][a-zA-Z0-9_]*/;

    if (clean_parameters.length > 0 && !checkClean.test(clean_parameters)) {
        alert_box("error", "请填写正确的类名，包含包名");
        return;
    }

    var data = $('#validate_rules_table').bootstrapTable('getData')
    $('#validate_rules').val(JSON.stringify(data));

    $('#task_form').submit();

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

function validRuleSelect(type) {
    if (type == 0) { //正则匹配
        $('#rule_label').text('正则表达式');
        $('#rule').attr('placeholder', '正则表达式');
        $('#rule').css("display", "block");
        $('#type_select').css('display', 'none');
        $('#rule_type').val(0);
    } else {
        $('#rule_label').text('类型匹配');
        $('#rule').attr('placeholder', '类型匹配');
        $('#rule').css('display', 'none');
        $('#type_select').css('display', 'block');
        $('#rule_type').val(1);
    }
}

function resetValidateForm() {
    $("#rule_fields").val('').trigger('change')
    $('#validate_rule_form')[0].reset();
}

function typeSelect(type) {
    var rule_type = type;
    //$('#rule').val(rule);
    $('#rule_type').val(rule_type);
}

function validRuleForm() {
    var rule_desc = $('#rule_desc').val();
    var rule_fields = $('#rule_fields').val();
    var rule_type = $('#rule_type').val();
    var rule = $('#rule').val();
    var valid = true;
    if (rule_desc && rule_desc.trim().length <= 0) {
        valid = false;
        alert_box("error", "规则描述不可以为空");
    }
    if (!rule_fields || rule_fields.length < 0) {
        valid = false;
        alert_box("error", "请添加字段");
    }
    if (rule_type == '0' && rule.trim().length <= 0) {
        valid = false;
        alert_box("error", "请填写正则表达式")
    }

    return valid;
}

function validAndSaveRule() {
    if (validRuleForm()) {
        var rule_fields = $('#rule_fields').val();
        var datas = []
        for (index in rule_fields) {
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
    if (validRuleForm()) {
        var rule_fields = $('#rule_fields').val();
        var datas = []
        for (index in rule_fields) {
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