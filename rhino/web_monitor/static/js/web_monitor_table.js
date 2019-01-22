
function doQuery(params){
    $('#web_monitor_list_table').bootstrapTable('refresh');    //刷新表格
}

function webMonitorListTable(){
    var url = "./web_monitor_list_api";
    $('#web_monitor_list_table').bootstrapTable({
        method:'POST',
        dataType:'json',
        contentType: "application/x-www-form-urlencoded",
        cache: false,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        height: $(window).height(),
        width:$(window).width(),
        toolbar:'#toolbar',
        showExport:true,
        showToggle:true,
        showRefresh:true,
        pagination:true,
        queryParams: queryParams,
        queryParamsType: "limit",
        checkboxHeader:true, //全选
        clickToSelect: true, //是否启用点击选中行
        cardView: true,
        minimumCountColumns:4,
        pageNumber:1,                       //初始化加载第一页，默认第一页
        pageSize: 200,                       //每页的记录行数（*）
        pageList: [200,400,'All'],        //可供选择的每页的行数（*）
        uniqueId: "web_name",                     //每一行的唯一标识，一般为主键列
        exportDataType: 'all',
        responseHandler: responseHandler,
        searchOnEnterKey:true,
        searchText:"",
        sortName : 'web_update_time',
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
                searchable:true,
                searchFormatter:true
            }, {
                field : 'web_site',
                title : '网页地址',
                align : 'center',
                valign : 'middle'
            },  {
                field : 'request_function',
                title : '请求方式',
                align : 'center',
                valign : 'middle'
            },{
                field : 'request_body',
                title : '请求主体',
                align : 'center',
                valign : 'middle'
            },{
                field : 'xpath_str',
                title : 'xpath表达式',
                align : 'center',
                valign : 'middle'
            },{
                field : 'per_num',
                title : '每页数量',
                align : 'center',
                valign : 'middle',
                visible: false
            },{
                field : 'web_update_time',
                title : '修改时间',
                align : 'center',
                valign : 'middle'
            },{
                field : 'response_type',
                title : '响应类型',
                align : 'center',
                valign : 'middle'
            },{
                field : 're_str',
                title : 're表达式',
                align : 'center',
                valign : 'middle'
            },{
                field : 'keyword',
                title : '关键词',
                align : 'center',
                valign : 'middle'
            },{
                field : 'data_type',
                title : '数据类型',
                align : 'center',
                valign : 'middle'
            }
        ]
    });
}

// function sort_flag_status(value, row, index) {
//     row['flag_status']
// }


function queryParams(params) {

    var param = {
        limit : params.limit, // 页面大小
        offset : params.offset, // 页码
        data_type:$('#data_type').val(),
        search_keyword:$('#search_keyword').val()
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
    data_type = $('.menu_data_type li a .active').val();
    params = {
        query: {
            limit: 10,
            offset: 0,
            data_type:data_type
        }
    };
    $('#web_monitor_list_table').bootstrapTable('refresh', params);    //刷新表格

}
function refreshTable_manual(data_type) {

    var search_keyword =  $('#search_keyword').val();
    params = {
        query: {
            limit: 20,
            offset: 0,
            data_type: data_type,
            search_keyword:search_keyword
        }
    };
    $('#web_monitor_list_table').bootstrapTable('refresh', params);    //刷新表格


    $('#data_type').text(data_type)
}

// 新增按钮
function create_web_monitor(){
    $('#create_web_monitor').modal('show');
}

function delete_web_monitor() {
    var webMonitorInfo_list = $('#web_monitor_list_table').bootstrapTable('getAllSelections');
    var url = "./delete_web_monitor";
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

function run_web_monitor_task() {
    var webMonitorInfo_list = $('#web_monitor_list_table').bootstrapTable('getAllSelections');
    var url = "./run_web_monitor_task";

    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           tranditional:true,
           dataType : "html",
           url:  url,
           data: {webMonitorInfo_list:JSON.stringify(webMonitorInfo_list)},
           success: function() {
                window.location.href ="results_web_monitor.html"
           }
    })

}
function refresh_task_table() {
    $('#search_keyword').val("");
    $('#data_type').text("数据类型");
    params = {
        query: {
            limit: 20,
            offset: 0,
            data_type: "",
            search_keyword:""
        }
    };
    $('#web_monitor_list_table').bootstrapTable('refresh', params);    //刷新表格
}
