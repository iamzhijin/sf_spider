/**
 * Created by Administrator on 2017/11/21.
 */
import { formDate } from './util';
let dates = [];
let nt = new Date();
let nd = nt.getDate();
for(let i = 0;i<15;i++){
    nt.setDate(nd);
    nd = nt.getDate()-1;
    dates.unshift(formDate(nt,'yyyy-MM-dd'))
}
let hisData = dates.map(function (v,i) {
    return {
        date:v,
        count:Math.ceil(Math.random()*50000000)
    }
});
let warningData = new Array(16).join(',').split(',').map(function (v,i) {
    return {
        id:i,
        message:'预警信息11111111111111111111'+i
    }
});
let overviewData = new Array(20).join(',').split(',').map(function (v,i) {
    return {
        source:'信息来源地1111'+i,
        total:Math.ceil(Math.random()*2000000),
        day_update:Math.ceil(Math.random()*100000)
    }
});

const morkData = {
    '/monitor/crawler/stat/history':{
        "code" : true,
        "msg": "返回数据成功",
        "data" : {
            "type" : "ktgg",
            "name": "开庭公告",
            "data_items":hisData
        }
    },
    '/monitor/crawler/alert':{
        "code": true,
        "msg": "接口调用成功",
        "data": {
            "items": warningData
        }
    },
    '/monitor/crawler/stat/overview':{
        "code": true,
        "msg": "接口返回成功",
        "data": {
            "type": "ktgg",
            "name": "开庭公告",
            "date": "2017-10-10",
            "data_items": {
                "total": Math.ceil(Math.random()*10000000),
                "day_update": Math.ceil(Math.random()*1000000),
                "source_stat": overviewData
            }
        }
    },
    '/monitor/crawler/stat/daily_increase_ratio':{
        "code": true,
        "msg": "调用成功",
        "data": [
            {"date": "2017-11-17", "ratio": 0.23},
            {"date": "2017-11-18", "ratio": -0.23},
            {"date": "2017-11-19", "ratio": 0.00},
            {"date": "2017-11-20", "ratio": 0.65},
            {"date": "2017-11-21", "ratio": -0.45},
            {"date": "2017-11-22", "ratio": 1.23},
            {"date": "2017-11-23", "ratio": -1.00}
        ]
    }
};

export default morkData;