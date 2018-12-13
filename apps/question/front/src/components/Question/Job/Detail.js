/**
 * 问卷详情首页
 */
import React, { Component } from "react";


class JobDetail extends Component {
    render() {
        return <h1>JobDetail {this.props.match.params.id}</h1>
    }
}

export default JobDetail;