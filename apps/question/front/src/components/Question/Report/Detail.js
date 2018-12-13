/**
 * 问卷答卷详情首页
 */
import React, { Component } from "react";
import { Layout, message, Row } from "antd";
import ReportAnswer from "./Ansers";

const {
    Header, Content, Footer
} = Layout;


class ReportDetail extends Component {
    constructor(props){
        super(props);
        this.state = {
            id: this.props.match.params.id,
            detail: {},
            jobDetail: {},
        }
    }

    componentDidMount(){
        // 获取问卷 答卷信息
        this.fetchDetailData();
    }

    fetchDetailData = () => {
        const url = "http://127.0.0.1:8090/api/v1/question/report/" + this.state.id;
        fetch(url, {method: "GET", credentials: "include"})
           .then(response => response.json())
           .then(data => {
               if(data.id){
                   this.setState({
                       detail: data
                   });
                   this.fetchJobDetailData(data.job);
               }else{
                   message.error(JSON.stringify(data), 5);
               }
           })
           .catch(err => console.log(err));
    }

    fetchJobDetailData = (id) => {
        const url = "http://127.0.0.1:8090/api/v1/question/job/" + id;
        fetch(url, {method: "GET", credentials: "include"})
           .then(response => response.json())
           .then(data => {
               if(data.id){
                   this.setState({
                       jobDetail: data
                   });
               }else{
                   message.error(JSON.stringify(data), 5);
               }
           })
           .catch(err => console.log(err));
    }

    render() {
        return (
            <Layout>
                <Header>
                    <h1 style={{color: "#F9F9F9"}}>答卷</h1>
                </Header>
                <Content>
                    <div className="container question-report">
                        <div className="header">
                             <h2>{this.state.jobDetail.title}</h2>
                        </div>
                        <div className="description">
                            {this.state.jobDetail.description}
                        </div>

                        <div className="answers">
                            <Row className="title">
                                <h4>回答信息</h4>
                            </Row>
                            <ReportAnswer answers={this.state.detail.answers} />

                            <Row className="title">
                                <h4>基本信息</h4>
                            </Row>
                            <div className="info-property">
                                <dl>
                                    <dt>添加者</dt>
                                    <dd>{this.state.detail.user ? this.state.detail.user : "---"}</dd>
                                </dl>
                                <dl>
                                    <dt>回答IP</dt>
                                    <dd>{this.state.detail.ip}</dd>
                                </dl>
                                <dl>
                                    <dt>回答时间</dt>
                                    <dd>{this.state.detail.time_added}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </Content>
                <Footer></Footer>
            </Layout>
        );
    }
}

export default ReportDetail;