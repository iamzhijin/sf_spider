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

function alert_box(type, msg){
    var css = 'alert-info'
    var hint = '提示'
    if(type == 'error') {
        css = 'alert-danger'
        hint = '错误'
    }
    else if(type == 'success') {
        css = 'alert-success'
        hint = '成功'
    }
    else if(type == 'warning') {
        css = 'alert-warning'
        hint = '警告'
    }
    else {
        css = 'alert-info'
        hint = '提示'
    }
    $('.alert').alert('close');
    $('#alert_banner').html('<div class=\"alert ' + css + ' alert-dismissible fade\" role=\"alert\">' +
                '<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span' +
                        'aria-hidden=\"true\">&times;</span>' +
                '</button>' +
                '<strong>' + hint +': </strong>' + msg +
            '</div>')
    $('.alert').addClass('in');

}

function isJsonFormat( str ) {
    try {
        $.parseJSON(str);
    } catch (e) {
        return false;
    }
    return true;
}
