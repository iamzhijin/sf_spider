/**
 * Created by linshirong on 2017/9/16.
 */

processor_list_table_init = false;

function resetForm() {
    $('.form-horizontal')[0].reset()
    $('#custom-clean-panel').addClass('in');
    $('#custom-clean-panel').css('display', 'block');
    $('#common-clean-panel').removeClass('in');
    $('#common-clean-panel').css('display', 'none');
    $('#confirmModal').modal('toggle');
}


function project_select() {
    $('#projectSelectModal').modal('show');
    initTable();
}

function initTable() {
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
        uniqueId: "code",                     //每一行的唯一标识，一般为主键列
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

function processorOperateFormatter(value, row, index) {
    return '<button type="button" class="btn btn-default" ' +
        'onclick="selectProcessor(\'' + row['id'] + '\', \''
        + row['processor_name'] + '\')">选择</button>'
}

function queryParams(params) {
    var param = {
        limit: params.limit, // 页面大小
        offset: params.offset // 页码
    }
    return param;
}

function processorQueryParams(params) {
    var param = {
        limit: params.limit, // 页面大小
        offset: params.offset, // 页码
        check_status: false,
        project_id: $('#project_id').val()
    }
    return param;
}


function selectProject(project_id, project_name) {
    $('#project_id').val(project_id);
    $('#project_name').val(project_name);
    $('#project').val(project_id + ' ---- ' + project_name);
    $('#projectSelectModal').modal('toggle');
}

function selectProcessor(processor_id, processor_name) {
    var row = $('#processor-list-table').bootstrapTable('getRowByUniqueId', processor_id);
    $('#processor_id').val(processor_id);
    $('#processor_name').val(processor_name);
    $('#processor').val(processor_id + ' ---- ' + processor_name);
    $('#processorSelectModal').modal('toggle');

    $('#common_clean_app').val(row['clean_app']);
    $('#common_deploy_target').val(row['deploy_target']);
    $('#common_clean_parameters').val(row['clean_parameters']);
    document.getElementById("common_field_mapping").value= row['fields_mapping'];



    $('#deploy_target_panel').css("display", "block");
    $('#class_panel').css("display", "block");
    $('#field_panel').css("display", "block");
    $('#clean_panel').css("display", "block");

    $('#deploy_target_panel').addClass("in");
    $('#class_panel').addClass("in");
    $('#field_panel').addClass("in");
    $('#clean_panel').addClass("in");
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

function choose_clean_method(method) {
    if (method == 1) {
        //使用自定义程序
        $('#custom-clean-panel').addClass('in');
        $('#custom-clean-panel').css('display', 'block');
        $('#common-clean-panel').removeClass('in');
        $('#common-clean-panel').css('display', 'none');
    } else {
        //使用通用程序
        $('#common-clean-panel').addClass('in');
        $('#common-clean-panel').css('display', 'block');
        $('#custom-clean-panel').removeClass('in');
        $('#custom-clean-panel').css('display', 'none');
    }
}


function processor_select() {
    //如果项目没有选择，则报错
    if ($('#project_name').val().trim().length <= 0) {
        alert_box('error', '请先选择项目');
        return;
    }
    //弹出处理程序选择modal
    $('#processorSelectModal').modal('show');
    initProcessorTable();
}

function validateAndSubmitForm() {
    var project_id = $("#project_id").val();
    var processor_id = $("#processor_id").val();
    var crawler_id = $("#crawler_id").val();
    var crawler_name = $("#crawler_name").val();
    var crawler_app = $("#crawler_app").val();
    var field_mapping = $("#field_mapping").val();
    var need_clean = $("#need_clean").val();
    var clean_app = $("#clean_app").val();
    var clean_parameters = $('#clean_parameters').val();
    // var clean_method = $('clean_method').val();
    var clean_method = $('input[name="clean_method"]:checked').val();
    // 新增字段
    // var web_title = $("#web_title").val();
    // var web_url = $("#web_url").val();
    // var update_strategy = $("#update_strategy").val();
    // var use_for = $("#use_for").val();
    // var crawl_owner = $("#crawl_owner").val();
    // var count = $("#count").val();
    // var time_limit = $("#time_limit").val();
    // var source = $("#source").val();

    var checkID = /^[A-Za-z0-9_-]+$/;
    validate = false;
    if (project_id == null || project_id.trim().length <= 0) {
        alert_box('error', '请选择项目！');
        return;
    } else if (!checkID.test(project_id)) {
        alert_box('error', '项目编码只能是字母、数字、下划线、中横线！');
        return;
    }
    if (crawler_id == null || crawler_id.trim().length <= 0) {
        alert_box('error', '请填写爬虫编码！');
        return;
    } else if (!checkID.test(crawler_id)) {
        alert_box('error', '爬虫编码只能是字母、数字、下划线、中横线！');
        return;
    }
    if (crawler_name == null || crawler_name.trim().length <= 0) {
        alert_box('error', '爬虫名字不可以为空！');
        return;
    }
    if (crawler_app == null || crawler_app.trim().length <= 0) {
        alert_box('error', '请上传爬虫程序！');
        return;
    }
    if(clean_method == 'custom') {

        if (!isJsonFormat(field_mapping)) {
            alert_box('error', '字段映射必须是json格式，如：[{"name":"f1", "type":"int", "doc": "描述", "default": "默认值"}, {"name": "f2", "type": "string", "doc": "描述", "default": "默认值"}]');
            return;
        }
        var checkClean = /^[a-z][a-zA-Z0-9_]*(\.[a-z][a-zA-Z0-9_]*)*\.[A-Z][a-zA-Z0-9_]*/;

        if (clean_parameters.length > 0 && !checkClean.test(clean_parameters)) {
            alert_box("error", "请填写正确的类名，包含包名");
            return;
        }
    }

    else {
        if(processor_id == null || processor_id.trim().length <= 0){
            alert_box('error', '请选择通用清洗程序！');
            return;
        }

    }


    $("#project_id").val(project_id.trim());
    $("#crawler_id").val(crawler_id.trim());
    $("#crawler_name").val(crawler_name.trim());
    $("#field_mapping").val(field_mapping.trim());
    $("#clean_parameters").val(clean_parameters.trim());

    // $("#web_title").val(web_title.trim());
    // $("#web_url").val(web_url.trim());
    // $("#update_strategy").val(update_strategy.trim());
    // $("#use_for").val(use_for.trim());
    // $("#crawl_owner").val(crawl_owner.trim());
    // $("#count").val(count.trim());
    // $("#time_limit").val(time_limit.trim());
    // $("#source").val(source.trim());

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

function initProcessorTable() {
    var url = "/crawler_manage/processor/api/list";
    if (processor_list_table_init == false) {
        $('#processor-list-table').bootstrapTable({
            method: 'POST',
            dataType: 'json',
            contentType: "application/x-www-form-urlencoded",
            cache: false,
            striped: true,                              //是否显示行间隔色
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            url: url,
            //data:[{"id":8,"code":"9","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:21.889174Z","update_time":"2017-09-15T15:43:21.889335Z"},{"id":7,"code":"8","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:08.422227Z","update_time":"2017-09-15T15:43:08.422409Z"},{"id":6,"code":"7","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:42:12.488034Z","update_time":"2017-09-15T15:42:12.488139Z"},{"id":5,"code":"6","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:41:48.833986Z","update_time":"2017-09-15T15:41:48.834099Z"},{"id":4,"code":"4","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:39:48.077809Z","update_time":"2017-09-15T15:39:48.077922Z"},{"id":3,"code":"3","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:30:16.145086Z","update_time":"2017-09-15T15:30:16.145190Z"},{"id":2,"code":"2","project_name":"浙江双告知","desc":"sdf电风扇","create_time":"2017-09-15T15:14:39.129643Z","update_time":"2017-09-15T15:14:39.129797Z"},{"id":1,"code":"1","project_name":"工商爬虫","desc":"工商爬虫","create_time":"2017-09-14T14:26:01.990634Z","update_time":"2017-09-14T14:26:01.990716Z"}],
            //height: $(window).height() - 110,
            width: $(window).width(),
            showColumns: true,
            pagination: false,
            queryParams: processorQueryParams,
            queryParamsType: "limit",
            minimumCountColumns: 2,
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 100,                       //每页的记录行数（*）
            //pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            showExport: false,
            exportDataType: 'all',
            //responseHandler: responseHandler,
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
                    title: '清洗程序编码',
                    align: 'center',
                    valign: 'middle',
                    sortable: true
                }, {
                    field: 'processor_name',
                    title: '清洗程序名称',
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
                    field: 'id',
                    title: '操作',
                    align: 'center',
                    valign: 'middle',
                    formatter: 'processorOperateFormatter'
                }]
        });
        processor_list_table_init = true;
    } else {
        var param = {
            check_status: false,
            project_id: $('#project_id').val()
        };
        $('#processor-list-table').bootstrapTable('refresh', param);
    }
}