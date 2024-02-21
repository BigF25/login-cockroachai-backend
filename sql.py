import sqlite3 as sqlite
import logging

name = "users.db"

def create_db():
    conn = sqlite.connect(name)
    cursor = conn.cursor()
    cursor.execute( '''
            CREATE TABLE IF NOT EXISTS users
            (userID  INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            GPT4_EN BOOLEAN NOT NULL,
            token TEXT)
            ''')
    conn.commit()
    conn.close()

def insert_user(username,passwd,en,token):
    conn = sqlite.connect(name)
    cursor = conn.cursor()
    user_data = (username,passwd,en,token)
    try:
        cursor.execute("INSERT INTO users (username, password, GPT4_EN , token) VALUES (?, ?, ?, ?)",
                       user_data)
        logging.info(f"User '{username}' created successfully.")
        conn.commit()
    except sqlite.IntegrityError:
        conn.close()
        update_users(username,passwd,en,token)
        logging.info(f"User '{username}' changed.")
    conn.close()
'''
token : normal
0     : passwd not true
2     : ban
3     : user not exit

'''
def authenticate_user(user,passwd)->str:
    conn = sqlite.connect(name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT password, GPT4_EN, token FROM users WHERE username=?", (user,))
    result = cursor.fetchone()
    conn.close()
    if result:
        stored_password, enable_status, token = result
        if enable_status:
            if passwd == stored_password:
                logging.info(token)
                return token
            else:
                logging.info('0')
                return '0'
        else:
            logging.info("2")
            return '2'
    else:
        logging.info('3')
        return '3'
    
"""password最短长度在html中设定

0     : ok
1     : error

"""
def change_passwd(user,old_passwd,new_passwd)->bool:
    conn = sqlite.connect(name)
    cursor = conn.cursor()
    # 验证旧密码是否匹配
    cursor.execute("SELECT password FROM users WHERE username=?", (user,))
    stored_password = cursor.fetchone()

    if stored_password and stored_password[0] == old_passwd:
        # 旧密码匹配，执行更新操作
        cursor.execute("UPDATE users SET password=? WHERE username=?",
                    (new_passwd, user))
        conn.commit()
        logging.info("修改成功")
        result_code = 0  
    else:
        logging.info("旧密码不匹配")
        result_code = 1  
    conn.commit()
    conn.close()
    return result_code

def update_users(user,passwd=None,en=None,token=None):
    conn = sqlite.connect(name)
    cursor = conn.cursor()

    # SET DATA STRING
    update_query = "UPDATE users SET "
    update_values = []
    if passwd is not None:
        update_query += "password=?, "
        update_values.append(passwd)
    if en is not None:
        update_query += "GPT4_EN=?, "
        update_values.append(en)
    if token is not None:
        update_query += "token=?, "
        update_values.append(token)
    update_query = update_query.rstrip(', ') + " WHERE username=?"
    update_values.append(user)

    cursor.execute(update_query, tuple(update_values))

    conn.commit()
    conn.close()

def get_user_info():
    conn = sqlite.connect(name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    conn.close()
    return data

def delete_user(userID):
    conn = sqlite.connect(name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE userID = ?", (userID,))
    conn.commit()
    cursor.close()
    conn.close()

if __name__=="__main__":
    # 配置日志
    logging.basicConfig(level=logging.DEBUG)
    create_db()
    insert_user('user','password',True,'user2')
    # update_users('user','passwd',token='user3')
    # change_passwd('user','passwd','passwd')
    # authenticate_user('user','passwd')
    data = get_user_info()
    for i in data:
        print(i)