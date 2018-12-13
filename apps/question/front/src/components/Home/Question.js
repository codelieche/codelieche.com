/**
 * Question Home Page
 */

import React from "react";
import { Switch, Route } from "react-router-dom";

// 组件
import JobIndex from "../Question/Job/Index";
import ReportIndex from "../Question/Report/Index";

class QuestionHome extends React.Component {
    render() {
        return (
        <Switch>
            <Route path="/question/job" component={JobIndex} location={this.props.location} />
            <Route path="/question/report" component={ReportIndex} location={this.props.location} />
        </Switch>
        )
    }
}

export default QuestionHome;