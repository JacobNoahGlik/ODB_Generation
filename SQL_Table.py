import LethalErr
import re

class SQL_Table: # foreignKeys [ (name, fromTable), (name, fromTable) ]
    def __init__(self, line):# name, attributes, primaryKey, foreignKeys):
        self.name = self.__name_extractor(line)
        _attributes = self.__attr_extractor(line)
        self.attributes = {}
        for attribute in _attributes:
            a_name, a_type = attribute
            if a_name in self.attributes.keys():
                LethalErr.throw_lethal_err(
                    f'ERR: duplicate attribute {a_name} already exists in table {self.name}.'
                )
                
            self.attributes[a_name] = a_type
        self.primaryKey = self.__pk_extractor(line)
        self.foreignKeys = self.__fk_extractor(line)
        

    def listify(self):
        out = []
        for attr in self.attributes.keys():
            out.append((attr, self.attributes[attr]))
        return out


    def __name_extractor(self, line):
        pattern = '(?is)create table [a-z_]+[ ]*[(]'
        match = re.search(pattern, line)
        if not match: return None
        group = match.group()
        pattern_cuttoff = '[ ]*[(]'
        match2 = re.search(pattern_cuttoff, group)
        return group[13:-1 * len(match2.group())]


    def __attr_extractor(self, line):
        pattern = '(?is)[a-z_]+[ ]+[a-z]+(([(][0-9]+[)])|)'
        matchgroup = re.finditer(pattern, line)
        attrs = []
        for match in matchgroup:
            sout = match.group()
            check = sout.lower()
            if 'create table' in check or 'primary key' in check or 'foreign key' in check or 'references ' in check:
                continue
            attrs.append(
                (sout[:sout.index(' ')], sout[sout.index(' ')+1:])
            )
        return attrs


    def __pk_extractor(self, line):
        pattern = '(?is)primary key[ ]+[(][a-z_, ]+[)]'
        matchgroup = re.finditer(pattern, line)
        for match in matchgroup:
            pk = match.group()
            pk = pk[pk.index('(') + 1 : pk.index(')')]
            pks_lst = []
            for p in pk.split(','):
                pks_lst.append(p.replace(' ', ''))
            return pks_lst
        else:
            LethalErr.throw_lethal_err(f'Primary Key not found for table {self.name}.')

        
    def __fk_extractor(self, line):
        pattern = '(?is)foreign key[ ]+[(][a-z_, ]+[)][ ]+References [a-z_]+[ ]+[(][a-z_, ]+[)]'
        matchgroup = re.finditer(pattern, line)
        fks_lst = []
        for match in matchgroup:
            fk_raw = match.group()
            fk_cut = fk_raw[fk_raw.lower().index('references ') + 11:]
            fks_lst.append(
                (
                    fk_raw[fk_raw.index('(') + 1 : fk_raw.index(')')],
                    fk_cut[: fk_cut.index(' ')],
                    fk_cut[fk_cut.index('(') + 1 : fk_cut.index(')')]
                )
            )
        return fks_lst


    def __keyify(self):
        strBuilder = '('
        for key in self.primaryKey:
            strBuilder += key + ','
        return strBuilder[:-1] + ')'

    
    def display(self, prefix='\t'):
        print(f'{prefix}TABLE "{self.name}" has {len(self.attributes.keys())} attributes')
        print(f'{prefix}\tPrimaryKey={self.__keyify()}')
        for attribute in self.attributes.keys():
            print(f'{prefix}\tattr={attribute}, type={self.attributes[attribute]}')
        if len(self.foreignKeys) == 0:
            print(f'{prefix}\tNo ForeignKeys')
        else:
            for (key, fromTable, _) in self.foreignKeys:
                print(f'{prefix}\tForeignKey={key} fromTable={fromTable}')


    def toCreateTableString(self, prefix='\t'):
        output = f'CREATE TABLE {self.name} (\n'
        for attr in self.attributes.keys():
            output += f'{prefix}{attr} {self.attributes[attr].upper()},\n'
        output += f'{prefix}PRIMARY KEY {self.__keyify()},\n'
        for (key, fromTable, nickname) in self.foreignKeys:
            output += f'{prefix}FOREIGN KEY {key} REFERENCES {fromTable} ({nickname}),\n'
        output = output[:-2] + '\n);\n'
        return output


    def toDropTableString(self):
        return f'DROP TABLE {self.name};\n'


    def toPrintableString(self):
        return f"SELECT '{self.name}' FROM dual;\nSELECT * FROM {self.name};\n"