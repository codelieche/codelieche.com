/**
 * 问卷详情首页
 */
import React, { Component } from "react";
import { message } from "antd";

import { Layout, Icon } from "antd";

import JobQuestionsForm from "./Form";

const {
    Header, Footer, Content
} = Layout;

class JobDetail extends Component {
    constructor(props) {
        super(props);
        // 问卷的id
        this.state = {
            id: this.props.match.params.id,
            detail: {}
        }
    }

    componentDidMount(){
        // 获取Job的详情
        this.fetchDetailData();
    }

    fetchDetailData = () => {
        const url = "http://127.0.0.1:8090/api/v1/question/job/" + this.state.id;
        fetch(url, {method: "GET", credentials: "include"})
           .then(response => response.json())
           .then(data => {
               if(data.id){
                   this.setState({
                       detail: data
                   });
               }else{
                   message.error(JSON.stringify(data), 5);
               }
           })
           .catch(err => console.log(err));
    }

    handleAddSubmit = (values) => {
        values["job"] = this.state.detail.id;
        // console.log(values);
        // 通过Fetch Post 添加问卷回答
        const url = "http://127.0.0.1:8090/api/v1/question/report/create";
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json"
            },
            credentials: "include",
            body: JSON.stringify(values)
        })
          .then(response => response.json())
            .then(data => {
                // 如果成功会有个id的字段
                if( data.id > 0 ){
                    message.success("问卷回答成功", 3);
                    this.props.history.push(`/question/report/${data.id}`);
                }else{
                    message.error(JSON.stringify(data), 5);
                }
            })
              .catch(err => console.log(err));
    }

    render() {
        // console.log(this.state.detail);
        return (
            <Layout className="question">
                <Header>
                    <div className="title float-l">
                        问卷调查 <Icon type="edit" />
                    </div>
                    <div className="title float-r">
                        {this.state.detail.title}
                    </div>
                </Header>
                <div className="description">
                    { this.state.detail.description ? this.state.detail.description : this.state.detail.title }
                </div>
                <Content>
                    <div className="container question question-job">
                        {/* <div className="header">
                            <h2>{this.state.detail.title}</h2>
                        </div> */}
                        
                        <div className="forms">
                            <JobQuestionsForm 
                            questions={this.state.detail.questions} 
                            handleSubmit={this.handleAddSubmit}/>
                        </div>
                    </div>
                </Content>
                <Footer>
                    <span>感谢您的参与！</span>
                </Footer>
                
            </Layout>
            
        );
    }
}

export default JobDetail;