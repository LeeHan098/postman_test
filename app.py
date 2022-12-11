from flask import Flask, render_template, request

import logging

application = Flask(__name__)

logging.warning()
import pymysql
import json

app = Flask(__name__)


#  튜플에서 딕셔너리로 cursor= db.cursor(pymysql.cursors.DictCursor)

# db 연결
# 참고 - https://problem-solving.tistory.com/10
# 참고 - https://shanepark.tistory.com/64


# route
@app.route('/')
def root():
    return render_template('index.html', component_name='groups')


# get layout
@app.route('/groups-layout')
def groupsLayout():
    return render_template('index.html', component_name='groups')


@app.route('/users-layout')
def usersLayout():
    return render_template('index.html', component_name='users')


@app.route('/images-layout')
def imagesLayout():
    return render_template('index.html', component_name='images')


# user
@app.route('/user', methods=['POST'])
def insert_user():
    db = pymysql.connect(host='localhost', user='root', db='sparta_test', password='gks1004*', charset='utf8')
    # db에서 커서를 어디에 두겠다.
    curs = db.cursor()
    # request 라이브러리로 json포멧인 것을 딕셔너리 객체로 받겠다.
    user = request.json

    first_name = user['first_name']
    last_name = user['last_name']
    user_name = user['user_name']
    email = user['email']
    avatar = user['avatar']
    city_id = user['city_id']
    group_id = user['group_id']

    sql = """insert into user (first_name, last_name, user_name, email, avatar, city_id, group_id)
         values (%s,%s,%s,%s,%s,%s,%s)
        """
    # execute 실행하는 함수 curs를 sql 쿼리를 실행 data를 넣어서
    curs.execute(sql, (first_name, last_name, user_name, email, avatar, city_id, group_id))

    # commit함수는 DB에 적용하는 함수
    db.commit()
    # close함수는 DB와 연결 종료하는
    db.close()

    return 'sucesess', 200


@app.route('/user', methods=['GET'])
def get_users():
    print('get_users')
    db = pymysql.connect(host='localhost', user='root', db='sparta_test', password='gks1004*', charset='utf8')
    curs = db.cursor()

    sql = """
    SELECT *
    FROM user as u
    LEFT JOIN `group` as g
    ON u.group_id = g.id
    """
    curs.execute(sql)

    rows = curs.fetchall()
    print(rows)

    # dumps 함수 파이썬 객체를 JSON 문자열로 변화하는 함수
    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    db.close()

    return json_str, 200


# photo

# group
# @app.route('/group')
# def getGroup():


# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
