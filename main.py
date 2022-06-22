from common import Data

data = Data()
data.download_data(
    "https://mail2.dcz.gov.ua/publikaciya/6-perelik-aktualnyh-vakansiy-stanom-na-datu")
data = data.search_data('програміст', 'name')

with open('data.txt', 'w') as f:
    for i in data:
        f.write(str(i))
        f.write('\n')
