import os
import re
import sqlite3
import xml.etree.ElementTree as ET
import zipfile
import shutil
import requests


# It downloads data from a url, parses it, and saves it.
class Data:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')  # connect to the database
        self.cur = self.conn.cursor()  # create a cursor
        self.parse_data = ''

        # Create table if it doesn't exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTOINCREMENT, id_job INTEGER, link TEXT, name TEXT, region TEXT, description TEXT, pubdate TEXT, salary TEXT, company TEXT, expire TEXT, jobtype TEXT, phone TEXT)''')

    def download_data(self, url):
        """
        It downloads data from a url, parses it, and saves it

        :param url: The URL of the file you want to download
        """
        data_down = Downloader_Data(
            url)  # create a new object of the Downloader_Data class
        self.parse_data = data_down.file_data()  # parse the data
        data_down.delete_tmp()  # delete the temporary file
        self.save_data()  # save the data to a file

    def save_data(self):
        """
        It takes the data from the parse_data function and saves it to a file
        """
        Parse_And_Save_Data(self.parse_data)

    def get_columns(self):
        """
        It gets the column names from the database and stores them in a list
        :return: The column names of the table.
        """
        self.cur.execute("SELECT * FROM data")  # set cursor to the table
        self.columns = [description[0]
                        for description in self.cur.description]  # get the column names
        return self.columns  # return the column names

    def search_data(self, search_text, column_number, exact_search):
        #find all data in the column_number that matches the search text
        self.cur.execute("SELECT * FROM data WHERE " + self.columns[column_number] + " LIKE ?", (search_text,))
        search_data = self.cur.fetchall()
        if exact_search:
            search_data = [i for i in search_data if i[column_number] == search_text]
        else:
            search_data = [i for i in search_data if search_text in i[column_number]]
        return search_data
        


# It downloads a zip file from a url, extracts the zip file, and then parses the xml file
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
        It takes the data from the get_data variable, and searches for a link that ends in .zip
        """
        regexp = re.compile('<a.*?href="(.*?)".*?>(.*?)</a>')
        data_url = regexp.findall(self.get_data)
        for i in data_url:
            regexp = re.compile(r"sites/default/files/.+?.zip")
            url = regexp.findall(i[0])
            if url:
                self.file_url = self.domain + "/" + url[0]  # set the file url
                self.__download_file()  # download the file
                break

    def __download_file(self):
        """
        It downloads the file from the url, and then extracts it
        """
        if not os.path.exists(self.tmp_dir):  # if the temporary directory doesn't exist
            os.makedirs(self.tmp_dir)  # create the temporary directory
        r = requests.get(self.file_url, stream=True)  # download the file
        with open(self.tmp_dir + '/' + self.down_data_name, 'wb') as f:  # save the file
            # iterate through the file
            for chunk in r.iter_content(chunk_size=self.chunk_size):
                if chunk:  # if the chunk is not empty
                    f.write(chunk)  # write the chunk to the file
                    f.flush()  # flush the file
            f.close()  # close the file
        self.__extract_file()  # extract the file

    def __extract_file(self):
        """
        It downloads a zip file, extracts it, and then deletes the zip file
        """
        with zipfile.ZipFile(self.tmp_dir + '/' + self.down_data_name, 'r') as zip_ref:
            zip_ref.extractall(self.tmp_dir)  # extract the zip file
            zip_ref.close()  # close the zip file
            # delete the zip file
            os.remove(self.tmp_dir + '/' + self.down_data_name)
            # iterate through the files in the temporary directory
            for file in os.listdir(self.tmp_dir):
                os.rename(os.path.join(self.tmp_dir, file),
                          os.path.join(self.tmp_dir, self.name_data))  # rename the file

    def delete_tmp(self):
        """
        It deletes the temporary directory if it exists
        """
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
        

    def file_data(self):
        """
        It takes a file name, parses it, and returns the root of the parsed file
        :return: The data from the xml file.
        """
        data = ET.parse(self.tmp_dir + '/' + self.name_data) # parse the file
        data = data.getroot() # get the root of the parsed file
        return data # return the data


# It parses data from xml and saves it to sqlite
class Parse_And_Save_Data(Data):
    def __init__(self, data):
        Data.__init__(self)
        self.data = data
        self.__parse_data()

    def __parse_data(self):
        """
        It takes the XML data from the API, parses it, and saves it to a database
        """
        for x in self.data:
            data = dict()  # create array to store data
            # enter data into the array
            data['id_job'] = x.attrib.get('id')
            data['link'] = self.__parse_cdata(x.find('link'))
            data['name'] = self.__parse_cdata(x.find('name'))
            data['region'] = self.__parse_cdata(x.find('region'))
            data['description'] = self.__parse_cdata(x.find('description'))
            data['pubdate'] = self.__parse_cdata(x.find('pubdate'))
            data['salary'] = self.__parse_cdata(x.find('salary'))
            data['company'] = self.__parse_cdata(x.find('company'))
            data['expire'] = self.__parse_cdata(x.find('expire'))
            data['jobtype'] = self.__parse_cdata(x.find('jobtype'))
            data['phone'] = self.__parse_cdata(x.find('phone'))
            self.parse_data = data # set the parse_data variable
            self.__save_data() # save the data to the database
        self.conn.commit()  # commit changes to database
        self.conn.close()  # close connection to database

    def __parse_cdata(self, data):
        """
        It takes a cdata tag and returns the text inside the tag

        :param data: the data to be parsed
        :return: The text inside the cdata tag.
        """
        try:
            data = data.text  # get the text inside the cdata
        except AttributeError:
            data = ''
        data = data.replace('![CDATA[', '')  # remove the cdata tag
        data = data.replace(']]', '')  # remove the cdata tag
        return data

    def __save_data(self):
        """
        It takes the keys from the dictionary, creates a string of comma separated keys, then takes the
        values from the dictionary, creates a string of comma separated question marks, then creates a
        string of the SQL query, then takes the values from the dictionary, converts the boolean values
        to integers, then executes the SQL query
        """
        columns = ', '.join(self.parse_data.keys())  # get all keys from data
        placeholders = ', '.join('?' * len(self.parse_data)) # get all placeholders from data
        sql = 'INSERT INTO data ({}) VALUES ({})'.format(
            columns, placeholders)  # create sql query
        values = [int(x) if isinstance(x, bool)
                  else x for x in self.parse_data.values()] # get all values from data
        self.cur.execute(sql, values)  # execute the query
