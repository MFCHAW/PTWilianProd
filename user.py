import streamlit as st
import asyncio
import aiohttp
import json
# import pymssql
from init_connection import qconnection

# -- Variables and Session States Initialization --
if 'user_LoginResult' not in st.session_state:
    st.session_state['user_LoginResult'] = False
    
if 'UserKey' not in st.session_state:
    st.session_state['UserKey'] = -1


url_Login = st.secrets['url_Login']
url_UserKey = st.secrets['url_UserKey']


    
async def tryLogin(userName, password):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url_Login, data=json.dumps({
            "UserName": userName,
            "Password": password
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            
            # if response.status == 200 and data['Status'] != 'Failed' and len(result) == 0:
            if data['userId'] == {}:
                st.session_state['user_LoginResult'] = False
            else:
                st.session_state['user_LoginResult'] = True
            
                
                
async def getUserKey(userName, password):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url_UserKey, data=json.dumps({
            "UserName": userName,
            "Password": password
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            
            st.session_state['UserKey'] = data['UserKey']['Table1'][0]['UserKey']
            
            


# def run_query(query, args):
#     conn = qconnection()
#     cursor = conn.cursor(as_dict=True)

#     try:
#         cursor.callproc(query, args)
#         return cursor.fetchall()

#     except pymssql.Error as e:
#         print(f'Error executing stored procesure: {e}')
#         return False
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()


# def getUserKey(userName, password):
#     result = -1
#     conn = qconnection()
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute(f"""Select UserKey 
#                             from FPS_Users 
#                             Where UserId = '{userName}' and Password = '{password}' """)
        
#         array1 = []
#         columns = [column[0] for column in cursor.description]
#         for row in cursor.fetchall():
#             array1.append(dict(zip(columns, row)))

#         result = array1[0]['UserKey']
        
#     except pymssql.Error as e:
#         st.write(f'Error executing query: {e}')
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
    
#     return result
    

def login(userName: str, password: str) -> bool:
    if (userName is None):
        return False
    # args = (userName, password, 0)
    # result = run_query('FPS_CheckUser', args)
    
    # if result == False:
    #     return False
    # else:
    #     st.session_state['UserKey'] = getUserKey(userName, password)
    #     return True
    
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tryLogin(userName, password)) 
    
    if st.session_state['user_LoginResult'] == False:
        return False
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(getUserKey(userName, password)) 
        return True
    

    
