import pymysql

HOME            = "HOME"
BOARD_INFO      = "BOARD_INFO"
LOGIN           = "LOGIN"
LOGOUT          = "LOGOUT"
SIGNUP          = "SIGHUP"
REGIST_BOARD    = "REGIST_BOARD"
DETAIL_BOARD    = "DETAIL_BOARD"
SURPPORT        = "SURPPORT"
GET_SUPPORTERS  = "GET_SUPPORTERS"
LOCAL_LIST      = "LOCAL_LIST"
JOB_LIST        = "JOB_LIST"
ERROR           = "ERROR"
APPLYING        = "APPLYING"
UPLOAD          = "UPLOAD"
RECRUITMENT     = "RECRUITMENT"

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
    gender_code_check = "select id from data_code where type=\'성별\' and name=\'%s\';" %(gender_name)
    cursor.execute(gender_code_check)
    x = cursor.fetchall()

    return x[0][0]

def get_gender_name(cursor, gender_code):
    gender_name = None
    gender_name_check = "select name from data_code where type=\'성별\' and id=%d;" %(gender_code)
    cursor.execute(gender_name_check)
    x = cursor.fetchall()

    return x[0][0]

def get_local_id(cursor, local_name):
    local_id = None

    local_id_query = "select local_id from local where local_name=%s;"
    cursor.execute(local_id_query, local_name)
    x = cursor.fetchall()

    return x[0][0]

def get_upper_local(cursor, local_id):
    local_id_query = "select local_upper from local where local_id=%d;" %(local_id)
    cursor.execute(local_id_query)
    x = cursor.fetchall()

    return x[0][0]

def get_local_name(cursor, local_id):
    local_id_query = "select local_name from local where local_id=%d;" %(local_id)
    cursor.execute(local_id_query)
    x = cursor.fetchall()

    return x[0][0]


def get_job_id(cursor, job_name):
    local_id_query = "select id from data_code where name=\'%s\' and type=\'직종\';" %(job_name)
    cursor.execute(local_id_query)
    x = cursor.fetchall()

    return x[0][0]

def get_num(cursor, title, id):
    query = "select no from board where title=\'%s\' and id=\'%s\';"%(title, id)
    cursor.execute(query)
    x = cursor.fetchall()

    return int(x[0][0])