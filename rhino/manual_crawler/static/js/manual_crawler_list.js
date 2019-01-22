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
    $('#crwawler_list_table').bootstrapTable('refresh');    //刷新表格
}

function crawlerListTable(){
    var url = "./crawler_list_api";
    $('#crwawler_list_table').bootstrapTable({
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
        strictSearch:false,
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
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        exportDataType: 'all',
        responseHandler: responseHandler,
        searchOnEnterKey:true,
        sortName : 'id',
        sortOrder : 'desc',
        sortable: true,
        columns: [
            {
                checkbox: true,
                clickToSelect:true
            },
            {
                field: 'id',
                title: 'ID',
                align : 'center',
                formatter: function (value, row, index) {
                    return index;
                }
            },
            {
                field : 'crawler_type',
                title : '爬取类型',
                align : 'center',
                valign : 'middle',
                sortable : true,
                searchable:true,
                searchFormatter:true
            }, {
                field : 'type',
                title : '企业名/人名',
                align : 'center',
                valign : 'middle',
                sortable : true,
                formatter: typeFormatter,
                searchable:true,
                searchFormatter:true
            },  {
                field : 'ent_person_name',
                title : '关键词',
                align : 'center',
                valign : 'middle',
                searchable:true,
                searchFormatter:true
            },{
                field : 'flag_status',
                title : '状态',
                align : 'center',
                valign : 'middle',
                formatter: flagStatusFormatter,
                searchable:true,
                searchFormatter:true
            },{
                field : 'create_time',
                title : '创建时间',
                align : 'center',
                valign : 'middle',
                visible : true,
                sortable :true,
                order :"desc"
            }
        ]
    });
}

// function sort_flag_status(value, row, index) {
//     row['flag_status']
// }

function typeFormatter(value, row, index){
    if(row['type']==1)
        return "企业名";
    else
        return "人名";
}

function queryParams(params) {
    var search_keyword = $('#status').val()
    var param = {
        limit : 200, // 页面大小
        offset : 0, // 页码
        status:$('#status').val(),
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

function flagStatusFormatter(value, row, index) {
    if (row["flag_status"]==0)
        return '<button type="button" id="start_manual_crawler_'+row['id']+'"'+ ' class="btn btn-default btn-xs btn-primary " '+'>待启动</button>'
            +'<button type="button" id="doing_manual_crawler_'+row['id']+'"'+' class="btn btn-default  btn-xs btn-warning" style="display: none"' +
        '">正在爬取</button>'
    else if (row['flag_status']==1)
        return '<button type="button" class="btn btn-default  btn-xs btn-warning "  ' + '">正在爬取</button>';
    else if (row['flag_status']==3)
        return '<button type="button" id="start_manual_crawler_' + row['id'] + '" class="btn btn-default btn-xs btn-danger "'+'>失败</button>'
        +'<button type="button" id="doing_manual_crawler_'+row['id']+'"'+' class="btn btn-default  btn-xs btn-warning" style="display: none"' +
        '">正在爬取</button>'
    else if (row['flag_status']==2)
        return '<button type="button" class="btn btn-default  btn-xs btn-success"' +
        '">成功</button>';
    else if (row['flag_status']==4)
        return '<button type="button" class="btn btn-default  btn-xs btn-success"' +
        '">0002</button>';
}



function crawlerStatusSwitch(id){
    var start_str = "start_manual_crawler_"+id;
    var doing_str = "doing_manual_crawler_"+id;
    $('#' + start_str ).css("display", "none");
    $('#' + doing_str ).css("display", "inherit");

}


function deleteManual_Crawler(){
    var crawlerInfo_list = $('#crwawler_list_table').bootstrapTable('getAllSelections');
    var url = "./delete_manual_crawler";
    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           tranditional:true,
           dataType : "html",
           url:  url,
           data: {crawlerInfo_list:JSON.stringify(crawlerInfo_list)},
           success: function() {
               // $('#crwawler_list_table').bootstrapTable('refresh')}})
           }})
}

function refreshTable_manual() {
    $("#status_str").text("432");
    $("#search_keyword").val("");
    params = {
        query: {
            limit: 10,
            offset: 0,
            status: "",
            search_keyword:""
        }
    };
    $('#crwawler_list_table').bootstrapTable('refresh', params);    //刷新表格
}
// 重试、启动、其他 按钮
function refreshTable_manual(flag_status){
    var search_keyword =  $('#search_keyword').val();
    params = {
        query: {
            limit: 200,
            offset: 0,
            status: flag_status,
            search_keyword:search_keyword
        }
    };

    $('#crwawler_list_table').bootstrapTable('refresh', params);    //刷新表格

    $('#status_str').text(flag_status)
}

// 新增按钮
function create_crawler_task(){
    $('#create_crawler_task').modal('show');
}

function run_manual_crawler() {
    var crwawler_list = $('#crwawler_list_table').bootstrapTable('getAllSelections');
    var url = "./run_manual_crawler";

    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           tranditional:true,
           dataType : "html",
           url:  url,
           data: {crwawler_list:JSON.stringify(crwawler_list)},
           success: function() {
           }
    })
}