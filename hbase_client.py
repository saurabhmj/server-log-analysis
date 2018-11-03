import happybase

connection = happybase.Connection('ec2-34-207-217-187.compute-1.amazonaws.com')

"""
Function to insert a row into HBase.
Input Parameter: HBase table, row key, column info as a dict 
"""
def insert_row(table_name, row_key, column_info):

    try:
        table = connection.table(table_name)
        table.put(row_key, column_info)
    except Exception as e:
        print('Insert Failed..')
        print(e)
        raise Exception('Insert Failed')


"""
Function to insert a batch of rows into HBase.
Input Parameter: HBase table, {rowKey: {column info}}
"""
def insert_batch(table_name, data):
    try:
        table = connection.table(table_name)
        b = table.batch()
        for key, columns in data.items():
            b.put(key, columns)
        b.send()
    except Exception as e:
        print (e)
        print('Insert Failed..')


"""
Function to create a table into HBase.
Input Parameter: HBase table name, column family names 
"""
def create_table(table_name, families):
    try:
        d_families = {families[i]: dict() for i in range(len(families))}
        connection.create_table(table_name, d_families)
        print("Created: ", table_name)
    except Exception as e:
        print(e)
        raise Exception("Table creation failed: ", table_name)


"""
Function to delete a table from HBase.
Input Parameter: HBase table name
"""
def delete_table(table_name):
    try:
        connection.disable_table(table_name)
        connection.delete_table(table_name)
        print("Deleted: ", table_name)
    except Exception as e:
        print(e)
        raise Exception("Table deletion failed: ", table_name)


"""
Function to truncate a table. HBase does not have a builtin truncate functionality.
THis method will delete table and re-create it.
Input Parameter: HBase table name, column families of the table. 
"""
def truncate_table(table_name, families):
    delete_table(table_name)
    create_table(table_name, families)


"""
Function to test operations in the script
Input Parameter: HBase table name and column families 
"""
def test_delete_create(table_name='server_logs_new', families=['log_info','loca_info']):
    delete_table(table_name)
    create_table(table_name, families)

if __name__== "__main__":
    test_delete_create()
