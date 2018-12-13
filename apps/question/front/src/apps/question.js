/**
 * 问卷模块前端代码入口
 */
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import NoMatch from "../components/Base/Nomatch";

// 各个组件
import QuestionHome from "../components/Home/Question";


class App extends React.Component {
    render() {
        return(
            <Router>
                <Switch>
                    <Route path="/question" render={ props => <QuestionHome {...props} /> } />
                    {/* 这个一定要放最后面 */}
                    <Route component={NoMatch} />
                </Switch>
            </Router>
            
        );
    }
}

export default App;
