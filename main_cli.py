from common import Data

data = Data()

def export_to_txt(data):
    """
    It takes the data from the database and exports it to a txt file
    :param data: the data to be exported
    """
    with open('data.txt', 'w') as f:
        for x in data:
            f.write(str(x) + '\n')
    f.close()

def export_to_pdf(data):
    """
    It takes the data from the database and exports it to a pdf file
    :param data: the data to be exported
    """
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Data', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    for x in data:
        pdf.cell(200, 10, str(x[5]), 0, 1, 'L')
    pdf.output('data.pdf', 'F')
    

# get_new_data = input("Do you want to get new data? (y/n) ")
# if get_new_data == "y":
#     data.download_data(
#         "https://mail2.dcz.gov.ua/publikaciya/6-perelik-aktualnyh-vakansiy-stanom-na-datu")
#     print("Data downloaded")

while True:
    columns = data.get_columns()
    print('Which columns to look for')
    for i in range(len(columns)):
        print(str(i) + ": " + columns[i])
    column_number = input(
        "Enter the number of the column you want to look for: ")
    if column_number.isdigit():
        column_number = int(column_number)
        if column_number in range(len(columns)):
            search_text = input("Enter the text you want to search for: ")
            exact_search = input(
                "Do you want to search for an exact match? (y/n): ")
            if exact_search == "y":
                exact_search = True
            else:
                exact_search = False
            searc_data = data.search_data(
                search_text, column_number, exact_search)

            export_to_txt(searc_data)
            export_to_pdf(searc_data)

            print("Done" + '\n')



