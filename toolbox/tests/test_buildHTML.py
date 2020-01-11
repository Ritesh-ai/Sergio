###	Import custom modules
import sys
sys.path.append('../')
from toolboxdummy import buildHTML
import datetime

def main():
	# tlbx = Toolbox()
	listXLTabs = {
					'report_name':'Sheet name'
					, 'report_result':[{'Company Name': 'My Company', 'Buyer': 'Unknown', 'ProductID': 'POOROY2N4KIT'}
					, {'Company Name': 'My Company1', 'Buyer': 'Unknown1', 'ProductID': 'POOROY2N4KIT1111'}
					, {'Company Name': 'My Company2', 'Buyer': 'Unknown2', 'ProductID': 'POOROY2N4KIT2222'}]
					, 'indexState': ['Company Name', 'Buyer', 'ProductID']
					, 'template' : 'BuildHTML'				# BuildHTML, BuildHTMLFancy, buildHTMLFancyResponstable, sortable
					, 'index': 0
				}
	# final_html = tlbx.buildHTML(**listXLTabs)
	final_html = buildHTML(**listXLTabs)
	print(final_html)

	with open('data.html','w') as f:
		f.write(final_html)

if __name__ == '__main__':
	main()