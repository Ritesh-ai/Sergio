from Toolbox import Toolbox
import csv

def main():
	tlbx = Toolbox()
	sheet_name = "Some title here"
	csv1 = """Name,Profession
		Derek,Software Developer
		Steve,Software Developer
		Paul,Manager"""
	csv2 = """Name,Profession
		Bob,Software Developer
		Bill,Software Developer
		Stacy,Manager"""
	csv3 = """Name,Profession
		Jennifer,Software Developer
		Bernard,Software Developer
		William,Manager"""
	gsheet = tlbx.gsheet_new_sheet(sheet_name, ['anubhadoriya1994@gmail.com'])
	gsheet_id = gsheet.id
	print(gsheet_id)
	tlbx.gsheet_upload_csv(gsheet, sheet_name, gsheet_id, csv1)
	
	
if __name__ == '__main__':
	main()

