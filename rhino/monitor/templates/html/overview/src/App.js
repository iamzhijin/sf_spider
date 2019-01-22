/**
 * Created by 2087 on 2017/11/17.
 */
import React, {Component} from 'react';
import Header from './pages/header';
import Charts from './pages/charts';
import Warning from './pages/warning';
import Charts2 from './pages/charts2';
import DataStatistics from './pages/dataStatistics';
import './app.css';
// import Fireworks from './compontents/yh';

const TABS = [{key:'ktgg',name:'开庭公告',color:"#335984"},{key:'cpws',name:'裁判文书',color:"#a84048"},
    {key:'sxbzxr',name:'失信被执行人',color:"#795795"},{key:'bzxr',name:'被执行人',color:"#9ab556"},
    {key:'bgt',name:'曝光台',color:"#367c91"},{key:'fygg',name:'法院公告',color:"#924943"}];

const TITLE_IMGS = [
    require('./images/title-1.png'),
    require('./images/title-2.png'),
    require('./images/title-3.png'),
    require('./images/title-4.png'),
];

export default class App extends Component {
    constructor(props){
        super(props);
        this.state={

        };
        this.childRefs = {};
        this.sectionTimer = null;
        this.tabs = TABS;
    }

    componentDidMount(){
        //每秒轮询是否需要翻页或请求数据
        this.sectionTimer = setInterval(()=>this.secondChange(),1000);
    }

    componentWillUnmount(){
        //销毁组件时，清除定时器
        this.sectionTimer && clearInterval(this.sectionTimer);
    }

    secondChange(){
        let s = new Date().getSeconds();
        this.childRefs['header'] && this.childRefs['header'].updateTime();
        !(s%10) && this.childRefs['chart'] && this.childRefs['chart'].renderNext();
        !(s%3) && this.scrollStatistics();
        !(s%3) && this.childRefs['warning'] && this.childRefs['warning'].renderList();
        !(s%60) && this.minutesChange();
    }

    minutesChange(){
        let m = new Date().getMinutes();
        !(m%15) && this.childRefs['chart'] && this.childRefs['chart'].clearData();
        !(m%15) && this.childRefs['chart2'] && this.childRefs['chart2'].renderChart();
        !(m%15) && this.childRefs['warning'] && this.childRefs['warning'].getData();
        !(m%15) && this.getDataStatistics();
    }

    updateAllData(){
        this.childRefs['chart'] && this.childRefs['chart'].clearData();
        this.childRefs['chart2'] && this.childRefs['chart2'].renderChart();
        this.childRefs['warning'] && this.childRefs['warning'].getData();
        this.getDataStatistics();
    }

    getDataStatistics(){
        if(this.childRefs['DataStatistics']){
            for(let i =0;i<this.childRefs['DataStatistics'].length;i++){
                this.childRefs['DataStatistics'][i].getData();
            }
        }
    }

    scrollStatistics(){
        if(this.childRefs['DataStatistics']){
            for(let i =0;i<this.childRefs['DataStatistics'].length;i++){
                this.childRefs['DataStatistics'][i].renderList();
            }
        }
    }

    render() {
        return (
            <div className="flexbox flex1 fdc" style={{height:'100%'}}>
                <Header clickHandle={()=>this.updateAllData()} ref={(ref) => this.childRefs['header'] = ref} />
                <div className="flexbox flex1" style={{marginBottom:10}}>
                    <div className="flexbox flex3 box-back fdc section1-1">
                        <SectionTitle icon={<img src={TITLE_IMGS[3]} />} title="数据更新趋势" />
                        <Charts ref={(ref)=>this.childRefs['chart'] = ref} tabs={TABS} />
                    </div>
                    <div className="flexbox flex2 fdc section1-2">
                        <div className="flexbox box-back fdc" style={{height:80,padding:10,marginBottom:10}}>
                            <SectionTitle icon={<img src={TITLE_IMGS[2]} />} title="预警信息" />
                            <Warning ref={(ref)=>this.childRefs['warning'] = ref} />
                        </div>
                        <div className="flexbox flex1 fdc box-back flex1" style={{padding:10}}>
                            <SectionTitle icon={<img src={TITLE_IMGS[1]} />} title="日环比增长率" />
                            <Charts2 ref={(ref)=>this.childRefs['chart2'] = ref} />
                        </div>
                    </div>

                </div>
                <div className="flexbox flex1 fdc box-back section2" style={{padding:10}}>
                    <SectionTitle icon={<img src={TITLE_IMGS[0]} />} title="数据量统计" />
                    <div className="flexbox flex1">
                        {
                            this.tabs.map((v,i) => {
                                return <DataStatistics key={i} options={v} ref={(ref)=>{this.childRefs['DataStatistics']?this.childRefs['DataStatistics'][i] = ref:this.childRefs['DataStatistics'] = [ref]}} />
                            })
                        }
                    </div>
                </div>
            </div>
        )
    }
}

class SectionTitle extends Component {
    render(){
        return(
            <div className="flexbox aic" style={{margin:'5px 0',fontSize:16}}>{this.props.icon}<span style={{marginLeft:10,fontWeight:'bold'}}>{this.props.title}</span></div>
        )
    }
}