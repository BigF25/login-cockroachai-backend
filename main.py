from flask import Flask, render_template, request, redirect, url_for,session,Blueprint
import sql

app = Flask(__name__,static_folder='style_static')

app.secret_key = 'xyzsdfg'

admin_users ={
    'admin':'password',
    'admin2':'password'
}

@app.route('/login/')
def index():
    return render_template('login.html')


@app.route('/login/auth_login', methods=['POST','GET'])
def login():
    if request.method == 'POST':  # 确保是 POST 请求
        username = request.form['username']
        password = request.form['password']

        if username in admin_users:
            if admin_users[username] == password:
                session['loggedin'] = True
                return redirect(url_for('user_manager'))
            else:
                return render_template('login.html',error='error password')
        else:
            result = sql.authenticate_user(username,password)
            
            if result == '0':
                return render_template('login.html', error='Invalid password')
            elif result == '3':
                return render_template('login.html', error='Invalid user')
            elif result == '2':
                return render_template('login.html', error='You have no access to GPT4, Please connect to the Administrators')
            else:
                
                return redirect('https://cockroachai.syberf.top/logintoken?access_token=%s'% result)
                # 本机部署使用
                # return redirect('/logintoken?access_token=%s'% result)
    return redirect(url_for('index'))

@app.route('/login/renew',methods=['POST','GET'])
def renew():
    if request.method == 'POST':
        change_username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        
        result = sql.change_passwd(change_username,old_password,new_password)
        if result == 0:
            return redirect(url_for('index'))
        else:
            return render_template('renew.html',error='error user or password')
    return render_template('renew.html')

@app.route('/login/user_manager',methods=['POST','GET'])
def user_manager():
    if 'loggedin' in session:
        return render_template('user_manager.html',users = sql.get_user_info())
    
    return redirect(url_for('index'))

@app.route('/login/user_manager/add_user',methods=['POST','GET'])
def add_user():
    if 'loggedin' in session:
        if request.method == 'POST':
            user = request.form['username']
            PWD = request.form['password']
            GPT4_EN = bool(request.form.get('enable'))
            Token = request.form['token']
            sql.insert_user(user,PWD,GPT4_EN,Token)
            return redirect(url_for('user_manager'))
    return redirect(url_for('index')) 

@app.route('/login/user_manager/delete/<int:user_id>',methods=['POST','GET'])
def delete_user(user_id):
    if 'loggedin' in session:
        sql.delete_user(user_id)
        return redirect(url_for('user_manager'))
    return redirect(url_for('index')) 


if __name__ == '__main__':
    sql.create_db()  
    app.run(port=8505)
