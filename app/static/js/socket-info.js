$(function(){
    var socketid = $('#sid').val();
    if(!socketid) {
        return;
    }

    var socket = io.connect('http://localhost:5050/sio');
	socket.emit('socketinfo', socketid);
    socket.on('socketinfo', function(socketinfo) {
        $('.content').show();
        
		if(socketinfo && !($.isEmptyObject(socketinfo))) {
           $('#ap').html(socketinfo.ap);
           $('#pc').html(socketinfo.pc);
           $('#v').html(socketinfo.v);
           $('#c').html(socketinfo.c);
           $('#apw').html(socketinfo.apw);
           $('#f').html(socketinfo.f);
           $('#rp').html(socketinfo.rp);
           $('#pf').html(socketinfo.pf);
           $('#status-img').attr("src", getStatusImg(socketinfo.Status));
        } else {
            $('.content').html('No socket data available.');
        }
    });

    var getStatusImg = function(status) {
        if(status) {
            return '/img/grn-status.png';
        }
        return '/img/red-status.png';
    }
});