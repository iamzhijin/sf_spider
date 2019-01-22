/**
 * Created by Administrator on 2017/11/20.
 */
import React, {Component} from 'react';
import { formDate } from '../util/util';

const LOGO = require('../images/ys-logo.png');

export default class Header extends Component {
    constructor(props){
        super(props);
        this.state = {
            time: formDate(Date.now(),'yyyy-MM-dd hh:mm:ss')
        };
    }

    componentWillMount(){

    }

    componentDidMount(){

    }

    updateTime(){
        let time = formDate(Date.now(),'yyyy-MM-dd hh:mm:ss');
        this.setState({time});
    }

    render(){
        return(
            <div className="flexbox aic" style={{height:48,position:'relative',paddingLeft:100}}>
                <div className="flexbox aic"><div style={{fontSize:16,color:'#333',fontWeight:'bold'}}>有数金服司法数据采集展示终端</div><div style={{color:'#666',fontSize:12,marginLeft:20}}>{this.state.time}</div></div>
                <div className="flexbox time-container fdc">
                    <img onClick={()=> this.props.clickHandle()} src={LOGO} />
                </div>
            </div>
        )
    }
}