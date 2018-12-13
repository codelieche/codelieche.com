/**
 * 问卷表单的Item
 */

 import React from "react";
import { Form, Input, Radio, Checkbox } from "antd";

class JobFormItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: this.props.data ? this.props.data : {},
        }
    }

    static getDerivedStateFromProps(nexProps, prevState) {
        // 当父组件传递的属性改变的时候，要改变下自身的状态
        if (
            nexProps.data !== prevState.data
        ) {
            return {
                data: nexProps.data,
            };
        } else {
            return null;
        }
    }

    render() {

        const getFieldDecorator = this.props.getFieldDecorator;
        if( this.state.data.category === "radio" ){
            // 处理Option
            let options = this.state.data.choices.map((item, index) => {
                return <Radio value={item.option} key={index}>{item.value}</Radio>
            });
            return (
                <Form.Item label={this.state.data.title}
                help={this.state.data.description}>
                  {getFieldDecorator(`question_${this.state.data.id}`, {
                    rules: [{ required: true, message: this.state.data.title }]
                    })(
                    <Radio.Group>
                        {options}
                    </Radio.Group>
                    )}
                </Form.Item>
            );
        }

        if( this.state.data.category === "checkbox"){
            let options = this.state.data.choices.map((item, index) => {
                return (
                    <Checkbox value={item.option} key={index}>
                        {item.value}
                    </Checkbox>
                );
            });
            return (
                <Form.Item label={this.state.data.title}
                help={this.state.data.description}>
                  {getFieldDecorator(`question_${this.state.data.id}`, {
                    rules: [{ required: true, message: this.state.data.title }]
                    })(
                    <Checkbox.Group>
                        {options}
                    </Checkbox.Group>
                    )}
                </Form.Item>
            );
        }else{
            // 采用Input
            return (
                <Form.Item 
                    label={this.state.data.title}
                    help={this.state.data.description}
                >
                    {getFieldDecorator(`question_${this.state.data.id}`, {
                    rules: [{ required: true, message: this.state.data.title }]
                    })(<Input placeholder="" />)}
                </Form.Item>
            );
        }
        
    }
}

export default JobFormItem;