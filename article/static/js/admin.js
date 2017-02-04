
window.onload  = function (){
    var t = document.getElementsByClassName('vLargeTextField')[0];
    var editor = new Editor({
        height: "200px"
    });
    editor.render(t);
}


