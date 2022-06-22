from common import Data

data = Data()
data.download_data("https://mail2.dcz.gov.ua/publikaciya/6-perelik-aktualnyh-vakansiy-stanom-na-datu")

columns = data.get_columns()

while True:
    print('Which columns to look for')
    for i in range(len(columns)):
        print(str(i) + ": " + columns[i])
    column_number = input("Enter the number of the column you want to look for: ")
    if column_number.isdigit():
        column_number = int(column_number)
        if column_number in range(len(columns)):
            search_text = input("Enter the text you want to search for: ")
            exact_search = input("Do you want to search for an exact match? (y/n): ")
            if exact_search == "y":
                exact_search = True
            else:
                exact_search = False
            searc_data = data.search_data(search_text, column_number, exact_search)

            with open('data.txt', 'w') as f:
                for i in searc_data:
                    f.write(str(i))
                    f.write('\n')
            f.close()
            print("Done")