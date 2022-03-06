$(function(){
    var socket = io.connect('http://localhost:5050/sio');
	socket.emit('sockets', "Initiate socket list websocket.");

    socket.on('sockets', function(socketinfo) {
        $('.content').html('');        
		if(socketinfo) {
            $.each(socketinfo, function(socketid, status) {
                var label = '<label class="caption">Socket - ' + socketid + ' - ' + status + '</label>';
                $('.content').append(buildSocketInfo(socketid, status));
            });
        } else {
            $('.content').html('No socket data available.');
        }
    });
	socket.on('connect', function(data) {
        
    });

    var buildSocketInfo = function(socketid, status) {
        var label = '<a href="/socket/'+ socketid +'"><div class="list-row"><div class="list-lt">';
        label += '<div class="caption">Socket ' + socketid + '</div>';
        label += '<div class="sub"></div></div>';
        label += '<div class="list-rt"><img src="' + getStatusImg(status) + '">';
        label += '</div><div class="clear"></div></div></a>'
        return label;
    };

    var getStatusImg = function(status) {
        if(status) {
            return 'img/grn-status.png';
        }
        return 'img/red-status.png';
    }
});