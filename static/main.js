/* global io */

import * as line from "./line.js";
import * as matrix from "./matrix.js";

var main = function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/main');
    socket.on('message', function(data) {
        var li = document.createElement('li');
        li.textContent = JSON.stringify(data);
        document.querySelector('#messages').append(li);

        window.scrollTo(0, document.body.scrollHeight);
    });
    socket.on('csv', function(data) {
        if (data.type == 'line') {
            line.add(data);
        } else {
            matrix.add(data);
        }

        window.scrollTo(0, document.body.scrollHeight);
    });
};

((callback) => {
    if (document.readyState != "loading") callback();
    else document.addEventListener("DOMContentLoaded", callback);
})(main);
