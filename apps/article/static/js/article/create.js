$(function() {
        var saveEvent ; //按Ctrl+S进行保存操作
        // 当取消按钮点击的时候，upload隐藏
        $('#btn_upload_cancel').click(function(){
            $($('.upload')[0]).hide();
        });
        //buttons.btn提交前先验证数据
        $(".buttons .btn").bind("click",function(event){
            var dt = document.getElementById('id_created');
            var re_dt = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;
            var flag = re_dt.test(dt.value);
            if(flag == false){
                alert("日期格式错误！");
                event.preventDefault();
                event.stopPropagation();
            }
        });
        // 当上传按钮点击的时候，开始上传图片
        $('#btn_upload').bind("click",function(event){
            event.preventDefault();
            var imagePath = $('#id_filename').val();
            if(imagePath == ""){
                alert("请选择上传的图片");
                return;
            }
            var formData = new FormData($('.upload form')[0]);//html5的特性
            $.ajax({
                type:"POST",
                url: '/article/upload',
                data: formData,
                contentType: false,
                cache: false,
                async:false,
                processData:false,
                success: function(data){
                    testEditor.insertValue(data.url);
                },
                error: function(err){
                    console.log(err);
                }
            });
            event.stopPropagation();
            $($('.upload')[0]).hide();
        });
        testEditor = editormd("editor", {
            width   : "100%",
            height  : document.documentElement.clientHeight - 200,
            name:"content",
            syncScrolling : "single",
            path    : "/static/libs/editor/lib/",
            toolbarIcons : function() {
                            return ["undo", "redo", "|", "bold","del","italic","quote","|",
                                "h1","h2","h3","h4","|",
                                "list-ul","list-ol","hr", "code","code-block" ,"|",
                                "link","reference-link",'upload',"table","|",//"image",默认的上传图片功能，不要
                                "datetime","emoji","html-entities","pagebreak","|",
                                "clear","goto-line","search",
                                "||","watch","preview", "fullscreen","|"
                            ]
                        },
            flowChart: true,
            sequenceDiagram: true,
            value:$("#old_content")[0].value,
            toolbarIconsClass: {
                upload:'fa-picture-o' //指定一个FontAawsome的图标类
            },
            toolbarHandlers : {
                upload : function(cm,icon,cursor,selection) {
                    //var cursor    = cm.getCursor();     //获取当前光标对象，同cursor参数
                    //var selection = cm.getSelection();  //获取当前选中的文本，同selection参数
                    // 替换选中文本，如果没有选中文本，则直接插入
                    cm.replaceSelection("![image]()");
                    // 如果当前没有选中的文本，将光标移到要输入的位置
                    if(selection === "") {
                        cm.setCursor(cursor.line, cursor.ch + 9);
                    }
                    // this == 当前editormd实例
                    //显示上传图片的div
                    $('.upload').show();
                }
            },
            //自定义键盘事件
            disabledKeyMaps:["Cmd-S"],//禁止的按键事件
            onload:function(){
                var ctrlS = {
                    "Cmd-S": saveEvent,
                    "Ctrl-S": saveEvent,
                };
                this.addKeyMap(ctrlS);
            }
        });
        //键盘按键事件
        saveEvent = function(cm){
            // 获取到当前的表单数据
            var formData = new FormData($('#article')[0]);//html5的特性
            formData.delete('created');
            $.ajax({
                type:"POST",
                url: '/article/save',
                data: formData,
                contentType: false,
                cache: false,
                processData:false,
                success: function(data){
                    if (data.sucess){
                        $(".message").text('保存文章成功').show();
                        setTimeout(function(){$(".message").hide(3000)},2000)
                    }else{
                        $(".message").text('保存文章失败').toggleClass('red').show();
                        setTimeout(function(){$(".message").hide(3000);$(".message").toggleClass('red');},2000)
                    }
                },
                error: function(err){
                    $(".message").text('保存文章出错').toggleClass('red').show().hide(8000);
                    $(".message").toggleClass('red')
                }
            });
        };

    });
