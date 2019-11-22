$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('mqtt_data', function(msg) {
        $('#mqtt_string0').html(msg.mqtt_string0);
        $('#mqtt_string1').html(msg.mqtt_string1);
    });
});