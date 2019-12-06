from flask import Flask, render_template
from flask_socketio import SocketIO, ConnectionRefusedError
import time
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
stop = False

GLOBAL1 = 'global1'

@socketio.on('connect')
def connect():
    print('connect event', )
    raise ConnectionRefusedError({'hello': 'world'})



@socketio.on('hello')
def hello(msg):
    socketio.emit('greet', 'begin ' + msg)
    #socketio.start_background_task(fib,1,1,int(msg))
    # echoo('direct ', int(msg))
    socketio.start_background_task(sleepInf)
    socketio.start_background_task(echoo, 'background ', int(msg))



def fib(carry, val,loop):
    loop-=1
    sum = carry+val
    emitV(carry)
    if(loop == 0):
        return sum
    else:
        fib(sum, carry,loop)

def emitV(num):
    socketio.sleep(.3)
    socketio.emit('greet', num)

def echoo(val, num):
    for i in range(1, 10000000):
        # socketio.sleep(.3)
        if i%100000==0 :
            #socketio.sleep(.3)
            socketio.emit('greet', val + str(num))
    global stop 
    stop = True

def sleepInf():
    count = 1
    while not stop:
        #socketio.emit('greet', 'woke')
        count+=1
        socketio.emit('greet', 'count '+ str(count))
        socketio.sleep(5)
    socketio.emit('greet', 'count '+ str(count))
            
@socketio.on('fetchGlobal')
def globalVar(val):
    socketio.emit('msg', GLOBAL1)

def ack_cb(msg):
    print('msg received')
    print(msg)

@socketio.on('ack')
def ack(val, cb):
    #socketio.emit('ack_res','received', callback=ack_cb)
    cb(val)
    #socketio.emit('ack_res', 'ack_res', callback=ack_cb)
    


if __name__ == '__main__':
    socketio.run(app, debug=True)