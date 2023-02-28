class SQL_InputObject:
    def __init__(self, sql_file=None, add_file=None, insert_file=None):
        self.sql_file = sql_file
        self.add_file = add_file
        self.insert_file = insert_file


    def getSQLF(self): return self.sql_file
    def getADDF(self): return self.add_file
    def getINSF(self): return self.insert_file