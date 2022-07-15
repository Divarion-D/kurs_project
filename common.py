import os
import re
import sqlite3
import xml.etree.ElementTree as ET
import zipfile
import shutil
import requests
from fpdf import FPDF


# Он загружает данные из url, анализирует их и сохраняет.
class Data:
    def __init__(self):
        self.conn = sqlite3.connect('data.db') # создаем соединение с базой данных
        self.cur = self.conn.cursor() # создаем курсор
        self.parse_data = '' # пустой список для данных

        # Создаем таблицу если ее нет
        self.cur.execute('''CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTOINCREMENT, id_job INTEGER, link TEXT, job_name TEXT, region TEXT, description TEXT, pubdate TEXT, salary TEXT, company TEXT, expire TEXT, phone TEXT)''')
        self.cur.execute("SELECT * FROM data") # устанавливаем курсор на таблицу
        self.columns = [description[0]
                        for description in self.cur.description] # получаем названия столбцов
        self.conn.commit() # подтверждаем изменения в базе данных

    def download_data(self, url):
        """
        Он загружает данные из url, анализирует их и сохраняет.
        :param url: Ссылка на сайт вакансий
        """
        # Очистить базу данных если в ней есть данные
        if self.get_count_row() > 0:
            self.cur.execute('''DELETE FROM data''')
            self.conn.commit()
        
        data_down = Downloader_Data(url) # Загрузить данные
        self.parse_data = data_down.file_data() # получаем данные из файла
        data_down.delete_tmp() # удаляем временную папку
        self.save_data() # сохраняем данные в базу данных

    def save_data(self):
        """
        Он получает данные из функции parse_data и сохраняет их в файл
        """
        Parse_And_Save_Data(self.parse_data)

    def get_columns(self):
        """
        Получить названия столбцов
        :return: Названия столбцов
        """
        collumns_dict = dict() # словарь для названий столбцов
        for i in range(len(self.columns)): 
            collumns_dict[i] = self.columns[i]  # заполняем словарь
        collumns_dict.pop(0) # удаляем первый элемент из словаря
        return collumns_dict # возвращает словарь

    def get_count_row(self):
        """
        Получить количество строк в таблице
        :return: Количество строк
        """
        self.cur.execute("SELECT COUNT(*) FROM data")
        return self.cur.fetchone()[0]

    def get_all_data_column(self, column):
        """
        Получить все данные из столбца
        :param column: ID столбца
        :return: Все данные из столбца
        """
        self.cur.execute("SELECT * FROM data")
        return [row[column+1] for row in self.cur.fetchall()]


    def export_to_txt(self, data, file_name):
        """
        Он экспортирует данные в файл txt
        :param data: Данные для экспорта
        :param file_name: Имя файла
        """

        with open(file_name, 'w') as f:
            for x in data:
                f.write(str(x['company']) + '\n')
                f.write('Название' + '\n')
                f.write(str(x['job_name']) + '\n')
                f.write('Регион' + '\n')
                f.write(str(x['region']) + '\n')
                f.write('О вакансии' + '\n')
                f.write(str(x['description']))
                f.write('Телефон: ' + str(x['phone']) + '\n')
                f.write('Ссылка на вакансию: ' + str(x['link']) + '\n')
                f.write('\n\n')
    
    def export_to_pdf(self, data, file_name):
        """
        Он экспортирует данные в файл pdf
        :param data: Данные для экспорта
        :param file_name: Имя файла
        """
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
            pdf.multi_cell(190, 8, str(x['description']), 0, 1, 'J')
            # print some data
            pdf.set_font('DejaVu', size=14)
            pdf.cell(190, 4, '', 0, 1, 'L')
            pdf.cell(190, 8, 'Телефон: ' +
                    str(x['phone']), 0, 1, 'L', link=str(x['link']))
            pdf.cell(190, 8, 'Ссылка на вакансию: ' +
                    str(x['link']), 0, 1, 'L', link=str(x['link']))
        pdf.output(file_name)
    
    def search_data(self, search_text, column_number, exact_search):
        """
        Поиск данных в таблице
        :param search_text: Текст для поиска
        :param column_number: Номер столбца для поиска
        :param exact_search: True, если вы хотите искать точное совпадение, False, если вы хотите искать частичное совпадение
        :return: Данные из базы данных, соответствующие критериям поиска, в словаре
        """
        self.cur.execute('''SELECT * FROM data''')  # устанавливаем курсор на таблицу
        rows = self.cur.fetchall()  # получаем все данные из таблицы
        search_data = []  # создаем пустой список для данных поиска
        for row in rows: # проходим по всем строкам
            if exact_search: # если выбрана точная поисковая строка
                if str(row[column_number+1]) == search_text: # если строка совпадает с поисковой строкой
                    search_data.append(dict(zip(self.columns, row))) # добавляем данные в список
            else:
                if search_text in str(row[column_number+1]): # если строка содержит поисковую строку
                    search_data.append(dict(zip(self.columns, row))) # добавляем данные в список
        return search_data # возвращаем список данных поиска



