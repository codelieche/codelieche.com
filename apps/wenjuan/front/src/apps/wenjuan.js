/**
 * 问卷模块前端代码入口
 */
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import NoMatch from "../components/Base/Nomatch";

// 各个组件
import WenjuanHome from "../components/Home/Wenjuan";


class App extends React.Component {
    render() {
        return(
            <Router>
                <Switch>
                    <Route path="/wenjuan" render={ props => <WenjuanHome {...props} /> } />
                    {/* 这个一定要放最后面 */}
                    <Route component={NoMatch} />
                </Switch>
            </Router>
            
        );
    }
}

export default App;
