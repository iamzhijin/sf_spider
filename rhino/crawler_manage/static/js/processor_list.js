validateRuleTableInitialized = false;
detail_field_mapping_table_exists = false;


function populateProcessorListTable() {
    var url = "/crawler_manage/processor/api/list";
    $('#processor-list-table').bootstrapTable({
        method: 'POST',
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded",
        cache: false,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        //height: $(window).height() - 200,
        width: $(window).width(),
        showColumns: false,
        pagination: true,
        queryParams: queryParams,
        queryParamsType: "limit",
        minimumCountColumns: 2,
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        showExport: true,
        exportDataType: 'all',
        responseHandler: responseHandler,
        rowStyle: rowStyle,
        onExpandRow: showTaskServerStatus,
        //detailView: true,
        dataDetailView: "true",
        columns: [
            {
                field: '',
                title: '序号',
                formatter: function (value, row, index) {
                    return index;
                },
                width: '6%',
            },
            {
                field: 'id',
                title: '清洗程序ID',
                align: 'center',
                valign: 'middle',
                width: '18%',

            }, {
                field: 'processor_name',
                title: '清洗程序名称',
                align: 'center',
                valign: 'middle',
                width: '18%',
            }, {
                field: 'project_name',
                title: '数据项目',
                align: 'center',
                valign: 'middle',
                width: '18%',
            }, {
                field: 'id',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: operatorFormatter,
                width: '16%',
            }
            /**, {
                field: 'id',
                title: '爬虫运行',
                align: 'center',
                valign: 'middle',
                formatter: crawlerTaskListStatus,
                width: '8%',
            }**/
            , {
                field: 'id',
                title: '数据备份',
                align: 'center',
                valign: 'middle',
                formatter: backupOperatorFormatter,
                width: '8%',
            }, {
                field: 'id',
                title: '清洗上线',
                align: 'center',
                valign: 'middle',
                formatter: cleanOperatorFormatter,
                width: '8%',
            }]
    });
}

function showTaskServerStatus(index, row, $detail) {
    var task_id = row['id']
    var url = '/crawler_manage/task/api/status/' + task_id
    $el = $detail.html('<table></table>').find('table')
    $el.bootstrapTable({
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded",
        cache: false,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        showColumns: false,
        responseHandler: responseHandler,

        method: 'GET',

        columns: [
            {
                field: '',
                title: '序号',
                formatter: function (value, row, index) {
                    return index;
                },
                width: '6%',
            },
            {
                field: 'host',
                title: '服务器地址',
                align: 'center',
                valign: 'middle',
                width: '18%',
            }, {
                field: 'port',
                title: '服务器端口',
                align: 'center',
                valign: 'middle',
                width: '18%',
            }, {
                field: 'status',
                title: '爬虫状态',
                align: 'center',
                valign: 'middle',
                formatter: crawlerOperatorFormatter,
                width: '16%',
            }]

    });
}

function refreshTable() {
    sk = $('#search_keyword').val().trim();
    p_id = $('#project_id').val().trim();
    params = {
        query: {
            limit: 10,
            offset: 0,
            search_keyword: sk,
            project_id: p_id
        }
    };
    $('#task-list-table').bootstrapTable('refresh', params);    //刷新表格
}

function project_filter(project_id, project_name) {
    $('#project_id').val(project_id);
    if (project_id.length <= 0)
        $('#dropdownMenu1').html('所有数据项目 <span class="caret"></span>');
    else
        $('#dropdownMenu1').html(project_id + ' ---- ' + project_name + ' <span class="caret"></span>');
    refreshTable();
}

function responseHandler2(res) {
    if (res) {
        return {
            "rows": res,
            "total": res.size
        };
    } else {
        return {
            "rows": [],
            "total": 0
        };
    }
}

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


function queryParams(params) {
    var param = {
        limit: params.limit, // 页面大小
        offset: params.offset, // 页码
        search_keyword: $('#search_keyword').val().trim()
    }
    return param;
}

function rowStyle(row, index) {
    var classes = ['active', 'success', 'info', 'warning', 'danger'];
    if (index % 2 === 1) {
        return {
            classes: classes[1]
        };
    }
    return {};
}

/**
 * 按钮开关
 * @param type 按钮类型，1为爬虫程序，2为数据备份，3为清洗上线
 * @param task_id 任务id
 * @param on_or_off 开或者关，字符串类型，"on" "off"
 */
