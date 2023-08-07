import streamlit as st
import pyodbc


def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )


def run_query(query, args):
    try:
        conn = init_connection()

        cursor = conn.cursor()
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


def login(userName: str, password: str) -> bool:
    if (userName is None):
        return False
    args = [userName, password, 0]
    result = run_query('execute FPS_CheckUser ?, ?, ?', args)
    if len(result) > 0:
        return True
    else:
        return False
