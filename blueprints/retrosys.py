import os
import traceback

from flask import Blueprint, render_template, flash, request, session, redirect, url_for

from learn_flask import service

from learn_flask.exts import db, is_smiles

bp = Blueprint("retrosys", __name__, url_prefix="/index")


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route("/re", methods=('GET', 'POST'))
def re():
    if request.method == 'POST':
        m = request.form['title']
        if not m:
            flash('Smiles分子式不为空!')
        elif not is_smiles(m):
            flash('请输入正确的SMILES码')
        else:
            if request.form.get('option') == 'option1':
                option = 1
            else:
                option = 2
            userid = int(session['user_id'])
            try:
                # 查询是否已存在该用户与产物的历史记录
                sql = "SELECT route FROM route WHERE user_id = %s AND product = %s"
                cursor = db.cursor()
                cursor.execute(sql, (userid, m,))
                result = cursor.fetchone()
                if result:
                    img_path = str(result[0])
                    img_stream = return_img_stream(img_path)
                    return render_template('out.html', img_stream=img_stream, img_path=img_path)

            except Exception as e:
                traceback.print_exc()
                flash("查询出错: {}".format(str(e)))
            finally:
                cursor.close()


            try:
                with db.cursor() as cursor:
                    # 插入
                    sql = "INSERT INTO route(user_id, product) VALUES (%s, %s)"
                    params = (userid, m,)
                    # 执行 SQL 语句
                    cursor.execute(sql, params)
                    db.commit()
            except:
                traceback.print_exc()
                db.rollback()
            finally:
                # 关闭数据库连接
                cursor.close()
            img_path = service.resyn(m, userid, option)
            img_stream = return_img_stream(img_path)
            return render_template('out.html', img_stream=img_stream, img_path=img_path)
    return render_template('re.html')


def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream
