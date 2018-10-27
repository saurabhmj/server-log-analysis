import happybase

connection = happybase.Connection('ec2-34-207-217-187.compute-1.amazonaws.com')

def insert_row(table_name, row_key, column_info):
    #accessing a table
    try:
        print('Table:', table_name)
        print('Row Key:', row_key)
        print('Columns:', column_info)
        table = connection.table(table_name)
        table.put(row_key, column_info)
        print('Inserted Succesfully!!')
    except:
        print('Insert Failed..')
        raise Exception('Insert Failed')
