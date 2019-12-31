###	Import custom modules
import sys
sys.path.append('../')
from Toolbox import SeleniumBox
import time

def main():
	sbx = SeleniumBox()
	sbx.loadSelenium(**{'driver':'Chrome'
		, 'displayUI':True
		, 'profile':None})
	sbx.loadPage('http://google.com')
	time.sleep(10)

if __name__ == '__main__':
	main()
