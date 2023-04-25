import os

from flask import Blueprint, render_template, request, flash, session, redirect, url_for, send_file, jsonify, \
    make_response
import traceback
from exts import db
from flask_login import UserMixin, login_user

from learn_flask.blueprints.retrosys import return_img_stream

bp = Blueprint("history", __name__, url_prefix="/history")


@bp.route("/", methods=['GET', 'POST'])
def history():

    sql = "SELECT * FROM route WHERE user_id = %s"
    userid = int(session['user_id'])
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (userid,))
            results = cursor.fetchall()
    except Exception as e:
        traceback.print_exc()
        flash("查询出错: {}".format(str(e)))
        results = []

    return render_template('history.html', results=results)

@bp.route("/update", methods=['GET', 'POST'])
def update():
    sql = "SELECT * FROM route WHERE user_id = %s"
    userid = int(session['user_id'])
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (userid,))
            results = cursor.fetchall()
    except Exception as e:
        traceback.print_exc()
        flash("查询出错: {}".format(str(e)))
        results = []

    return jsonify({'success': True}, results=results)


@bp.route('/delete/<int:rid>', methods=['DELETE'])
def delete(rid):
    cursor = db.cursor()
    try:
        sql = "DELETE FROM route WHERE route_id = %s"
        cursor.execute(sql, (rid,))
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cursor.close()

@bp.route('/thumbnail/<filename>')
def thumbnail(filename):
    # 获取完整的文件路径
    file_path = os.path.join('D:/retrosynData/data/thumbnail', filename)

    # 发送图片
    return send_file(file_path, mimetype='image/png')

@bp.route('/detail/<int:rid>', methods=['GET', 'POST'])
def detail(rid):
    if request.method == 'GET':
        sql = "SELECT route FROM route WHERE route_id = %s"
        try:
            cursor = db.cursor()
            cursor.execute(sql, (rid,))
            results = cursor.fetchone()
            img_path = str(results[0])
        except Exception as e:
            traceback.print_exc()
            flash("查询出错: {}".format(str(e)))
        finally:
            cursor.close()
        img_stream = return_img_stream(img_path)
        return render_template('out.html', img_stream=img_stream, img_path=img_path)
    return redirect(url_for('history.history'))

@bp.route('/download', methods=['POST'])
def download():
    img_path = request.form.get('img_path')
    return send_file(img_path, as_attachment=True)