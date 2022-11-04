import re

list = ['$23.2','$49.6','$43.97','$89.098']

for item in list:
    entry = re.findall(r'[\d]*[.][\d]+',item)
    # print(item)
    res = float(entry[0])
    print(res)