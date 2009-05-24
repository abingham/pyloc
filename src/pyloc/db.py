import sqlite3

types_table_sql = '''
CREATE TABLE IF NOT EXISTS types
(id INTEGER PRIMARY KEY NOT NULL,
 type TEXT NOT NULL)
'''

files_table_sql = '''
CREATE TABLE IF NOT EXISTS files
(id INTEGER PRIMARY KEY NOT NULL,
 name TEXT NOT NULL,
 root TEXT NOT NULL,
 type_id INTEGER NOT NULL)
'''

categories_table_sql = '''
CREATE TABLE IF NOT EXISTS categories
(id INTEGER PRIMARY KEY NOT NULL,
 category TEXT NOT NULL)
'''

counts_table_sql = '''
CREATE TABLE IF NOT EXISTS counts
(id INTEGER PRIMARY KEY NOT NULL,
 cat_id INTEGER NOT NULL,
 file_id INTEGER NOT NULL,
 count INTEGER NOT NULL)
'''

class Results(object):
    def __init__(self, name=':memory:'):
        self.conn = sqlite3.Connection(name)
        cur = self.conn.cursor()
        cur.execute(types_table_sql)
        cur.execute(files_table_sql)
        cur.execute(categories_table_sql)
        cur.execute(counts_table_sql)

        self.__types = {}
        self.__categories = {}

    def close(self, commit=True):
        if commit:
            self.conn.commit()
        self.conn.close()

    def add_result(self, filename, root, type, counts):
        cur = self.conn.cursor()

        try:
            typeid = self.__types[type]
        except KeyError:
            cur.execute('INSERT INTO types VALUES(?,?)',
                        (None, type))
            typeid = cur.lastrowid
            self.__types[type] = typeid
                
        cur.execute('INSERT INTO files VALUES(?,?,?,?)',
                    (None, filename, root, typeid))
        fileid = cur.lastrowid
        
        for cat,count in counts.items():
            try:
                catid = self.__categories[cat]
            except KeyError:
                cur.execute('INSERT INTO categories VALUES(?,?)',
                            (None, cat))
                catid = cur.lastrowid
                self.__categories[cat] = catid
            
            cur.execute('INSERT INTO counts VALUES(?,?,?,?)',
                        (None, catid, fileid, count))

    def categories(self):
        '''get a list of all categories present in the results

        Note that not all files will have all categories
        '''
        cur = self.conn.cursor()
        cur.execute('SELECT category FROM categories')
        return [row[0] for row in cur]

    def types(self):
        '''get a list of all file-types present in the results'''

        cur = self.conn.cursor()
        cur.execute('SELECT type FROM types')
        return [row[0] for row in cur]

    def counts_by_type(self, filetype):
        '''get counts summed over a particular file type
        
        :param filetype: the filetype to get counts for
        :return: a dictionary { category -> sum }
        '''
        cur = self.conn.cursor()
        cur.execute('''SELECT categories.category, 
                              counts.count
                       FROM counts, 
                            types, 
                            files, 
                            categories 
                       WHERE types.type = ?
                             AND files.type_id = types.id
                             AND counts.file_id = files.id
                             AND categories.id = counts.cat_id''',
                    (filetype,))
        counts = [(row[0], row[1]) for row in cur]
        rslt = {}
        for cat,count in counts:
            try:
                rslt[cat] += count
            except KeyError:
                rslt[cat] = count
        return rslt
        

    def sum_categories(self, filetype):
        pass
