import SQL_Table
import LethalErr
import re

class SQL_Object:
    def __init__(self, name, inputObject):
        self.name = name
        self.tablenames = {}
        self.tables = []
        if inputObject.getSQLF(): 
            self.droppedtablenames = self.__readin(inputObject.getSQLF())
            self.__checkTables()
        if inputObject.getADDF():
            self.__addin(inputObject.getADDF())


    def __checkTables(self):
        for tablename in self.droppedtablenames:
            if tablename not in self.tablenames():
                LethalErr.throw_lethal_err(f'{tablename} dropped but never created by {self.name}')

    
    def __addin(self, ADD_File):
        lines = self.__readfile(ADD_File)
        for line in lines:
            if self.__typeify(line) == 1:
                newTable = SQL_Table.SQL_Table(
                    self.__tableBuilder(line)
                )
                self.__addTable(newTable)
                

    def __addTable(self, table):
        self.tablenames[table.name] = len(self.tables)
        self.tables.append(table)
    

    def __tableBuilder(self, line):
        stringBuilder = 'CREATE TABLE '
        lines = line.split(',', 1)
        name = lines[0]
        first = name.index("'") + 1
        name = name[first : name.index("'", first)]
        stringBuilder += name + '('
        if 'Attributes' not in lines[1][:12]:
            LethalErr.throw_lethal_err(f'Could not find attribute creation "{lines[1]}"')
        attributes = lines[1]
        attributes = attributes[attributes.index('[') + 1: attributes.index(']')].split(',')
        package = []
        for attr in attributes:
            if attr in ['', ' ']:
                continue
            attr_name, flag, tablefrom, nickname = self.__attribute_select(attr)
            stringBuilder += attr_name
            package.append((attr_name, flag, tablefrom, nickname))
        pks = []
        fks = ''
        for (attr_name, flag, tablefrom, nickname) in package:
            attr_name = attr_name.split(' ')[0]
            if flag:
                pks.append(attr_name)
            if tablefrom:
                fks += f',FOREIGN KEY ({attr_name}) REFERENCES {tablefrom} ({nickname})'
        stringBuilder += f'PRIMARY KEY {self.__keyify(pks)}{fks})'
        print(f'{stringBuilder}')
        return stringBuilder

        
    def __attribute_select(self, attribute):
        attribute = attribute.strip()
        counter = 0
        primarykey = False
        tablename = False
        nickname = None
        items = attribute.split(' ')
        for item in items:
            if item == '-p':
                primarykey = True
            elif '.' in item:
                tablename, t_attr = item.split('.')
                if tablename not in self.tablenames:
                    LethalErr.throw_lethal_err(f'{tablename} from context {attribute} could not be found in tablenames {self.tablenames}.')
                tablename
                name = t_attr # set default name
                nickname = t_attr
                type = self.getTableByName(tablename).attributes[t_attr]
            elif counter == 0:
                name = item
                counter += 1
            elif counter == 1:
                type = item
                counter += 1
            else:
                LethalErr.throw_lethal_err(f'Unknown situation: {counter=}, {name=}, {type=}, {attribute=}')
        return f'{name} {type},', primarykey, tablename, nickname


            
            
    def getTableByName(self, name):
        return self.tables[self.tablenames[name]]

    def __typeify(self, line):
        if 'NewTable' in line[:15]:
            return 1
        
    
        
    def __readin(self, SQL_File):
        content = self.__readfile(SQL_File)
        self.tables = []
        self.tablenames = {}
        tablenames = []
        for line in content:
            if 'drop table' in line.lower():
                tablenames.apppend()#__nameExtractDT(line))
                print('did not write')
                exit()
            if 'create table' in line.lower():
                newTable = SQL_Table.SQL_Table(line)
                self.__addTable(newTable)
        return tablenames
        
    
    def __readfile(self, filename):
        with open(filename, 'r') as sql_file:
            sqlContent = sql_file.read()
        return sqlContent.replace('\n', '').split(';')


    def __nameExtractDT(line):
        pattern = 'drop table [a-z_]+'
        match = re.search(pattern, line)
        if not match: return None
        group = match.group()
        return group[11:].capitalize()


    def display(self):
        print(f'OBJECT {self.name} has {len(self.tables)} table(s)')
        for table in self.tables:
            table.display(prefix=f'  ')


    def writeToFile(self, filename, dropTable=True, displayTables=True):
        with open(filename, 'w') as fout:
            for table in reversed(self.tables):
                fout.write(table.toDropTableString())
            fout.write('\n')
            for table in self.tables:
                fout.write(table.toCreateTableString())
            fout.write('\n')
            for table in self.tables:
                fout.write(table.toPrintableString())

    def __keyify(self, keys):
        strBuilder = '('
        for key in keys:
            strBuilder += key + ','
        return strBuilder[:-1] + ')'