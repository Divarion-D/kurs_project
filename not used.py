class Sort_Data:
    def __init__(self, order_by, order_type):
        self.conn = sqlite3.connect('data.db')  # connect to the database
        self.cur = self.conn.cursor()  # create a cursor
        self.cur.execute('''SELECT * FROM data''')
        self.data = self.cur.fetchall()
        self.order_by = order_by
        self.order_type = order_type
        self.__sort_data__()
    
    def __sort_data__(self):
        # get all column names from database
        self.cur.execute('''SELECT * FROM data''')
        self.columns = [column[0] for column in self.cur.description]
        # get index of column name
        self.index = self.columns.index(self.order_by)
        # sort data by column name
        self.data = sorted(self.data, key=lambda x: x[self.index], reverse=self.order_type)
        return self.data

    #save data to txt file
    def save_data(self):
        with open('data.txt', 'w') as f:
            for i in self.data:
                f.write(str(i))
                f.write('\n')