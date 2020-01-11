from jinja2 import Environment, FileSystemLoader



file_loader = FileSystemLoader('/home/indian/Pictures/toolbox/templates')
env = Environment(loader=file_loader)

template = env.get_template('table_standard.html')


data = """

<th class="text-left">Company Name</th>
<th class="text-left">Buyer11111</th>
<th class="text-left">ProductID</th>

"""

data1 = """
<tr>
    <td class="text-left">My Company</td>
    <td class="text-left">Unknown</td>
    <td class="text-left">POOROY2N4KIT</td>
</tr>
<tr>
    <td class="text-left">My Company1</td>
    <td class="text-left">Unknown1</td>
    <td class="text-left">POOROY2N4KIT1111</td>
</tr>
<tr>
    <td class="text-left">My Company2</td>
    <td class="text-left">Unknown2</td>
    <td class="text-left">POOROY2N4KIT2222</td>
</tr>
"""


temp = template.render(data=data, data1=data1)


with open("testing11.html","w") as file:
    file.write(temp)
"""
<td class="text-left">My Company</td>
<td class="text-left">Unknown</td>
<td class="text-left">POOROY2N4KIT</td>

"""

# template = Template('Hello {{ name }}!')