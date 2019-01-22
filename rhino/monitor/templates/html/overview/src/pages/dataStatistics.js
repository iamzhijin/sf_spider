import React, {Component} from 'react';
import { doRequest, toThousands, formDate } from '../util/util';
import $ from 'jquery';

export default class DataStatistics extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data:[]
        };
        this.datas = [];
        this.id = 'listC'+this.props.options.key;
    }

    componentWillMount() {

    }

    componentDidMount() {
        this.getData();
    }

    getData(){
        doRequest({
            url:'/monitor/crawler/stat/overview',
            method:'post',
            data:{
                type : this.props.options.key,
                date: formDate(Date.now(),'yyyy-MM-dd')
            },
            success:(res)=>{
                if(res.code == true){
                    let datas = res.data.data_items;
                    let total = datas.total || 0,day_update = datas.day_update || 0;
                    this.datas = JSON.parse(JSON.stringify(datas.source_stat));
                    let data = this.datas.slice(0,9);
                    this.setState({data,total,day_update});
                }
            }
        })
    }

    renderList(){
        if(this.datas.length < 9) return;
        let data = this.datas.slice(0,9);
        this.setState({data});
        let _data = this.datas[0];
        this.datas.shift();
        this.datas.push(_data);
        let list = $('#'+this.id);
        list.css('transform','translate(0,0)');
        setTimeout(()=>{
            list.addClass('trans05');
        },100);
        setTimeout(()=>{
            list.css('transform','translate(0,-12.5%)');
        },200);
        setTimeout(()=>{
            list.removeClass('trans05');
        },1000);
    }

    render(){
        return(
            <div className="flexbox flex1 list-container fdc">
                <div className="flexbox box-back" style={{height:70,padding:'5px 0',fontSize:16,marginBottom:10}}>
                    <div className="flexbox fdc flex1 aic jcc">
                        <div style={{fontWeight:'bold',color:'#666'}}>{this.props.options.name}</div>
                        <div style={{fontSize:20,color:'#37c0f7'}}>{toThousands(this.state.total)}</div>
                    </div>
                    <div className="flexbox fdc flex1 aic jcc">
                        <div style={{fontWeight:'bold',color:'#666'}}>今日净增</div>
                        <div style={{fontSize:20,color:(this.state.day_update>0?'#fc9b03':'#666')}}>{toThousands(this.state.day_update)}</div>
                    </div>
                </div>
                <div className="flexbox flex1 fdc box-back" style={{fontSize:12,overflow:'hidden',padding:'0 5px'}}>
                    <div className="flexbox" style={{color:'#333',lineHeight:3,fontSize:13}}>
                        <div className="flex1 flexbox">网站来源</div><div className="flexbox jcc" style={{width:'5em'}}>总量</div><div className="flexbox jcc" style={{width:'4em'}}>今日更新</div>
                    </div>
                    <div className="flex1" style={{overflow:'hidden',color:'#666'}}>
                        <div id={this.id} style={{transform:'translate(0,0)',height:'100%'}}>
                            {
                                this.state.data.map((v,i)=>{
                                    return <div key={i} className="flexbox aic" style={{height:'12.5%'}}>
                                        <div className="flex1 flexbox list-li"><span title={v.source}>{v.source}</span></div><div className="flexbox jcc" style={{width:'5em'}}>{v.total}</div><div className="flexbox jcc" style={{width:'4em',color:v.day_update>0?'#fc9b03':'#666'}}>{v.day_update}</div>
                                    </div>
                                })
                            }
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}