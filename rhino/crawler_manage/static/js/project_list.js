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

function doQuery(params) {
    $('#project-list-table').bootstrapTable('refresh');    //刷新表格
}

function initTable() {
    var url = "./api/project_list";
    $('#project-list-table').bootstrapTable({
        method: 'POST',
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded",
        cache: false,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        //data:[{"id":8,"code":"9","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:21.889174Z","update_time":"2017-09-15T15:43:21.889335Z"},{"id":7,"code":"8","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:43:08.422227Z","update_time":"2017-09-15T15:43:08.422409Z"},{"id":6,"code":"7","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:42:12.488034Z","update_time":"2017-09-15T15:42:12.488139Z"},{"id":5,"code":"6","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:41:48.833986Z","update_time":"2017-09-15T15:41:48.834099Z"},{"id":4,"code":"4","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:39:48.077809Z","update_time":"2017-09-15T15:39:48.077922Z"},{"id":3,"code":"3","project_name":"浙江双告知","desc":"sdf电风扇项目代码已经存在，无法保存！项目代码已经存在，无法保存！项目代码已经存在，无法保存！","create_time":"2017-09-15T15:30:16.145086Z","update_time":"2017-09-15T15:30:16.145190Z"},{"id":2,"code":"2","project_name":"浙江双告知","desc":"sdf电风扇","create_time":"2017-09-15T15:14:39.129643Z","update_time":"2017-09-15T15:14:39.129797Z"},{"id":1,"code":"1","project_name":"工商爬虫","desc":"工商爬虫","create_time":"2017-09-14T14:26:01.990634Z","update_time":"2017-09-14T14:26:01.990716Z"}],
        height: $(window).height() - 200,
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
        columns: [
            {
                field: '',
                title: 'ID',
                formatter: function (value, row, index) {
                    return index;
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
                field: 'update_time',
                title: '最后修改时间',
                align: 'center',
                valign: 'middle',
                sortable: true
                ,
                formatter: function (value, row, index) {
                    return new Date(value).format('yyyy-MM-dd hh:mm:ss')
                }
            }, {
                field: 'code',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: createCrawlerOperator,
                width: '16%',
            }]
    });
}

function createCrawlerOperator(value, row, index) {
    return '<a class="btn btn-default btn-xs btn-primary" ' +
        'href="/crawler_manage/crawler/create?project=' + row['code'] +'">新建爬虫</a>'
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
