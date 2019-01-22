/**
 * Created by Administrator on 2017/11/17.
 */
import React, {Component} from 'react';
import echarts from 'echarts/lib/echarts';
import  'echarts/lib/chart/line';
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import { doRequest, formDate } from '../util/util';

export default class Charts extends Component {
    constructor(props){
        super(props);
        this.chart = null;
        this.datas = {};
    }

    componentWillMount(){
        window.addEventListener('resize',() => {
            this.chart && this.chart.resize();
        })
    }

    componentDidMount(){
        this.initChart();
    }

    renderChart(){
        doRequest({
            url:'/monitor/crawler/stat/daily_increase_ratio',
            method:'post',
            data:{
                duration:7
            },
            success:(res)=>{
                if(res.code){
                    let data = this.beautyData(res.data);
                    this.setChartOptions(data);
                }
            }
        });
    }

    beautyData(data){
        let dates = [];
        let nt = new Date();
        let nd = nt.getDate();
        for(let i = 0;i<7;i++){
            nd = nt.getDate()-1;
            nt.setDate(nd);
            dates.unshift(formDate(nt,'yyyy-MM-dd'))
        }
        let res = new Array(7).join(',').split(',');
        for(let j = 0;j<data.length;j++){
            res[dates.indexOf(data[j].date)] = data[j];
        }
        return res.map((v,i)=>{
            return v || {date:dates[i],ratio:0}
        })
    }

    setChartOptions(data){
        this.chart && this.chart.setOption({
            xAxis:[{
                data:data.map((v)=>{
                    return v.date.substr(5)
                })
            }],
            series:[{
                data:data.map((v)=>{
                    return Math.round(v.ratio*10000)/100
                })
            }]
        })
    }

    initChart(){
        this.chart = echarts.init(document.getElementById('myChart2'));
        this.chart.setOption({
            legend: {
                data:['日环比增长率']
            },
            grid:{
                x:60,
                y:20,
                x2:45,
                y2:30
            },
            calculable : true,
            yAxis : [
                {
                    type : 'value',
                    axisLabel : {
                        textStyle:{
                            color:'#999'
                        },
                        formatter:function (v) {
                            return v+'%'
                        }
                    },
                    splitNumber:5,
                    splitLine:{
                        show:true,
                        lineStyle:{
                            color:'#ccc'
                        }
                    },
                    axisLine:{
                        show:false
                    },
                    axisTick:{
                        show:false
                    }
                },
            ],
            xAxis : [
                {
                    type : 'category',
                    boundaryGap : false,
                    splitLine:{
                        show:false
                    },
                    axisLabel:{
                        textStyle:{
                            color:'#999'
                        },
                        interval:0,
                        rotate:-30
                    },
                    axisLine:{
                        show:true,
                        lineStyle:{
                            color:'#fc9b03',
                            type:'dashed'
                        }
                    },
                    axisTick:{
                        show:false
                    }
                }
            ],
            series : [
                {
                    name:'日环比增长率',
                    type:'line',
                    smooth:false,
                    label:{
                        normal:{
                            show:true,
                            position:[5,-10],
                            color:'#2fb8f5',
                            formatter:function (v) {
                                return v.data+'%'
                            }
                        }
                    },
                    lineStyle:{
                        normal:{
                            color:'#2fb8f5',
                            shadowColor : '#fff',
                            shadowBlur: 5,
                            shadowOffsetX: 0,
                            shadowOffsetY: 0
                        }
                    },
                    itemStyle:{
                        normal:{
                            color:'#2fb8f5',
                        }
                    },
                    symbol:'circle',
                    symbolSize:6
                }
            ]
        });
        this.renderChart();
    }

    render(){
        return(
            <div className="flex1" id="myChart2"></div>
        )
    }
}