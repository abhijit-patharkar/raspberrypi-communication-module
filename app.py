import schedule
import time
import datetime as dt
from time import gmtime, strftime
from threading import Thread
from app.ping import Ping
from app import app
from flask_socketio import SocketIO, emit
from app.slave_metric import SlaveMetrics
app.config['SECRET_KEY'] = 'pdus3cre!'
socketio = SocketIO(app)

def sendSlaveMetrics():
    #while 1:
    SlaveMetrics().processMetrics()
    time.sleep(1)
        
def pingServer():
    Ping().pingServer()

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

@socketio.on('date', namespace='/sio')
def render_date(message):
    while 1:
        now = dt.datetime.now()
        emit('date', now.strftime('%Y-%m-%d %H:%M:%S'))
        socketio.sleep(1)

@socketio.on('sockets', namespace='/sio')
def socket_list(message):
    while 1:
        emit('sockets', SlaveMetrics().fetchSocketStatus())
        socketio.sleep(1)

@socketio.on('socketinfo', namespace='/sio')
def socket_information(socketid):
    print('provide information socket ', socketid)
    while 1:
        emit('socketinfo', SlaveMetrics().getSocketMetrics(int(socketid)))
        socketio.sleep(1)

@socketio.on('connect', namespace='/sio')
def client_connected():
    print('client connnected')

if __name__ == "__main__":
    #while 1:
        #sendSlaveMetrics()
        #time.sleep(1)
    #schedule.every(10).seconds.do(pingServer)
    #t1 = Thread(target=run_schedule)
    #t1.start()
    #sendSlaveMetrics()
    #pingServer()
    socketio.run(app, "0.0.0.0", port=5050, debug=True, use_reloader=False)
    