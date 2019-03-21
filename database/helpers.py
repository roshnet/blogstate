# All helper functions that involve database.


def safe_connect(MYSQL_HANDLE):
    '''
    Attempts to establish a connection with the database
    contained in the MYSQL_HANDLE variable.
    Returns the cursor on success.
    Returns 0 on any kind of failure. 
    '''
    try:
        cur =  MYSQL_HANDLE.connect().cursor()
        return cur
    except:
        return 0


# def safe_fetch(cursor, table, column_list, type='one'):
#     '''
#     :param table:           Specifies table name to connect to.
#     :param column_list      List of arguments for SELECT statement.
#     :param type:            Specifies which one out of `fetchone` or `fetchall`
#                             modes to use.
#     This function has in built error handling in case it cannot connect to the DB
#     for some reason.

#     Returns 0 to indicate failure.
#     '''

#     if '*' in column_list:
#         q = "SELECT * FROM {table} WHERE "
#     columns = '`, `'.join(column_list)
#     q = "SELECT `{cols}` FROM {table}".format(cols=columns,
#                                               table=table)
#     if type == 'all':
#         pass

