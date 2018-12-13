/**
 * 问卷答卷详情首页
 */
import React, { Component } from "react";


class ReportDetail extends Component {
    render() {
        return <h1>ReportDetail：{this.props.match.params.id}</h1>
    }
}

export default ReportDetail;