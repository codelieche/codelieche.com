# -*- coding:utf-8 -*-
from rest_framework import serializers

from wenjuan.models.question import Job, Report, Answer
# from wenjuan.serializer.question import JobModelSerializer
from wenjuan.serializer.answer import AnswerDetailSerializer


class ReportModelSerializer(serializers.ModelSerializer):
    """
    Report Model Serializer
    """
    def check_job_answers(self, job):
        # print("validate_answers", job)
        # 1. 获取到问卷的所有问题
        questions = job.questions.all()
        # 答卷的回答
        answers_list = []

        # 2. 开始检查问题
        request = self.context["request"]
        for question in questions:
            # 根据question的类型来处理
            category = question.category
            field_name = "question_{}".format(question.id)
            field_value = request.data.get(field_name)
            # 判断传入的值是否为空
            if not field_value:
                raise serializers.ValidationError("问题(ID:{})：{}，回答未填写".format(question.id, question.title))

            # 判断是否需要唯一值
            if question.is_unique:
                # 从答案中查找相关的值【注意：只有用户自己输入的才可能需要唯一值，单选和复选框是没唯一值一说的】
                if category == "text":
                    answer_exist = Answer.objects.filter(question=question, answer=field_value).first()
                    if answer_exist:
                        raise serializers.ValidationError(
                            "问题(ID:{})：{}，回答值需唯一！值({})已经提交".format(question.id, question.title, field_value))
            if category == "radio":
                # 如果是单选或者多选框，需要校验结果
                choice = question.choices.filter(option=field_value).first()
                if not choice:
                    raise serializers.ValidationError(
                        "问题(ID:{}):{}，没有{}这个选项".format(question.id, question.title, field_value))
                else:
                    # 添加answer
                    answer = Answer(question=question, option=field_value, answer=choice.value)
                    answers_list.append(answer)
                # 创建answer
            elif category == "checkbox":
                # 如果是checkbox就需要对多个选项都进行检查
                # 检查字段的值是否为空
                option_field = ",".join(field_value)
                answer_field_list = []
                for v in field_value:
                    choice = question.choices.filter(option=v).first()
                    if not choice:
                        raise serializers.ValidationError(
                            "问题(ID:{}):{}，没有{}这个选项".format(question.id, question.title, v))
                    else:
                        answer_field_list.append(choice.value)

                # 选项
                answer_field = ",".join(answer_field_list)
                # 添加answer
                answer = Answer(question=question, option=option_field, answer=answer_field)
                answers_list.append(answer)

            else:
                # input
                # 添加answer
                answer = Answer(question=question, answer=field_value)
                answers_list.append(answer)
        # 返回answers
        return answers_list

    def create(self, validated_data):
        # 1. get job
        job = validated_data["job"]
        request = self.context["request"]

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        validated_data["ip"] = ip

        # 判断是否登录
        user = request.user
        if job.is_authenticated:
            # 需要用户登录才ok
            if not user.is_authenticated:
                raise serializers.ValidationError("需要登录才可以回答")
            validated_data["user"] = user
        else:
            if user.is_authenticated:
                validated_data["user"] = user

        # check job answer data
        answers = self.check_job_answers(job=job)

        instance = super().create(validated_data=validated_data)
        for answer in answers:
            answer.save()

            instance.answers.add(answer)
        return instance

    class Meta:
        model = Report
        fields = ("id", "job", "user", "ip", "time_added", "answers")


class ReportDetailSerializer(serializers.ModelSerializer):
    """
    问卷回答详情api
    """
    # job = JobModelSerializer(read_only=True)
    answers = AnswerDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ("id", "job", "user", "ip", "time_added", "answers")
