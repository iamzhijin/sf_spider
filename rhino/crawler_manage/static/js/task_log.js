
function init_ws(task_id) {
    var path = task_id;
    var ws;
    var host = "ws://127.0.0.1:5678/";
    try {
        ws = new WebSocket(host);
        ws.onopen = function () {
            log('Connected');
            ws.send(path)
        };
        ws.onmessage = function (msg) {
            log(msg.data);
        };
        ws.onclose = function () {
            log("Lose Connection!");
        };
        //保持连接
        if(ws.readState == WebSocket.OPEN){
            ws.onopen()
        }
        window.s = ws
    }
    catch (ex) {
        log(ex);
    }
}
// window.onbeforeunload = function () {
//     try {
//         ws.send('quit');
//         ws.close();
//         ws = null;
//     }
//     catch (ex) {
//         log(ex);
//     }
// };
function log(msg) {
    var obje = document.getElementById("log");
    obje.innerHTML += '<p>' + msg + '</p>';
    obje.scrollTop = obje.scrollHeight;   //滚动条显示最新数据
}
function stop() {
    try {
        log('Close connection!');
        socket.send('quit');
        socket.close();
        socket = null;
    }
    catch (ex) {
        log(ex);
    }
}
function closelayer() {
    try {
        log('Close connection!');
        socket.send('quit');
        socket.close();
        socket = null;
    }
    catch (ex) {
        log(ex);
    }
    var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
    parent.layer.close(index); //再执行关闭
}
