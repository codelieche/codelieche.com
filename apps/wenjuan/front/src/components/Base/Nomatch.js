/**
 * 当路由为匹配到Switch中的路由的时候
 * 使用NoMatch组件处理
 */
import {Component} from 'react';


class NoMatch extends Component {
    constructor(props){
        super(props);
        this.state = {
            reFresh: false,
        }
    }

    componentDidMount() {
        // 获取pathname
        var pathname = this.props.history.location.pathname, reFreshPathname;
        try {
            // 获取reFreshPathname
            reFreshPathname = window.localStorage.reFreshPathname;
            // 设置reFreshPathname为新的pathname
            window.localStorage.reFreshPathname = pathname;
        } catch (error) {
            reFreshPathname = pathname;
        }

        if(pathname !== reFreshPathname){
            console.log(reFreshPathname, pathname);
            // 刷新网页
            // alert("准备刷新");
            window.location.reload();
        }else{
            // 无需刷新
            // console.log("无需刷新")
        }
    }

    render() {
        // console.log("未匹配到任何路由", this.props.history.location.pathname)
        return null;
    }

}

export default NoMatch;