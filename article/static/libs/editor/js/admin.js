console.log(document.getElementById('id_content'));
var testEditor;
$(function() {
    console.log(document.getElementById('id_content'));
    testEditor = editormd("id_content", {
        width   : "800px",
        height  : 240,
        // syncScrolling : "single",
        path    : "/static/libs/editor/lib/",
        saveHTMLToTextarea: true,
        // flowChart : true,
        // sequenceDiagram : true,
        // imageUpload : true,
        // imageFormats : ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        // imageUploadURL : "./php/upload.php?test=dfdf",
    });
    console.log("========");
});

// window.onload = function () {
//     testEditor = editormd("id_content", {
//         width   : "800px",
//         height  : 240,
//         // syncScrolling : "single",
//         path    : "/static/libs/editor/lib/",
//         // flowChart : true,
//         // sequenceDiagram : true,
//         // imageUpload : true,
//         // imageFormats : ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
//         // imageUploadURL : "./php/upload.php?test=dfdf",
//     });
// }