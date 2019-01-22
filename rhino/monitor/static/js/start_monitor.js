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

function monitor_action() {
   start_monitor = $("#start_monitor").text();
   if (start_monitor=="启动监控"){
       $("#start_monitor").text("停止监控");
//       var url = "./lanch_monitor"
//       $.get(url);
//       window.location.href=url;
   }
   else
   {
     $("#start_monitor").text("启动监控");
//     var url = "./stop_monitor"
//     $.get(url);
//     window.location.href=url;
   }
}

