/**
 * 问卷回答首页
 */
import React, { Component } from "react";
import { Route, Switch } from "react-router-dom";

// 问卷回答相关组件
import ReportDetail from "./Detail";

class JobIndex extends Component {
    render() {
        return (
            <Switch>
                <Route exat path="/wenjuan/report/:id" component={ReportDetail} />
            </Switch>
        );
    }
}

export default JobIndex;