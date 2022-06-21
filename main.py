import os
import re
import sqlite3
import xml.etree.ElementTree as ET
import zipfile

import requests


class Downloader_Data:
    def __init__(self, url):
        self.domain = re.search(r'(https?://[^/]+)', url).group(1)
        self.get_data = requests.get(url).text
        self.chunk_size = 1024
        self.tmp_dir = "tmp"
        self.down_data_name = "data.zip"
        self.name_data = "data.xml"
        self.file_url = ""
        self.__search_url__()

    def __search_url__(self):
        regexp = re.compile('<a.*?href="(.*?)".*?>(.*?)</a>')
        data_url = regexp.findall(self.get_data)
        for i in data_url:
            regexp = re.compile(r"sites/default/files/.+?.zip")
            url = regexp.findall(i[0])
            if url:
                self.file_url = self.domain + "/" + url[0]
                self.__download_file__()
                break

    def __download_file__(self):
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
        r = requests.get(self.file_url, stream=True)
        with open(self.tmp_dir + '/' + self.down_data_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()
        self.__extract_file__()

    def __extract_file__(self):

        with zipfile.ZipFile(self.tmp_dir + '/' + self.down_data_name, 'r') as zip_ref:
            zip_ref.extractall(self.tmp_dir)
            zip_ref.close()
            os.remove(self.tmp_dir + '/' + self.down_data_name)
            for file in os.listdir(self.tmp_dir):
                os.rename(os.path.join(self.tmp_dir, file),
                          os.path.join(self.tmp_dir, self.name_data))

    def delete_tmp(self):
        if os.path.exists(self.tmp_dir):
            os.rmdir(self.tmp_dir)

    def file_data(self):
        data = ET.parse(self.tmp_dir + '/' + self.name_data)
        data = data.getroot()
        return data


class Parse_And_Save_Data:
    def __init__(self, data):
        self.data = data
        self.conn = sqlite3.connect('data.db')  # connect to the database
        self.cur = self.conn.cursor()  # create a cursor

        # Create table if it doesn't exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTOINCREMENT, id_job INTEGER, link TEXT, name TEXT, region TEXT, description TEXT, pubdate TEXT, salary TEXT, company TEXT, expire TEXT, jobtype TEXT, phone TEXT)''')
        self.parse_data()

    def parse_data(self):
        for x in self.data:
            data = dict()  # create array to store data
            data['id_job'] = x.attrib.get('id')
            data['link'] = self.__parse_cdata__(x.find('link'))
            data['name'] = self.__parse_cdata__(x.find('name'))
            data['region'] = self.__parse_cdata__(x.find('region'))
            data['description'] = self.__parse_cdata__(x.find('description'))
            data['pubdate'] = self.__parse_cdata__(x.find('pubdate'))
            data['salary'] = self.__parse_cdata__(x.find('salary'))
            data['company'] = self.__parse_cdata__(x.find('company'))
            data['expire'] = self.__parse_cdata__(x.find('expire'))
            data['jobtype'] = self.__parse_cdata__(x.find('jobtype'))
            data['phone'] = self.__parse_cdata__(x.find('phone'))
            self.parse_data = data
            self.__save_data__()
        self.conn.commit()  # commit changes to database
        self.conn.close()  # close connection to database

    def __parse_cdata__(self, data):
        try:
            data = data.text  # get the text inside the cdata
        except AttributeError:
            data = ''
        data = data.replace('![CDATA[', '')  # remove the cdata tag
        data = data.replace(']]', '')  # remove the cdata tag
        return data

    def __save_data__(self):
        # insert data to database
        columns = ', '.join(self.parse_data.keys())  # get all keys from data
        # get all placeholders from data
        placeholders = ', '.join('?' * len(self.parse_data))
        sql = 'INSERT INTO data ({}) VALUES ({})'.format(
            columns, placeholders)  # create sql query
        # get all values from data
        values = [int(x) if isinstance(x, bool)
                  else x for x in self.parse_data.values()]
        self.cur.execute(sql, values)  # execute sql query


data = Downloader_Data("https://mail2.dcz.gov.ua/publikaciya/6-perelik-aktualnyh-vakansiy-stanom-na-datu")
data = data.file_data()

Parse_And_Save_Data(data)