function buttonSwitch(type, task_id, on_or_off) {

    var url = "";
    var btn = "";
    switch (type) {
        case 1:
            if (on_or_off == "on")
                url = "/crawler_manage/task/crawler_start/" + task_id;
            else
                url = "/crawler_manage/task/crawler_stop/" + task_id;
            btn = "crawlerOperator_" + task_id;
            break;
        case 2:
            if (on_or_off == "on")
                url = "/crawler_manage/task/backup_start/" + task_id;
            else
                url = "/crawler_manage/task/backup_stop/" + task_id;
            btn = "backupOperator_" + task_id;
            break;
        case 3:
            if (on_or_off == "on")
                url = "/crawler_manage/processor/start/" + task_id;
            else
                url = "/crawler_manage/processor/stop/" + task_id;
            btn = "cleanOperator_" + task_id;
            break;
    }
    $.ajax({
        url: url,
        type: "get",
        success: function (result) {
            //alert(result);
            if (result.code == true) {
                btnStyleSwitch(btn, on_or_off);
                alert_box("success", result.msg);
            }
            else
                alert_box("error", result.msg);
        },
        error: function (result) {
            alert_box("error", result.msg);
        },
        dataType: 'json',
        timeout: 60 * 1000,

    });


}

function btnStyleSwitch(btn, on_or_off) {
    var should_hide_btn_name = "";
    var should_show_btn_name = "";
    if (on_or_off == "on") {
        should_hide_btn_name = "start_" + btn;
        should_show_btn_name = "stop_" + btn;
    } else {
        should_hide_btn_name = "stop_" + btn;
        should_show_btn_name = "start_" + btn;
    }
    $('#' + should_hide_btn_name).css("display", "none");
    $('#' + should_show_btn_name).css("display", "inherit");
}

function operatorFormatter(value, row, index) {
    return '<button type="button" class="btn btn-default btn-xs btn-info" style="margin-right:5px;" ' +
        'onclick="showProcessor(\'' + row['id'] + '\')">查看</button>' +
        '<button type="button" class="btn btn-default  btn-xs btn-warning" style="margin-right:5px;" ' +
        'onclick="editProcessor(\'' + row['id'] + '\')">修改</button>' + 
        '<button type="button" class="btn btn-default  btn-xs btn-danger" data-toggle="modal" data-target="#confirmModal" style="margin-right:5px;" ' +
        'data-value = \'' + row['id'] + '\'>删除</button>';
}

function showProcessor(processor_id) {
    if (populateProcessorDetail(processor_id))
        $('#processorDetailModal').modal('show');
}

function populateProcessorDetail(processor_id) {
    var url = "/crawler_manage/processor/api/detail/" + processor_id
    var success = true;
    $.ajax({
        url: url,
        type: "get",
        async: false,
        success: function (result) {
            //alert(result);
            if (result.code == true) {
                $('#processor_detail_id').val(result.data.id);
                $('#processor_detail_name').val(result.data.processor_name);
                $('#processor_detail_project_id').val(result.data.project_id);
                $('#processor_detail_project_name').val(result.data.project_name);
                $('#processor_detail_clean_parameters').val(result.data.clean_parameters);
                $('#processor_detail_deploy_target').val(result.data.deploy_target);


                var download_clean_app_url = "/download/" + result.data.clean_app
                var clean_app_filename=result.data.clean_app.replace(/.*(\/|\\)/, "");
                if(clean_app_filename != null && clean_app_filename.length > 0) {
                    $('#download_clean_app').attr("href", download_clean_app_url);
                    $('#download_clean_app').css("display","block");
                }else
                {
                    $('#download_clean_app').css("display","none");
                }


                $('#processor_detail_clean_app').val(clean_app_filename);

                populateFieldMappingTable(JSON.parse(result.data.fields_mapping));
                if(result.data.validate_rules)
                    populateValidateRulesTable(result.data.validate_rules);
                /*                $('#task_detail_id').val(result.data.id);
                 $('#task_detail_id').val(result.data.id);*/
            }
            else {
                success = false;
                alert_box("error", result.msg);
            }
        },
        error: function (result) {
            alert_box("error", '查看任务详情失败');
            success = false;
        },
        dataType: 'json',
        timeout: 60 * 1000,

    });

    return success;

}

function editProcessor(processor_id) {
    $(window.location).attr('href', '/crawler_manage/processor/edit/' + processor_id);
}

$(function () {
    $('#confirmModal').on('show.bs.modal', function (e) {
        var btn = $(e.relatedTarget);
        processor_id = btn.data("value")
        var url = "/crawler_manage/processor/" + processor_id + "/crawlers";
        $.ajax({
            url: url,
            type: "get",
            cache: false,
            success: function (result) {
                if (result.code == true) {
                    $('.alert-text').text(result.msg)
                    $('#button').attr('value', result.tasks)
                    var tasks = $('#button').attr('value')
                    //     if (tasks == 0) {
                    //         console.log("可以删除爬虫..")
                    //     } else {
                    //         console.log("不可以删除爬虫")
                    //     }
                }
            },
            error: console.log('删除失败...'),
            dataType: 'json',
            timeout: 60 * 1000,
        });
    })
});


