function ProjectListTable() {
    $('#project-list').bootstrapTable('destroy');
    var url = "/CrawlProject/ProjectList/";
    $('#project-list').bootstrapTable({
        method:'GET',
        dataType:'json',
        contentType: "application/x-www-form-urlencoded",
        cache: false,
        striped: true,                              //是否显示行间隔色
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        url: url,
        toolbar: '#toolbar',
        toolbarAlign:'left',
        height: $(window).height()*0.8,
        width:$(window).width(),
        pagination:true,
        queryParams: queryParams,
        queryParamsType: "limit",
        clickToSelect: true, //是否启用点击选中行
        singleSelect: false,
        minimumCountColumns:2,
        pageNumber:1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [25, 50, 100, 'All'],     //可供选择的每页的行数（*）
        sortName: 'full_name',                // 指定默认排序字段
        idField:'id',
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        exportDataType: 'all',
        responseHandler: responseHandler,
        showColumns:true,
        showToggle:true,
        showRefresh:true,
        columns: [
            {
                field: '',
                title: '序号',
                algin: 'center',
                valign: 'middle',
                formatter: function(value, row, index){
                    return index + 1                
                },
                rowStyle:{  
                    css:{"background-color":"red"}  
                }  
            },
            {
                field: 'project_name',
                title: '项目名称',
                algin: 'center',
                valign: 'middle',               
            },
            {
                field: 'code',
                title: '项目编码',
                algin: 'center',
                valign: 'middle',               
            },
            {
                field: 'describe',
                title: '项目描述',
                algin: 'center',
                valign: 'middle',               
            },
            {
                field: 'update_time',
                title: '修改时间',
                algin: 'center',
                valign: 'middle',               
            },
            {
                field: 'create_time',
                title: '创建时间',
                algin: 'center',
                valign: 'middle',               
            },
        ]
    });
}

function refreshTable_myfeedback() {
    var params = {
        limit : 10, // 页面大小
        offset : 0, // 页码
    }
    $('#project-list').bootstrapTable('refresh', params);    //刷新表格
}
function queryParams(params) {    
    var params = {
        limit : params.limit, // 页面大小
        offset : params.offset, // 页码
    }
    return params;
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