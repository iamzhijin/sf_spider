/**
 * Created by Administrator on 2017/11/17.
 */
import React, {Component} from 'react';
import { doRequest } from '../util/util';
import $ from 'jquery';

export default class Warning extends Component{
    constructor(props){
        super(props);
        this.state = {
            datas:[]
        };
        this.datas = [];
        this.id = 'warningList2323';
    }

    componentWillMount(){

    }

    componentDidMount(){
        this.getData();
    }

    getData(){
        doRequest({
            url:'/monitor/crawler/alert',
            data:{},
            success:(res)=>{
                if(res.code){
                    let data = res.data.items;
                    this.datas = JSON.parse(JSON.stringify(data));
                    let datas = data.splice(0,2);
                    this.setState({datas});
                }
            }
        });
    }

    renderList(){
        if(this.datas.length < 2) return;
        let datas = this.datas.slice(0,2);
        this.setState({datas});
        let _data = this.datas[0];
        this.datas.shift();
        this.datas.push(_data);
        let list = $('#'+this.id);
        list.css('transform','translate(0,0)');
        setTimeout(()=>{
            list.addClass('trans05');
        },100);
        setTimeout(()=>{
            list.css('transform','translate(0,-100%)');
        },200);
        setTimeout(()=>{
            list.removeClass('trans05');
        },1000);
    }

    render(){
        return(
            <div className="flexbox flex1">
                <div className="flex1 flexbox fdc" id="warningList">
                    {!!this.state.datas.length &&
                        <div className="flex1" style={{overflow:'hidden'}}>
                            <div id={this.id} style={{transform:'translate(0,0)',height:'100%'}}>
                                {this.state.datas.map((v,i)=>{
                                    return <div className="waring-list-li flexbox aic" style={{height:'100%'}} key={i}>{v.message}</div>
                                })}
                            </div>
                        </div>
                    }
                    {!this.state.datas.length &&
                        <div className="no-msg flexbox aic jcc flex1">^_^ 数据更新正常，无异常信息</div>
                    }
                </div>
            </div>
        )
    }
}