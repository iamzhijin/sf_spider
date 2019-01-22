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

function doQuery(params){
    $('#monitor-list-table').bootstrapTable('refresh');    //刷新表格
}

function initTable(){
    var url = "./monitor_list_api";
    $('#monitor-list-table').bootstrapTable({
        method:'POST',
        dataType:'json',
        contentType: "application/x-www-form-urlencoded",
        cache: false,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        height: $(window).height()-200,
        width:$(window).width(),
        showColumns:true,
        toolbar:'#toolbar',
        showExport:true,
        showToggle:true,
        search:true,
        showRefresh:true,
        pagination:true,
        queryParams: queryParams,
        queryParamsType: "limit",
        clickToSelect: true, //是否启用点击选中行
        singleSelect: true,
        minimumCountColumns:2,
        pageNumber:1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100, 'All'],        //可供选择的每页的行数（*）
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        showExport: true,
        exportDataType: 'all',
        responseHandler: responseHandler,
        columns: [
            {
                checkbox: true
            },
            {
                field: 'id',
                title: 'ID',
                formatter: function (value, row, index) {
                    return index;
                }
            },
            {
                field : 'province',
                title : '省份名称',
                align : 'center',
                valign : 'middle',
                sortable : true
            }, {
                field : 'ent_name',
                title : '企业名称',
                align : 'center',
                valign : 'middle',
                sortable : true
            },  {
                field : 'update_time',
                title : '最后修改时间',
                align : 'center',
                valign : 'middle'
            }]
    });
}

function queryParams(params) {
    var param = {
        limit : params.limit, // 页面大小
        offset : params.offset // 页码

    }
    return param;
}

// 用于server 分页，表格数据量太大的话 不想一次查询所有数据，可以使用server分页查询，数据量小的话可以直接把sidePagination: "server"  改为 sidePagination: "client" ，同时去掉responseHandler: responseHandler就可以了，
function responseHandler(res) {
    if (res) {
        return {
            "rows" : res.data,
            "total" : res.size
        };
    } else {
        return {
            "rows" : [],
            "total" : 0
        };
    }
}

