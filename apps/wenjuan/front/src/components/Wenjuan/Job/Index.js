/**
 * 问卷首页
 */
import React, { Component } from "react";
import { Route, Switch } from "react-router-dom";

// 问卷相关组件
import JobDetail from "./Detail";



class JobIndex extends Component {
    render() {
        return (
            <Switch>
                <Route exat path="/wenjuan/job/:id" component={JobDetail} />
            </Switch>
        );
    }
}

export default JobIndex;