function deleteProcessor(processorId, tasks) {
    if (tasks == 0) {
        console.log('删除清洗程序...')
        var url = "/crawler_manage/processor/delete/" + processorId;
        $.ajax({
            url: url,
            type: "get",
            cache: false,
            success: function (result) {
                if (result.code == true) {
                    console.log('删除清洗程序成功...')
                } else {
                    console.log('删除清洗程序失败...')
                }
            },
            error: console.log('删除清洗程序失败...'),
            dataType: 'json',
            timeout: 60 * 1000,
        });
        $('#confirmModal').modal('toggle');
        window.location.reload();
    }
    else {
        console.log('直接关闭模态框')
        $('#confirmModal').modal('toggle');
    }
}

function backupOperatorFormatter(value, row, index) {
    if (row['clean_app_status'] == 0)
        return '<button type="button" id="start_backupOperator_' + row['id'] + '" class="btn btn-default btn-xs btn-primary glyphicon glyphicon-play" ' +
            'onclick="buttonSwitch(2, \'' + row['id'] + '\', \'on\')">启动</button>' +
            '<button type="button" id="stop_backupOperator_' + row['id'] + '" class="btn btn-default  btn-xs btn-danger glyphicon glyphicon-stop" style="display: none;" ' +
            'onclick="buttonSwitch(2, \'' + row['id'] + '\', \'off\')">停止</button>';
    else if (row['clean_app_status'] == 1)
        return '<button type="button" id="start_backupOperator_' + row['id'] + '" class="btn btn-default btn-xs btn-primary glyphicon glyphicon-play" style="display: none;" ' +
            'onclick="buttonSwitch(2, \'' + row['id'] + '\', \'on\')">启动</button>' +
            '<button type="button" id="stop_backupOperator_' + row['id'] + '" class="btn btn-default  btn-xs btn-danger glyphicon glyphicon-stop"  ' +
            'onclick="buttonSwitch(2, \'' + row['id'] + '\', \'off\')">停止</button>';
    else
        return null;
}

function cleanOperatorFormatter(value, row, index) {

    if (row['clean_app_status'] == 0)
        return '<button type="button" id="start_cleanOperator_' + row['id'] + '" class="btn btn-default btn-xs btn-primary glyphicon glyphicon-play" ' +
            'onclick="buttonSwitch(3, \'' + row['id'] + '\', \'on\')">启动</button>' +
            '<button type="button" id="stop_cleanOperator_' + row['id'] + '" class="btn btn-default  btn-xs btn-danger glyphicon glyphicon-stop" style="display: none;" ' +
            'onclick="buttonSwitch(3, \'' + row['id'] + '\', \'off\')">停止</button>';
    else if (row['clean_app_status'] == 1)
        return '<button type="button" id="start_cleanOperator_' + row['id'] + '" class="btn btn-default btn-xs btn-primary glyphicon glyphicon-play" style="display: none;" ' +
            'onclick="buttonSwitch(3, \'' + row['id'] + '\', \'on\')">启动</button>' +
            '<button type="button" id="stop_cleanOperator_' + row['id'] + '" class="btn btn-default  btn-xs btn-danger glyphicon glyphicon-stop"  ' +
            'onclick="buttonSwitch(3, \'' + row['id'] + '\', \'off\')">停止</button>';
    else
        return null;
}


