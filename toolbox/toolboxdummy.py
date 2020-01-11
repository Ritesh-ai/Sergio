import datetime
import htmlContent
from jinja2 import Environment, FileSystemLoader


file_loader = FileSystemLoader('/home/indian/Pictures/toolbox/templates')
env = Environment(loader=file_loader)


def buildHTML(**kwargs):
    """
        Build HTML file from SQL query 
    """
    report_name 	= kwargs.get('report_name'	,None)
    report_result 	= kwargs.get('report_result',None)
    indexState 		= kwargs.get('indexState'	,None)
    template 		= kwargs.get('template'	    ,None)
    index 		    = kwargs.get('index'	    ,None)

    if not report_name or not report_result or not indexState:
        print(80*"*")
        print("A report name, dataset & headers are required to continue")
        print(80*"*")
        return

    print(f"\t* * *\t{datetime.datetime.now()}	Data collected.  Writing file to HTML")
    ########			ADD HEADERS

    final_html = ""
    if template == 'BuildHTML':
        # template = env.get_template('table_standard.html')
        # data = ""
        # for cell in indexState:
        #     data = f'{data}<th bgcolor="Yellow"><font size="2" face="verdana"><B>{cell}</b><font></th>'

        # for i1, row in enumerate(report_result):
        #     if i1 % 2 == 0:
        #         highlight_color = "ffffff"
        #     else:
        #         highlight_color = "e6e6e6"
        #     HTML_TABLE_ROW_START = f'<tr bgcolor="#{highlight_color}">'
        #     final_html = f'{final_html}{HTML_TABLE_ROW_START}'
        #     HTML_TABLE_ROW = ""
        #     for i, cell in enumerate(row):
        #         HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td><font size="2" face="verdana">{row[cell]}</font></td>'
        #     final_html = f'{final_html}{HTML_TABLE_ROW}'
        #     final_html = f'{final_html}{HTML_TABLE_ROW}</tr>'


        HTML_header = htmlContent.HTML_header_Build
        final_html = HTML_header
        HTML_TABLE_HEADER = "<thead>"
        for cell in indexState:
            HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}<th bgcolor="Yellow"><font size="2" face="verdana"><B>{cell}</b><font></th>'
        HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}</thead>'

        final_html = f'{final_html}{HTML_TABLE_HEADER}'
        HTML_BEGIN_TABLE = "\r\n<tbody>\r\n"
        final_html = f'{final_html}{HTML_BEGIN_TABLE}'

        for i1, row in enumerate(report_result):
            if i1 % 2 == 0:
                highlight_color = "ffffff"
            else:
                highlight_color = "e6e6e6"
            HTML_TABLE_ROW_START = f'<tr bgcolor="#{highlight_color}">'
            final_html = f'{final_html}{HTML_TABLE_ROW_START}'
            HTML_TABLE_ROW = ""
            for i, cell in enumerate(row):
                HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td><font size="2" face="verdana">{row[cell]}</font></td>'
            final_html = f'{final_html}{HTML_TABLE_ROW}</tr>'
        HTML_END = "</tbody></table></body></html>"
        final_html = f'{final_html}{HTML_END}'
        final_html = final_html.replace('\n','')
        final_html = final_html.replace('\r','')
        final_html = final_html.replace('\t','')
        return final_html

    elif template == 'BuildHTMLFancy':
        # Done with the Template Part
        template = env.get_template('table_fancy.html')
        data = ""
        for cell in indexState:
            data = f'{data}<th class="text-left">{cell}</th>'
        data1 = ""
        for row in report_result:
            HTML_TABLE_ROW_START = f'<tr>'
            data1 = f'{data1}{HTML_TABLE_ROW_START}'
            HTML_TABLE_ROW = ""
            for cell in row:
                HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td class="text-left">{row[cell]}</td>'
            data1 = f'{data1}{HTML_TABLE_ROW}</tr>'

        final_html = template.render(data=data, data1=data1)
        return final_html

    elif template == 'buildHTMLFancyResponstable':
        HTML_header = htmlContent.HTML_header_Build_Responstable
        final_html = HTML_header
        HTML_TABLE_HEADER = "<thead><tr>"
        for cell in indexState:
            HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}<th>{cell}</th>'
        HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}</tr></thead>'

        final_html = f'{final_html}{HTML_TABLE_HEADER}'

        for i1, row in enumerate(report_result):
            HTML_TABLE_ROW_START = f'<tr>'
            final_html = f'{final_html}{HTML_TABLE_ROW_START}'
            HTML_TABLE_ROW = ""
            for i, cell in enumerate(row):
                HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td>{row[cell]}</td>'
            final_html = f'{final_html}{HTML_TABLE_ROW}'

        _final_html = final_html.split('</thead>')
        final_html = _final_html[0]+"</thead><tbody>"+_final_html[1]

        HTML_END = "</tr></tbody></table></body></html>"
        final_html = f'{final_html}{HTML_END}'
        return final_html
    elif template == 'sortable':
        HTML_header = htmlContent.HTML_header_Build_Responstable
        final_html = HTML_header

        TABLE_Head = """<table id='tablelinks"""+str(index)+"""'class="table table-striped table-bordered" style="width:100%">"""

        HTML_TABLE_HEADER = "<thead><tr>"
        for cell in indexState:
            HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}<th>{cell}</th>'
        HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}</tr></thead>'

        final_html = f'{final_html}{TABLE_Head}{HTML_TABLE_HEADER}'

        for row in report_result:
            HTML_TABLE_ROW = ""
            for _, cell in enumerate(row):
                HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td>{row[cell]}</td>'
            HTML_TABLE_HEADER = f'<tr>{HTML_TABLE_ROW}</tr>'
            final_html = f'{final_html}{HTML_TABLE_HEADER}'
        
        final_html1 = final_html.split('</thead>')
        final_html = final_html1[0]+"</thead><tbody>"+final_html1[1]
        
        HTML_END = "</tr></tbody></table></body></html>"
        final_html = f'{final_html}{HTML_END}'
        
        js = """<script>$(document).ready(function() {$('#tablelinks"""+str(index)+"""').DataTable();} );</script>"""
        final_html = f'{final_html}{js}'
        return final_html