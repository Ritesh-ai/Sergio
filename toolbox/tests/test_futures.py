import concurrent.futures
import random 
import datetime
import time
import uuid

def do_something(seconds, name, i):
	print(f"{i}\tSleeping {seconds}\t{name}\t{str(datetime.datetime.now())[:19][11:]}")
	time.sleep(seconds)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
	for i in range(1000):
		executor.submit(do_something
			, seconds = random.randint(1,6)
			, name = str(uuid.uuid4())[:6].upper()
			, i = i)
