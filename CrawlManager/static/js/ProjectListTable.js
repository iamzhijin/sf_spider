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
        // height: $(window).height()*0.8,
        width:$(window).width(),
        pagination:true,
        queryParams: queryParams,
        queryParamsType: "limit",
        clickToSelect: true, //是否启用点击选中行
        singleSelect: false,
        minimumCountColumns:2,
        pageNumber:1,                       //初始化加载第一页，默认第一页
        pageSize: 5,                       //每页的记录行数（*）
        pageList: [25, 50, 100, 'All'],     //可供选择的每页的行数（*）
        sortName: 'full_name',              // 指定默认排序字段
        idField:'id',
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        exportDataType: 'all',
        responseHandler: responseHandler,
        showColumns:false,
        showToggle:false,
        showRefresh:true,
        theadClasses: 'thead-light',    // 定义表头的class
        columns: [
            {
                field: 'id',
                title: '序号',
                algin: 'center',
                valign: 'middle',
                // formatter: function(value, row, index){
                //     return index + 1                
                // },                 
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
                field: 'crawl_num',
                title: '爬虫数量',
                algin: 'center',
                valign: 'middle',
                cellStyle: function(value, row, index){
                    if(value>0){
                        return {css:{"color": "#00ce68"}} // 爬虫数量大于是10 颜色显示为绿色
                    }
                    else{
                        return {}
                    }
                }
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
            {
                field: '',
                title: '操作',
                algin: 'center',
                valgin: 'middle',
                formatter: function(value, row, index){
                    return [
                        '<button onclick="updateProject(\''+row.id +'\',\''+ row.project_name +'\',\''+ row.code +'\',\''+ row.describe +'\')" type="button" class="btn btn-warning btn-xs" data-toggle="modal" data-target="#upProject" style="background-color: #ffaf00;">修改</button>',  
                        '<button onclick="deleteProject(' +row.id+')" type="button" class="btn btn-danger btn-xs" style="background-color: #e65251;">删除</button>'
                    ].join('&nbsp&nbsp')
                    
                }
            }
        ],
    });
}

function refreshTable_myfeedback() {
    var params = {
        limit : 5, // 页面大小
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

function updateProject(id, project_name, code, describe){
    $('#id').val(id)
    $('#new_projectname').val(project_name);
    $('#new_code').val(code);
    $('#new_describe').val(describe);
}