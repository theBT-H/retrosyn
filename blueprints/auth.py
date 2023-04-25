
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
import traceback
from exts import db
from flask_login import UserMixin, login_user
bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form.get('register') == 'register':
            return render_template('register.html')
        elif request.form.get('login') == 'login':
            user = request.form.get('user')
            password = request.form.get('password')

            if not user or not password:
                flash("输入不能为空")
                return render_template('login.html')
            else:
                try:
                    sql = "SELECT * FROM user WHERE user='{}' AND password='{}'".format(user, password)
                    cursor = db.cursor()
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    if len(results) == 1:
                        userid = int(results[0][0])
                        session['user_id'] = userid
                        session['user_name'] = user
                        return render_template('index.html')  # 返回需要跳转的页面或需要显示的字符串
                    else:
                        flash("用户名或密码不正确")
                        return render_template('login.html')
                except Exception as e:
                    traceback.print_exc()
                    flash("查询出错: {}".format(str(e)))
                finally:
                    cursor.close()
        return render_template('login.html')



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:

        username = request.form.get('username')
        password = request.form.get('password1')
        password2 = request.form.get('password2')
        if not username or not password or not password2:
            flash("输入不能为空")
            return render_template('register.html')

        else:
            #判断用户名是否合规
            if len(username) > 10:
                flash("用户名过长，应小于10！")
                return render_template('register.html')

            # 判断两次输入密码是否一致，一致则跳转到登录界面，不一致则弹出警告，要求用户重新输入
            if password == password2:
                try:
                    # 查询是否已存在该用户名
                    sql = "SELECT user FROM user WHERE user = %s"
                    cursor = db.cursor()
                    cursor.execute(sql, (username,))
                    result = cursor.fetchone()
                    if result:
                        flash("该用户名已存在")
                        return render_template('register.html')
                except Exception as e:
                    traceback.print_exc()
                    flash("查询出错: {}".format(str(e)))
                finally:
                    cursor.close()
                # SQL 插入语句
                sql = "INSERT INTO user(user, password) VALUES (%s, %s)"
                params = (username, password)
                try:
                    cursor = db.cursor()
                    cursor.execute(sql, params)
                    db.commit()
                    return render_template('login.html')
                except:
                    traceback.print_exc()
                    db.rollback()
                    flash('注册失败')
                finally:
                    cursor.close()
                # 关闭数据库连接
                db.close()
                return render_template('register.html')
            else:
                flash("两次输入密码不一致，请重新输入！")
                return render_template('register.html')
@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash("退出成功")
    return redirect(url_for('auth.login'))
