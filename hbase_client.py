import happybase

connection = happybase.Connection('ec2-34-207-217-187.compute-1.amazonaws.com')

def insert_row(table_name, row_key, column_info):
    #accessing a table
    try:
        #print('Table:', table_name)
        #print('Row Key:', row_key)
        #print('Columns:', column_info)
        table = connection.table(table_name)
        table.put(row_key, column_info)
        #print('Inserted Succesfully!!')
    except Exception as e:
        print('Insert Failed..')
        print(e)
        raise Exception('Insert Failed')



def create_table(table_name, families):
    try:
        d_families = {families[i]: dict() for i in range(len(families))}
        connection.create_table(table_name, d_families)
        print("Created: ", table_name)
    except Exception as e:
        #print("Table creation failed: ")
        print(e)
        raise Exception("Table creation failed: ", table_name)

def delete_table(table_name):
    try:
        connection.disable_table(table_name)
        connection.delete_table(table_name)
        print("Deleted: ", table_name)
    except Exception as e:
        print(e)
        raise Exception("Table deletion failed: ", table_name)

def truncate_table(table_name, families):
    delete_table(table_name)
    create_table(table_name, families)

def test_delete_create(table_name='server_logs_test', families=['log_info','loca_info']):
    delete_table(table_name)
    create_table(table_name, families)

if __name__== "__main__":
    test_delete_create()
