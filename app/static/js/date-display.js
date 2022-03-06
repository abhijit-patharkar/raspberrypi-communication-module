$(function(){
    var socket = io.connect('http://localhost:5050/sio');
	socket.emit('date', {data: 'send date'});

    socket.on('date', function(date) {
		$('#datetime').html(date);
    });
	socket.on('connect', function(data) {
        
    });
});