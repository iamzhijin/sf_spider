/**
 * Created by linshirong on 2017/9/16.
 */
Date.prototype.format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

function project_filter(project_id, project_name) {
    $('#project_id').val(project_id);
    if (project_id.length <= 0)
        $('#dropdownMenu1').html('所有数据项目 <span class="caret"></span>');
    else
        $('#dropdownMenu1').html(project_id + ' ---- ' + project_name + ' <span class="caret"></span>');
    refreshTable();
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
    $('#crawler-list-table').bootstrapTable('refresh', params);    //刷新表格
}

function populateFieldMappingTable(data) {
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
}


function initTable() {
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
        height: $(window).height() - 250,
        width: $(window).width(),
        showColumns: false,
        pagination: true,
        queryParams: queryParams,
        queryParamsType: "limit",
        minimumCountColumns: 2,
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [10, 20],        //可供选择的每页的行数（*）
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        showExport: true,
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
                valign: 'middle'
            }, {
                field: 'crawler_name',
                title: '爬虫名称',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'project_id',
                title: '项目编码',
                align: 'center',
                valign: 'middle'
            }, {
                field: 'project_name',
                title: '项目名称',
                align: 'center',
                valign: 'middle'
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
                field: 'update_time',
                title: '最后修改时间',
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
                width: '20%',
                formatter: 'operateFormatter'
            }]
    });
}

function operateFormatter(value, row, index) {
    return '<button type="button" class="btn btn-default btn-xs btn-info" style="margin-right:5px;font-size: 10px" ' +
        'onclick="showCrawlerDetail(\'' + row['id'] + '\', \''
        + row['project_name'] + '\')">查看</button>' +
        '<button type="button" class="btn btn-default  btn-xs btn-warning" style="margin-right:5px;font-size: 10px" ' +
        'onclick="editCrawler(\'' + row['id'] + '\')">编辑</button>' +
        '<button type="button" class="btn btn-default  btn-xs btn-primary" style="margin-right:5px;font-size: 10px" ' +
        'onclick="newTask(\'' + row['id'] + '\')">新建</button>' +
        '<button type="button" class="btn btn-default  btn-xs btn-danger" data-toggle="modal" data-target="#confirmModal" style="margin-right:5px;font-size: 10px" ' +
        'data-value = \'' + row['id'] + '\'>删除</button>'
}

function newTask(crawlerId) {
    $(window.location).attr('href', '/crawler_manage/task/create?crawler_id=' + crawlerId);
}

$(function () {
    $('#confirmModal').on('show.bs.modal', function (e) {
        var btn = $(e.relatedTarget);
        crawler_id = btn.data("value")
        var url = "/crawler_manage/crawler/" + crawler_id + "/tasks";
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


function deleteCrawler(crawlerId, tasks) {
    if (tasks == 0) {
        console.log('删除爬虫...')
        var url = "/crawler_manage/crawler/delete/" + crawlerId;
        $.ajax({
            url: url,
            type: "get",
            cache: false,
            success: function (result) {
                if (result.code == true) {
                    console.log('删除爬虫成功...')
                } else {
                    console.log('删除爬虫失败...')
                }
            },
            error: console.log('删除爬虫失败...'),
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

function editCrawler(crawlerId) {
    $(window.location).attr('href', '/crawler_manage/crawler/edit/' + crawlerId);
}

function showCrawlerDetail(crawkerID) {
    var crawlerDetail = $('#crawler-list-table').bootstrapTable('getRowByUniqueId', crawkerID);
    populateCrawlerDetailModal(crawlerDetail);
    var field_mapping = crawlerDetail.fields_mapping;
    populateFieldMappingTable($.parseJSON(field_mapping));
    $('#crawlerDetailModal').modal('toggle');
}

function populateCrawlerDetailModal(crawlerData) {
    $('#detail_crawler_id').val(crawlerData.id);
    $('#detail_crawler_name').val(crawlerData.crawler_name);
    $('#detail_project_id').val(crawlerData.project_id);
    $('#detail_project_name').val(crawlerData.project_name);
    $('#detail_crawler_app').val(crawlerData.crawler_app);
    $('#detail_clean_app').val(crawlerData.clean_app);
    $('#detail_clean_parameters').val(crawlerData.clean_parameters);
    $('#detail_field_mapping').val(crawlerData.fields_mapping);

    var download_crawler_app_url = "/download/" + crawlerData.crawler_app
    var filename = crawlerData.crawler_app.replace(/.*(\/|\\)/, "");
    if (filename != null && filename.length > 0) {
        $('#download_crawler_app').attr("href", download_crawler_app_url);
        $('#download_crawler_app').css("display", "block");
    } else {
        $('#download_crawler_app').css("display", "none");
    }

    var view_crawler_app_url = "crawler_app/" + crawlerData.id
    var fileExt = (/[.]/.exec(filename)) ? /[^.]+$/.exec(filename.toLowerCase()) : '';
    if (fileExt != null && fileExt.length > 0 && fileExt == 'py') {
        $('#view_crawler_app').attr("href", view_crawler_app_url);
        $('#view_crawler_app').css("display", "block");
    } else {
        $('#view_crawler_app').css("display", "none");
    }
    $('#detail_crawler_app').val(filename);

    var download_clean_app_url = "/download/" + crawlerData.clean_app
    var clean_app_filename = crawlerData.clean_app.replace(/.*(\/|\\)/, "");
    if (clean_app_filename != null && clean_app_filename.length > 0) {
        $('#download_clean_app').attr("href", download_clean_app_url);
        $('#download_clean_app').css("display", "block");
    } else {
        $('#download_clean_app').css("display", "none");
    }


    $('#detail_clean_app').val(clean_app_filename);
    //$('#detail_create_time').val(crawlerData.create_time);
    //$('#detail_update_time').val(crawlerData.update_time);
}

function queryParams(params) {
    var param = {
        limit: params.limit, // 页面大小
        offset: params.offset, // 页码
        search_keyword: $('search_keyword').val()
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
