import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import math
import json
from flask import render_template, request, send_from_directory
from flask import jsonify
from app.config import Config
from app import app
from functools import wraps
from flask import request, redirect, url_for

iscomp = Config().isComplete()

def socket_status(slave_id,socket_id,status):
    PORT = 'COM7'		
    logger = modbus_tk.utils.create_logger("console")
    try:
        socketStatus = {}
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT, baudrate=57600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        master.set_timeout(5.0)
        master.set_verbose(True)
        logger.info("connected")
        #master.execute(slave_id, cst.WRITE_SINGLE_COIL, socket_id, output_value=status)
        status = master.execute(slave_id, cst.READ_COILS,socket_id-1,socket_id)
        if status[0] == 1:
        	status = 'ON'
        else:
        	status = 'OFF'	
        socketStatus['status']	= status 
        return socketStatus
        master.close()
    except modbus_tk.modbus.ModbusError as exc:
        logger.error("%s- Code=%d", exc, exc.get_exception_code())
        master.close()

def is_configured(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		iscomplete = Config().isComplete()
		if iscomplete == 0:
			return redirect(url_for('config', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css',path)

@app.route('/img/<path:path>')
def send_img(path):
	return send_from_directory('img',path)	

@app.route('/menu')
def menu():
	return render_template('menu.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config')
def config():
	config = Config().fetch()
	return render_template('config.html', config=config)

@app.route('/network')
def network():
	config = Config().fetch()
	return render_template('network.html', config=config)

@app.route('/config' ,methods=['POST'])
def config1():
	config = Config()
	config.updateUnitIdentifier(request.form['unitIdentifier'])
	config.updateMgmtServerIp(request.form['mgmtServerIp'])
	return render_template('config.html', config=config.fetch())

@app.route('/network' ,methods=['POST'])
def save_net_settings():
	config = Config()
	config.updateNetworkSettings(request.form['address'], 
		request.form['netmask'], 
		request.form['gateway'],
		request.form['dns_servers'],
		request.form['search_domains'])
	return render_template('network.html', config=config.fetch())

@app.route('/sockets')
def sockets():
	return render_template('sockets.html')

@app.route('/socket/<int:socket_id>')
def socket_info(socket_id):
	return render_template('socket-info.html', sid=socket_id)

@app.route('/status', methods = ['GET'])
def Status():
    no_of_sockets_in_slave = 6
    message = {
            'UnitSerialNumber':request.args['serialNo'],
            'socketNumber':request.args['socketNo'],
            'action':request.args['action'] ,
    }
    socket_no = int(request.args['socketNo'])
    socket_id = socket_no % no_of_sockets_in_slave
    slave_id = math.floor(socket_no / no_of_sockets_in_slave)
    if slave_id == 0:
    	slave_id = 1
    if request.args['action'] == 'ON':
    	status = 1 
    else :
    	status = 0	 
    resp = jsonify(socket_status(slave_id,socket_id,status))
    resp.status_code = 200
    return resp		
        
@app.route('/secret_page')
@is_configured
def secret_page():
	pass

