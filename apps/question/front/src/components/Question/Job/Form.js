/**
 * 问卷的表单
 */
import React from "react";

import { Form, Button, Row } from "antd";

import JobFormItem from "./FormItem";

function hasErrors(fieldsError) {
    return Object.keys(fieldsError).some(field => fieldsError["field"]);
}


class JobQuestionsBaseForm extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            questisons: this.props.questions
        }
    }

    static getDerivedStateFromProps(nexProps, prevState) {
        // 当父组件传递的属性改变的时候，要改变下自身的状态
        if (
            nexProps.questions !== prevState.questions
        ) {
            return {
                questions: nexProps.questions,
            };
        } else {
            return null;
        }
    }

    getFormItems = (getFieldDecorator) => {
        // console.log(this.state.questisons);
        // 根据问题获取表单
        if(this.state.questions && this.state.questions.length > 0){
            let jobFormsItems = this.state.questions.map((item, index) => {
                return <JobFormItem key={index} index={index + 1}
                data={item} getFieldDecorator={getFieldDecorator} />;
            });
            return jobFormsItems;
        }else{
            return <div>无选项</div>;
        }

    }

    handleSubmit = (e) => {
        // 提交表单处理函数
        // Form表单实例化的时候传递了handleSubmit，实际的操作都是调用它
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if(!err){
                // console.log(values);
                this.props.handleSubmit(values);
            }else{
                console.log(err);
            }
        })
        
    }

    render() {
        // Form的一些内建函数
        const { getFieldDecorator, getFieldsError } = this.props.form;

        return (
            <Form onSubmit={this.handleSubmit}>
                {this.getFormItems(getFieldDecorator)}

                <Row className="center button">
                    {/* <Form.Item> */}
                        <Button 
                        type="primary"
                        htmlType="submit"
                        disabled={hasErrors(getFieldsError())}
                        >提交问卷</Button>
                    {/* </Form.Item> */}
                </Row>
            </Form>
        )
    }

}

export default Form.create()(JobQuestionsBaseForm);