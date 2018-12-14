/**
 * 问卷的回答信息
 */
import React from "react";

class ReportAnswer extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            answers: this.props.answers ? this.props.answers : [],
        }
    }

    static getDerivedStateFromProps(nexProps, prevState) {
        // 当父组件传递的属性改变的时候，要改变下自身的状态
        if (
            nexProps.answers !== prevState.answers
        ) {
            return {
                answers: nexProps.answers,
            };
        } else {
            return null;
        }
    }

    getAnswersItems = () => {
        if(this.state.answers && this.state.answers.length > 0){
            let items = this.state.answers.map((item, index) => {
                return (
                    <div className="answer-item" key={index}>
                        <div className="title">
                            {index + 1}. {item.question}
                        </div>
                       <div className="answer">
                           {item.answer}
                       </div>
                    </div>
                );
            });
            return items;
        }else{
            return <h1>无答卷数据</h1>
        }
    }

    render() {
        // console.log(this.state.answers);
        return (
            <div>
                {this.getAnswersItems()}
            </div>
        );
    }
}

export default ReportAnswer;