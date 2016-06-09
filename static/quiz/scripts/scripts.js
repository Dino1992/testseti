function sizeCalc() {
    var w = window.innerWidth;
    var h = window.innerHeight;
    var scaleRatio = 1.77;
    var container = document.getElementById("container");
    if(w / h > scaleRatio) {
        container.style.height = '' + h + 'px';
        container.style.top = '0px';
        var newWidth = Math.floor(h * scaleRatio);
        container.style.width = '' + newWidth + 'px';
        container.style.left = '' + Math.floor((w - newWidth) / 2) + 'px';
        container.style.fontSize = '' + h + 'px';
    } else {
        container.style.width = '' + w + 'px';
        container.style.left = '0px';
        var newHeight = Math.floor(w / scaleRatio);
        container.style.height = '' + newHeight + 'px';
        container.style.top = '' + Math.floor((h -  newHeight) / 2) + 'px';
        container.style.fontSize = '' + newHeight + 'px';
    }
}

window.addEventListener("resize", function(e) {
    sizeCalc();
});


function submit(action) {
    document.getElementById('action').value = action;
    document.getElementById('quiz_form').submit();
}