function populateFieldMappingTable(data) {
    if (detail_field_mapping_table_exists == null || detail_field_mapping_table_exists == false) {
        $('#processor_detail_field_mapping_table').bootstrapTable({
            //method:'POST',
            dataType: 'json',
            contentType: "application/x-www-form-urlencoded",
            cache: false,
            striped: true,                              //是否显示行间隔色
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            //url: url,
            data: data,
            //data:[{"id":8,"code":"9","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:21.889174Z","update_time":"2017-09-15T15:43:21.889335Z"},{"id":7,"code":"8","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:08.422227Z","update_time":"2017-09-15T15:43:08.422409Z"},{"id":6,"code":"7","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:42:12.488034Z","update_time":"2017-09-15T15:42:12.488139Z"},{"id":5,"code":"6","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:41:48.833986Z","update_time":"2017-09-15T15:41:48.834099Z"},{"id":4,"code":"4","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:39:48.077809Z","update_time":"2017-09-15T15:39:48.077922Z"},{"id":3,"code":"3","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:30:16.145086Z","update_time":"2017-09-15T15:30:16.145190Z"},{"id":2,"code":"2","project_name":"浙江双告知","desc":"sdf电风扇","create_time":"2017-09-15T15:14:39.129643Z","update_time":"2017-09-15T15:14:39.129797Z"},{"id":1,"code":"1","project_name":"工商爬虫","desc":"工商爬虫","create_time":"2017-09-14T14:26:01.990634Z","update_time":"2017-09-14T14:26:01.990716Z"}],
            //height: $(window).height() - 250,
            width: $(window).width(),
            //showColumns:true,
            //pagination:true,
            //queryParams : queryParams,
            queryParamsType: "limit",
            minimumCountColumns: 2,
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 1000,                       //每页的记录行数（*）
            //pageList: [10, 20],        //可供选择的每页的行数（*）
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            //showExport: true,
            //exportDataType: 'all',
            //responseHandler: responseHandler2,
            columns: [
                {
                    field: '',
                    title: 'ID',
                    formatter: function (value, row, index) {
                        return index + 1;
                    },
                    width: '5%'
                },
                {
                    field: 'name',
                    title: '字段名',
                    align: 'center',
                    valign: 'middle',
                    width: '10%'
                }, {
                    field: 'doc',
                    title: '字段描述',
                    align: 'center',
                    valign: 'middle',
                    width: '30%'
                }, {
                    field: 'type',
                    title: '类型',
                    align: 'center',
                    valign: 'middle',
                    width: '15%'
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
        $('#task_detail_field_mapping_table').bootstrapTable('load', data);
    }

}


function populateValidateRulesTable(data) {
    if (validateRuleTableInitialized == false) {
        $('#processor_detail_validate_rules_table').bootstrapTable({
            //method:'POST',
            dataType: 'json',
            contentType: "application/x-www-form-urlencoded",
            cache: false,
            striped: true,                              //是否显示行间隔色
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            //url: url,
            data: data,
            //data:[{"id":8,"code":"9","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:21.889174Z","update_time":"2017-09-15T15:43:21.889335Z"},{"id":7,"code":"8","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:08.422227Z","update_time":"2017-09-15T15:43:08.422409Z"},{"id":6,"code":"7","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:42:12.488034Z","update_time":"2017-09-15T15:42:12.488139Z"},{"id":5,"code":"6","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:41:48.833986Z","update_time":"2017-09-15T15:41:48.834099Z"},{"id":4,"code":"4","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:39:48.077809Z","update_time":"2017-09-15T15:39:48.077922Z"},{"id":3,"code":"3","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:30:16.145086Z","update_time":"2017-09-15T15:30:16.145190Z"},{"id":2,"code":"2","project_name":"浙江双告知","desc":"sdf电风扇","create_time":"2017-09-15T15:14:39.129643Z","update_time":"2017-09-15T15:14:39.129797Z"},{"id":1,"code":"1","project_name":"工商爬虫","desc":"工商爬虫","create_time":"2017-09-14T14:26:01.990634Z","update_time":"2017-09-14T14:26:01.990716Z"}],
            //height: $(window).height() - 250,
            //width: 700,
            //showColumns:true,
            //pagination:true,
            //queryParams : queryParams,
            queryParamsType: "limit",
            minimumCountColumns: 2,
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 1000,                       //每页的记录行数（*）
            //pageList: [10, 20],        //可供选择的每页的行数（*）
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            //showExport: true,
            //exportDataType: 'all',
            //responseHandler: responseHandler2,
            columns: [
                {
                    field: 'id',
                    title: 'ID',
                    formatter: function (value, row, index) {
                        return index + 1;
                    },
                    width: '5%'
                },
                {
                    field: 'field_name',
                    title: '字段名',
                    align: 'center',
                    valign: 'middle',
                    width: '10%'

                }, {
                    field: 'desc',
                    title: '规则描述',
                    align: 'center',
                    valign: 'middle',
                    width: '30%'
                }, {
                    field: 'type',
                    title: '规则类型',
                    align: 'center',
                    valign: 'middle',
                    formatter: function (value, row, index) {
                        switch (value) {
                            case 0:
                                return '正则表达式';
                            case 1:
                                return '日期验证';
                            case 2:
                                return '浮点数验证';
                            case 3:
                                return '整数验证';
                            case 4:
                                return '非空验证';
                        }


                    },
                    width: '15%'
                }, {
                    field: 'rule',
                    title: '规则实现',
                    align: 'center',
                    valign: 'middle',

                    /*formatter: 'operateFormatter'*/
                }]
        });
        validateRuleTableInitialized = true;
    } else {
        $('#task_detail_validate_rules_table').bootstrapTable('load', data);
    }
}