# Он загружает zip-файл по url, извлекает zip-файл, а затем анализирует xml-файл.
class Downloader_Data(Data):
    def __init__(self, url):
        Data.__init__(self)
        self.domain = re.search(r'(https?://[^/]+)', url).group(1)
        self.get_data = requests.get(url).text
        self.chunk_size = 1024
        self.tmp_dir = "tmp"
        self.down_data_name = "data.zip"
        self.name_data = "data.xml"
        self.file_url = ""
        self.__search_url()

    def __search_url(self):
        """
        Он берет данные из переменной get_data и ищет ссылку, которая заканчивается на .zip
        """
        regexp = re.compile('<a.*?href="(.*?)".*?>(.*?)</a>') # поиск ссылки на файл
        data_url = regexp.findall(self.get_data) # получаем ссылку на файл
        for i in data_url: # проходим по всем ссылкам
            regexp = re.compile(r"sites/default/files/.+?.zip") # поиск ссылки на файл
            url = regexp.findall(i[0]) # получаем ссылку на файл
            if url: # если ссылка на файл найдена
                self.file_url = self.domain + "/" + url[0]  # собрать строку url для скачивания файла
                self.__download_file()  # загрузить файл
                break

    def __download_file(self):
        """
        Он загружает файл по url, а затем извлекает его
        """
        if not os.path.exists(self.tmp_dir):  # если временная папка не существует
            os.makedirs(self.tmp_dir)  # создать временную папку
        r = requests.get(self.file_url, stream=True)  # загрузить файл
        with open(self.tmp_dir + '/' + self.down_data_name, 'wb') as f:  # записать файл в временную папку
            for chunk in r.iter_content(chunk_size=self.chunk_size): # построчно записать файл
                if chunk:  # если есть данные
                    f.write(chunk)  # записать файл
                    f.flush()  # обновить буфер
        self.__extract_file()  # извлечь файл

    def __extract_file(self):
        """
        Распаковка файла
        """
        with zipfile.ZipFile(self.tmp_dir + '/' + self.down_data_name, 'r') as zip_ref:
            zip_ref.extractall(self.tmp_dir)  # распаковать файл
            os.remove(self.tmp_dir + '/' + self.down_data_name) # удалить файл
            for file in os.listdir(self.tmp_dir): # проходим по всем файлам в временной папке
                os.rename(os.path.join(self.tmp_dir, file), 
                          os.path.join(self.tmp_dir, self.name_data))  # переименовать файл

    def delete_tmp(self):
        """
        Удаление временной папки
        """
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def file_data(self):
        """
        Он принимает имя файла, разбирает его и возвращает корень разобранного файла
        :return: корень разобранного файла
        """
        data = ET.parse(self.tmp_dir + '/' + self.name_data)  # парсит файл
        data = data.getroot()  # получает корень файла
        return data


# Разбирает данные из xml и сохраняет их в sqlite
class Parse_And_Save_Data(Data):
    def __init__(self, data):
        Data.__init__(self)
        self.data = data
        self.__parse_data()

    def __parse_data(self):
        """
        Разбирает данные из xml и сохраняет их в sqlite
        """
        for x in self.data:
            data = dict()  # словарь для хранения данных
            # проходим по всем элементам в файле
            data['id_job'] = x.attrib.get('id')
            data['link'] = self.__parse_cdata(x.find('link'))
            data['job_name'] = self.__parse_cdata(x.find('name'))
            data['region'] = self.__parse_cdata(x.find('region'))
            data['description'] = self.__cleanhtml(str(self.__parse_cdata(x.find('description'))))
            data['pubdate'] = self.__parse_cdata(x.find('pubdate'))
            data['salary'] = self.__parse_cdata(x.find('salary'))
            data['company'] = self.__parse_cdata(x.find('company'))
            data['expire'] = self.__parse_cdata(x.find('expire'))
            data['phone'] = self.__parse_cdata(x.find('phone'))
            self.parse_data = data  # записываем данные в переменную
            self.__save_data()  # сохраняем данные в базу данных
        self.conn.commit()  # подтверждаем изменения в базе данных


    def __parse_cdata(self, data):
        """
        Он принимает тег cdata и возвращает текст внутри тега
        :param data: тег cdata
        :return: текст внутри тега
        """
        try:
            data = data.text  # получаем текст внутри тега
        except AttributeError:
            data = '' # если нет текста возвращаем пустую строку
        data = data.replace('![CDATA[', '')  # удаляем тег cdata
        data = data.replace(']]', '')  # удаляем тег cdata
        return data

    def __cleanhtml(self, raw_html):
        """
        Очистка html кода
        :param raw_html: Код html
        :return: Очищенный код html
        """
        cleantext = re.sub(re.compile('<.*?>'), '', raw_html)
        # удалить новую строку в начале
        cleantext = re.sub(re.compile('^\n'), '', cleantext)
        # удалить двойную новую строку
        cleantext = re.sub(re.compile('\n\n\n\n'), '\n', cleantext)
        cleantext = re.sub(re.compile('\n\n\n'), '\n', cleantext)
        cleantext = re.sub(re.compile('\n\n'), '\n', cleantext)
        # удалить новую строку в конце
        cleantext = re.sub(re.compile('\n$'), '', cleantext)
        return cleantext

    def __save_data(self):
        """
        Она берет ключи из словаря, создает строку ключей, разделенных запятыми, затем берет
        значения из словаря, создает строку из разделенных запятыми вопросительных знаков, затем создает
        строку SQL-запроса, затем берет значения из словаря, преобразует булевы значения в целые числа, затем выполняет SQL-запрос.
        в целые числа, затем выполняет SQL-запрос
        """
        columns = ', '.join(self.parse_data.keys())  # получаем строку ключей, разделенных запятыми
        placeholders = ', '.join('?' * len(self.parse_data)) # получаем строку вопросительных знаков, разделенных запятыми
        sql = 'INSERT INTO data ({}) VALUES ({})'.format( 
            columns, placeholders)  # создаем строку SQL-запроса
        values = [int(x) if isinstance(x, bool)
                  else x for x in self.parse_data.values()]  # преобразуем булевы значения в целые числа
        self.cur.execute(sql, values)  # выполняем SQL-запрос
