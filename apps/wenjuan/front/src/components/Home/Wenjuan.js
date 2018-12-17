/**
 * Question Home Page
 */

import React from "react";
import { Switch, Route } from "react-router-dom";

// 组件
import JobIndex from "../Wenjuan/Job/Index";
import ReportIndex from "../Wenjuan/Report/Index";

class WenjuanHome extends React.Component {
    render() {
        return (
        <Switch>
            <Route path="/wenjuan/job" component={JobIndex} location={this.props.location} />
            <Route path="/wenjuan/report" component={ReportIndex} location={this.props.location} />
        </Switch>
        )
    }
}

export default WenjuanHome;