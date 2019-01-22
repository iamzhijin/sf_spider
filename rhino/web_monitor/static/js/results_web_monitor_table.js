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
};

function doQuery(params){
    $('#results_web_monitor_list_table').bootstrapTable('refresh');    //刷新表格
}

function webMonitorListTable(){
    var url = "./results_web_monitor_list_api";
    $('#results_web_monitor_list_table').bootstrapTable({
        method:'POST',
        dataType:'json',
        contentType: "application/x-www-form-urlencoded",
        cache: false,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        height: $(window).height(),
        width:$(window).width(),
        showColumns:true,
        toolbar:'#toolbar',
        showExport:true,
        showToggle:true,
        showRefresh:true,
        pagination:true,
        queryParams: queryParams,
        queryParamsType: "limit",
        checkboxHeader:true, //全选
        clickToSelect: true, //是否启用点击选中行

        minimumCountColumns:4,
        pageNumber:1,                       //初始化加载第一页，默认第一页
        pageSize: 200,                       //每页的记录行数（*）
        pageList: [200, 400, 'All'],        //可供选择的每页的行数（*）
        uniqueId: "web_name",                     //每一行的唯一标识，一般为主键列
        exportDataType: 'all',
        responseHandler: responseHandler,
        searchOnEnterKey:true,
        searchText:"",
        sortName : 'web_date_start',
        sortOrder : 'desc',
        sortable: true,
        columns: [
            {
                checkbox: true,
                clickToSelect:true
            },
            {
                field : 'web_name',
                title : '网页名称',
                align : 'center',
                valign : 'middle',
                sortable : true,
                searchable:true,
                searchFormatter:true
            }, {
                field : 'web_num',
                title : '本次爬取数量',
                align : 'center',
                valign : 'middle',
                sortable : true
            },  {
                field : 'es_num',
                title : 'es数量',
                align : 'center',
                valign : 'middle'
            },
             {
                field : 'web_date_start',
                title : '对比开始时间',
                align : 'center',
                valign : 'middle'
            },
            {
                field : 'status',
                title : '状态',
                align : 'center',
                valign : 'middle'
            }
        ]
    });
}


function queryParams(params) {
    var data_type = $('#data_type').val();
    var search_keyword =  $('#search_keyword').val();
    var result_status =  $('#result_status').val();
    var param = {
        limit : 200, // 页面大小
        offset : 0, // 页码
        result_status:result_status,
        data_type:data_type,
        search_keyword:search_keyword
    };
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


function refreshTable_manual() {

    var data_type = $('#data_type').val();
    var search_keyword =  $('#search_keyword').val();
    var result_status =  $('#result_status').val();
    params = {
        query: {
            limit: 200,
            offset: 0,
            data_type:data_type,
            search_keyword:search_keyword,
            result_status: result_status
        }
    };
    $('#results_web_monitor_list_table').bootstrapTable('refresh', params);    //刷新表格

}
function refreshTable_manual_result_status(result_status) {
    var data_type = $('#data_type').val();
    // var data_type = $('.menu_data_type li a .active').val();
    var search_keyword =  $('#search_keyword').val();
    params = {
        query: {
            limit: 200,
            offset: 0,
            data_type: data_type,
            search_keyword:search_keyword,
            result_status: result_status
        }
    };
    $('#results_web_monitor_list_table').bootstrapTable('refresh', params);    //刷新表格

    $('#original_status').text(result_status)
}

function refreshTable_manual_data_type(data_type) {
    // var result_status =  $('.result_status li a .active').val();
    var result_status =  $('#result_status').val();
    var search_keyword =  $('#search_keyword').val();
    params = {
        query: {
            limit: 200,
            offset: 0,
            data_type: data_type,
            search_keyword:search_keyword,
            result_status: result_status
        }
    };
    $('#results_web_monitor_list_table').bootstrapTable('refresh', params);    //刷新表格

    $('#data_type').text(data_type)
}


function delete_web_monitor_data() {
    var results_webMonitorInfo_list = $('#results_web_monitor_list_table').bootstrapTable('getAllSelections');
    var url = "./delete_results_web_monitor";
    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           tranditional:true,
           dataType : "html",
           url:  url,
           data: {results_webMonitorInfo_list:JSON.stringify(results_webMonitorInfo_list)},
           success: function() {
               // $('#crwawler_list_table').bootstrapTable('refresh')}})
           }})



}


function refresh_result_table_status() {
    // $('#search_keyword').val("");
    $('#original_status').text("状态");
    var data_type = $('.menu_data_type li a .active').val();
    params = {
        query: {
            limit: 200,
            offset: 0,
            data_type:data_type,
            result_status: "",
            search_keyword:$('#search_keyword').val()
        }
    };
    $('#results_web_monitor_list_table').bootstrapTable('refresh', params);    //刷新表格
}

function refresh_result_table_data_type() {
    // $('#search_keyword').val("");
    $('#data_type').text("数据类型");
    var result_status =  $('.result_status li a .active').val();
    params = {
        query: {
            limit: 200,
            offset: 0,
            result_status:result_status,
            data_type: "",
            search_keyword:$('#search_keyword').val()
        }
    };
    $('#results_web_monitor_list_table').bootstrapTable('refresh', params);    //刷新表格
}


function manual_trigger_web_monitor() {
    var webMonitorInfo_list = $('#results_web_monitor_list_table').bootstrapTable('getAllSelections');
    var url = "./manual_trigger_web_monitor";

    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           tranditional:true,
           dataType : "html",
           url:  url,
           data: {webMonitorInfo_list:JSON.stringify(webMonitorInfo_list)},
           success: function() {
           }
    })

}