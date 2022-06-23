from common import Data

bd = Data()


def cleanhtml(raw_html):
    import re
    cleantext = re.sub(re.compile('<.*?>'), '', raw_html)
    # remove newline at the beginning
    cleantext = re.sub(re.compile('^\n'), '', cleantext)
    # remove ddouble  newline
    cleantext = re.sub(re.compile('\n\n\n\n'), '\n', cleantext)
    cleantext = re.sub(re.compile('\n\n\n'), '\n', cleantext)
    cleantext = re.sub(re.compile('\n\n'), '\n', cleantext)
    # remove newline at the end
    cleantext = re.sub(re.compile('\n$'), '', cleantext)
    # print(cleantext)
    return cleantext


def export_to_pdf(data):
    """
    It takes the data from the database and exports it to a pdf file
    :param data: the data to be exported
    """
    from fpdf import FPDF

    pdf = FPDF()

    pdf.add_font('DejaVu', fname=r'fonts/Arial_Cyr.ttf', uni=True)
    pdf.add_font('DejaVuBold', fname=r'fonts/Arial_Cyr_Bold.ttf', uni=True)

    for x in data:
        pdf.add_page()
        # print company name
        pdf.set_font('DejaVuBold', size=16)
        pdf.multi_cell(190, 10, str(x['company']), 0, 1, 'C')
        # print job name
        pdf.set_font('DejaVuBold', size=16)
        pdf.cell(190, 10, 'Название', 0, 1, 'L')
        pdf.set_font('DejaVu', size=14)
        pdf.multi_cell(190, 10, str(x['job_name']).capitalize(), 0, 1, 'J')
        # print job region
        pdf.set_font('DejaVuBold', size=16)
        pdf.cell(190, 10, 'Регион', 0, 1, 'L')
        pdf.set_font('DejaVu', size=14)
        pdf.multi_cell(190, 10, str(x['region']), 0, 1, 'J')
        # print job description
        pdf.set_font('DejaVuBold', size=16)
        pdf.cell(190, 10, 'О вакансии', 0, 1, 'L')
        pdf.set_font('DejaVu', size=14)
        pdf.multi_cell(190, 8, cleanhtml(str(x['description'])), 0, 1, 'J')
        # print some data
        pdf.set_font('DejaVu', size=14)
        pdf.cell(190, 4, '', 0, 1, 'L')
        pdf.cell(190, 8, 'Телефон: ' +
                 str(x['phone']), 0, 1, 'L', link=str(x['link']))
        pdf.cell(190, 8, 'Ссылка на вакансию: ' +
                 str(x['link']), 0, 1, 'L', link=str(x['link']))
    pdf.output('data.pdf')

def export_to_txt(data):
    """
    It takes the data from the database and exports it to a txt file
    :param data: the data to be exported
    """
    with open('data.txt', 'w') as f:
        for x in data:
            f.write(str(x['company']) + '\n')
            f.write('Название' + '\n')
            f.write(str(x['job_name']) + '\n')
            f.write('Регион' + '\n')
            f.write(str(x['region']) + '\n')
            f.write('О вакансии' + '\n')
            f.write(cleanhtml(str(x['description'])) + '\n')
            f.write('Телефон: ' + str(x['phone']) + '\n')
            f.write('Ссылка на вакансию: ' + str(x['link']) + '\n')
            f.write('\n\n')

    f.close()

searc_data = bd.search_data('106', 1, False)
export_to_pdf(searc_data)
export_to_txt(searc_data)
