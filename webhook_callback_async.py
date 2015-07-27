import Queue
import threading
import time
from flask import Flask

callback_queue = Queue.Queue()

def from_dummy_thread(func_to_call_from_main_thread):
    callback_queue.put(func_to_call_from_main_thread)

def from_flask_thread(func_to_call_from_main_thread):
    callback_queue.put(func_to_call_from_main_thread)

def from_main_thread_blocking():
    callback = callback_queue.get() #blocks until an item is available
    callback()

def from_main_thread_nonblocking():
    while True:
        try:
            callback = callback_queue.get(False) #doesn't block
        except Queue.Empty: #raised when queue is empty
            break
        callback()

def print_num(dummyid, n):
    print "From %s: %d" % (dummyid, n)


def dummy_run(dummyid):
    for i in xrange(5):
        from_dummy_thread(lambda: print_num(dummyid, i))
        time.sleep(0.5)

def flask_webhook(thid):
	app = Flask(__name__)


	@app.route('/message')
	def hello_world():
		print 'Flask got message'
		from_flask_thread(lambda: print_num(thid, 12))
	

	app.run()

	


#threading.Thread(target=dummy_run, args=("a",)).start()
threading.Thread(target=flask_webhook, args=("Flask",)).start()

while True:
    #from_main_thread_blocking()
    from_main_thread_nonblocking()