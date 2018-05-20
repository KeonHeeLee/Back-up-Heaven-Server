import pymysql

HOME            = "HOME"
BOARD_INFO      = "BOARD_INFO"
LOGIN           = "LOGIN"
LOGOUT          = "LOGOUT"
SIGNUP          = "SIGHUP"
REGIST_BOARD    = "REGIST_BOARD"
DETAIL_BOARD    = "DETAIL_BOARD"
SURPPORT        = "SURPPORT"
LOCAL_LIST      = "LOCAL_LIST"
JOB_LIST        = "JOB_LIST"
ERROR           = "ERROR"

GET_LOCAL       = 100
GET_JOB         = 101

def open_db():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           charset='utf8')
    query = "use daetaheaven;"
    conn.cursor().execute(query)

    query = "set names utf8;"
    conn.cursor().execute(query)
    return conn

def close_db(conn):
    conn.close()

def get_gender_code(cursor, gender_name):
    gender_code = None
    gender_code_check = "select id from data_code where type=%s and name=%s;"
    cursor.execute(gender_code_check, ['성별', gender_name])
    x = cursor.fetchall()

    for i in x:
        gender_code = i[0]

    return gender_code

def get_local_id(cursor, local_name):
    local_id = None

    local_id_query = "select local_id from local where local_name=%s;"
    cursor.execute(local_id_query, local_name)
    x = cursor.fetchall()

    for i in x:
        local_id = i[0]

    return local_id


def get_job_id(cursor, job_name):
    job_id = None

    local_id_query = "select id from data_code where name=%s and type=%s;"
    cursor.execute(local_id_query, [job_name, '직종'])
    x = cursor.fetchall()

    for i in x:
        job_id = i[0]

    return job_id