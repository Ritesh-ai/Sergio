###	Import custom modules
import sys
sys.path.append('../')
from Toolbox import PandaBox
import datetime

def main():
	pdbx = PandaBox()
	file_name  = "MyFileHere.xlsx"
	listXLTabs = [{
					'report_name':'Sheet name'
					, 'report_result':[{'Company Name': 'Some Company', 'Buyer': 'Unknown', 'ProductID': 'POOROY2N4KIT'}]
					, 'indexState': ['Company Name', 'Buyer', 'ProductID']
				}
				,{
					'report_name':'Another Sheet'
					, 'report_result':[{'Company Name': 'Some Company', 'Buyer': 'Unknown', 'ProductID': 'POOROY2N4KIT'}]
					, 'indexState': ['Company Name', 'Buyer', 'ProductID']
				},{
					'report_name':'Yet another Sheet'
					, 'report_result':[{'Company Name': 'Some Company', 'Buyer': 'Unknown', 'ProductID': 'POOROY2N4KIT'}]
					, 'indexState': ['Company Name', 'Buyer', 'ProductID']
				}]

	pdbx.writeToExcelMulti(listXLTabs, [], file_name, [])

if __name__ == '__main__':
	main()