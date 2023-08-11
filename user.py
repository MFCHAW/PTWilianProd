import streamlit as st
import pyodbc
from init_connection import qconnection

if 'UserKey' not in st.session_state:
    st.session_state['UserKey'] = -1


def run_query(query, args):
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, args[0], args[1], args[2])
        return cursor.fetchall()

    except pyodbc.Error as e:
        print(f'Error executing stored procesure: {e}')
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def getUserKey(userName, password):
    result = ''
    conn = qconnection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"""Select UserKey 
                            from FPS_Users 
                            Where UserId = '{userName}' and Password = '{password}' """)
        
        array1 = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            array1.append(dict(zip(columns, row)))

        result = str(array1[0]['UserKey'])
        
    except pyodbc.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return result
    

def login(userName: str, password: str) -> bool:
    if (userName is None):
        return False
    args = [userName, password, 0]
    result = run_query('execute FPS_CheckUser ?, ?, ?', args)
    if len(result) > 0:
        st.session_state['UserKey'] = getUserKey(userName, password)
        return True
    else:
        return False
