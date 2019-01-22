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
        this.state = {
            activeTab:0
        };
        this.chart = null;
        this.tabs = this.props.tabs;
        this.datas = {};
    }

    componentWillMount(){
        window.addEventListener('resize',() => {
            this.chart && this.chart.resize();
        })
    }

    componentDidMount(){
        this.initChart();
        this.renderChart(this.tabs[0].key,0)
    }

    renderNext(){
        let index = (this.state.activeTab+1)%this.tabs.length;
        this.setState({activeTab:index});
        this.renderChart(this.tabs[index].key,index)
    }

    clearData(){
        this.datas = {};
    }

    renderChart(type,activeTab){
        if(activeTab !== undefined){
            this.setState({activeTab})
        }
        if(this.datas[type]){
            this.setChartOptions(this.datas[type],activeTab);
        } else {
            doRequest({
                url:'/monitor/crawler/stat/history',
                method:'post',
                data:{
                    type:type,
                    duration:15
                },
                success:(res)=>{
                    if(res.code){
                        let data = this.beautyData(res.data.data_items);
                        this.datas[type] = data;
                        this.setChartOptions(data,activeTab);
                    }
                }
            });
        }
    }

    beautyData(data){
        let dates = [];
        let nt = new Date();
        let nd = nt.getDate();
        for(let i = 0;i<15;i++){
            nt.setDate(nd);
            nd = nt.getDate()-1;
            dates.unshift(formDate(nt,'yyyy-MM-dd'))
        }
        let res = new Array(15).join(',').split(',');
        for(let j = 0;j<data.length;j++){
            res[dates.indexOf(data[j].date)] = data[j];
        }
        return res.map((v,i)=>{
            return v || {date:dates[i],count:0}
        })
    }

    setChartOptions(data,index){
        this.chart && this.chart.setOption({
            xAxis:[{
                data:data.map((v)=>{
                    return v.date.substr(5)
                })
            }],
            series:[{
                data:data.map((v)=>{
                    return v.count
                })
            }]
        })
    }

    initChart(){
        this.chart = echarts.init(document.getElementById('myChart'));
        this.chart.setOption({
            legend: {
                data:['接口调用']
            },
            grid:{
                x:80,
                y:20,
                x2:60,
                y2:30
            },
            calculable : true,
            yAxis : [
                {
                    type : 'value',
                    axisLabel : {
                        textStyle:{
                            color:'#999'
                        }
                    },
                    splitNumber:5,
                    splitLine:{
                        show:true
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
                        show:false
                    },
                    axisTick:{
                        show:false
                    }
                }
            ],
            series : [
                {
                    name:'接口调用',
                    type:'line',
                    smooth:false,
                    label:{
                        normal:{
                            show:true,
                            position:[5,-10],
                            color:'#2fb8f5'
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
                    areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(55, 192, 247, 0.6)'
                            }, {
                                offset: 0.9,
                                color: 'rgba(55, 192, 247, 0.3)'
                            }], false),
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 2
                        }
                    },
                    symbol:'circle',
                    symbolSize:6
                }
            ]
        });
    }

    render(){
        return(
            <div className="flexbox flex1 fdc">
                <div className="flexbox aic jcc">
                    {
                        this.tabs.map((v,i)=>{
                            return <div key={i} onClick={()=>this.renderChart(v.key,i)} className={(i == this.state.activeTab?'active ':'') + 'chart-tab'}>{v.name}</div>
                        })
                    }
                </div>
                <div className="flex1" id="myChart"></div>
            </div>
        )
    }
}