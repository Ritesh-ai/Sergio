###	Import custom modules
import sys
sys.path.append('../')
from Toolbox import Toolbox

def test_sendMailWithAttachments():
	tlbx = Toolbox()
	kwargs = {'mail_from': ''
			, 'mail_from_name': ''
			, 'mail_password': ''
			, 'mail_to': ''
			, 'mail_subject': ''
			, 'mail_body': ''
			, 'attachment_list': []
			, 'Cc':[]}
	tlbx.sendMailWithAttachments(**kwargs)

def main():
	test_sendMailWithAttachments()

if __name__ == '__main__':
	main()