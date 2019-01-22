/**
 * Created by Administrator on 2017/11/20.
 */
import $ from 'jquery';
import morkData from '../util/data';
//请求封装函数，参数同$.ajax，没有返回值
export function doRequest(options) {
    if(process.env.NODE_ENV !== 'production'){
        options.success(morkData[options.url]);
        return;
    }
    let urlPre = process.env.NODE_ENV == 'production'?(window.location.origin || (window.location.protocol+'//'+window.location.host)):'/api';
    options.url = urlPre + options.url;
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: window.GLOBAL_CSRF_TOKEN },
    });
    options.data = {...options.data,timeStrap:Date.now()};
    return $.ajax({
        ...options
    })
}

//时间格式函数
export function formDate(time, format) {
    let date = new Date(time);
    let o = {
        "M+": date.getMonth() + 1,
        "d+": date.getDate(),
        "h+": date.getHours(),
        "m+": date.getMinutes(),
        "s+": date.getSeconds(),
        "q+": Math.floor((date.getMonth() + 3) / 3),
        "S": date.getMilliseconds()
    };
    if (/(y+)/.test(format)) {
        format = format.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    for (let k in o) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
        }
    }
    return format;
}

export function toThousands(num) {
    let result = [], counter = 0;
    num = (num || 0).toString().split('');
    for (let i = num.length - 1; i >= 0; i--) {
        counter++;
        result.unshift(num[i]);
        if (!(counter % 3) && i != 0) {
            result.unshift(',');
        }
    }
    return result.join('');
}
