import SQL_Object
import SQL_InputObject

test = SQL_Object.SQL_Object(
    'Test', 
    SQL_InputObject.SQL_InputObject(
        add_file='file.add'
    )
)
# test.display()
test.writeToFile('out.sql')
