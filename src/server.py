#-*- coding utf-8-*-

from flask import Flask, jsonify, request
from handler import handler
import util, exception

app = Flask(__name__)

handler = handler()

@app.route(rule="/home", methods=["GET"])
def get_home():
    '''
    Print board list on main page.
    :return: {
    "1" : {
            "title": title,
            "storename" : storename,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "urgency" : urgency,
            "image": image_path
        },
    "2" : {

        },
    "3" : {}
    }
    '''
    local_name = None
    job_name = None

    local_name = request.args.get("local", local_name)
    job_name = request.args.get("job", job_name)

    args = {
        "local": local_name,
        "job": job_name }

    try:
        response = handler.get_request(type=util.HOME, request_data=None, args=args)
        return jsonify(response), 200
    except:
        return jsonify(exception.SEND_ERROR), 500

@app.route(rule="/board", methods=["GET"])
def get_board_info():
    '''
    If you click a component of ListView , this handler will be invoked.
    Print detail informations of a board.
    :param board_no: filter on database by board_no
    :return: {
        "no": row[0],
        "title": row[1],
        "storename": row[2],
        "start_time": row[3],
        "end_time": row[4],
        "urgency": row[5],
        "job_condition": row[6],
        "job": job,
        "favorable_condition": row[8],
        "detail": row[9],
        "local": local,
        "local_sub": row[11],
        "id": row[12]
    }
    '''
    board_no = None
    board_no = request.args.get("no", board_no)
    args = {"no": board_no}

    if board_no == None:
        return jsonify(exception.NO_BOARD_INFO), 404

    try:
        response = handler.get_request(type=util.BOARD_INFO, request_data=None, args=args)
        return jsonify(response), 200
    except:
        return jsonify(exception.SEND_ERROR), 500

@app.route(rule="/board_regist", methods=["POST"])
def regitst_board():
    '''
    If you regist a board in this server,
    server will send status_code to you.
    :return: status_code
    '''
    req = request.get_json()

    if req == None:
        return jsonify(exception.BAD_REQUEST), 400

    try:
        try:
            handler.get_request(type=util.REGIST_BOARD, request_data=req, args=None)
        except:
            return exception.FAIL_REGIST_BOARD, 500

        return "HTTP/1.1 200 OK", 200
    except:
        return jsonify(exception.SEND_ERROR), 500

#@app.route(rule="/board_down?no=<board_no>", methods=["DELETE"])
#def unregist_board():
#    return "HTTP/1.1 200 OK", 200

@app.route(rule="/login", methods=["POST"])
def login():
    '''

    :return:
    '''
    req = request.get_json()

    if req == None:
        return jsonify(exception.BAD_REQUEST), 400

    try:
        response = handler.get_request(util.LOGIN, request_data=req, args=None)
        return jsonify(response), 200
    except:
        return jsonify(exception.SEND_ERROR), 500

@app.route(rule="/logout", methods=["POST"])
def logout():
    '''

    :return:
    '''
    req = request.get_json()

    if req == None:
        return jsonify(exception.BAD_REQUEST), 400
    try:
        response = handler.get_request(util.LOGOUT, request_data=req, args=None)
        return jsonify(response), 200
    except:
        return jsonify(exception.SEND_ERROR)

@app.route(rule="/signup", methods=["POST"])
def sign_up():
    '''
    If you request to sign up, server will send status code to you.
    :return: status code
    '''
    req = request.get_json()
    response = handler.get_request(util.SIGNUP, request_data=req, args=None)

    if response != None:
        try:
            return jsonify(response), 200
        except:
            return jsonify(exception.SEND_ERROR), 500

    else:
        return jsonify(response), 406

@app.route(rule="/support", methods=["POST"])
def support():
    '''

    :return:
    '''
    req = request.get_json()
    try:
        response = handler.get_request(util.SURPPORT, request_data=req, args=None)
        return jsonify(response), 200
    except:
        return jsonify(exception.SEND_ERROR), 500


@app.route(rule="/supporters", methods=["GET"])
def get_supports():
    '''

    :return:
    '''
    no = None
    id = None

    no = request.args.get("no", no)
    id = request.args.get("od", id)

    args = {
        "no": no,
        "id": id }
    try:
        response = handler.get_request(util.GET_SUPPORTERS, request_data=None, args=args)
        return jsonify(response), 200
    except:
        return jsonify(exception.SEND_ERROR)

@app.route(rule="/locallist", methods=["GET"])
def get_local_list():
    '''
    If you click or call local_list,
    you will be seen local_list in dialog.
    :return: {"local_list": local_list}
    '''
    local_name = None
    local_name = request.args.get("filter", local_name)

    args = {"filter": util.GET_LOCAL,
            "local_name": local_name}
    try:
        response = handler.get_request(type=util.LOCAL_LIST, request_data=None, args=args)
        return jsonify(response), 200
    except:
        return jsonify(exception.SEND_ERROR), 500

@app.route(rule="/joblist", methods=["GET"])
def get_job_list():
    '''
    If you click or call job_list,
    you will be seen job_list in dialog.
    :return: {"local_list": job_list}
    '''
    args = {"filter": util.GET_JOB}
    try:
        response = handler.get_request(type=util.JOB_LIST, request_data=None, args=args)
        return jsonify(response), 200
    except:
        return jsonify(exception.SEND_ERROR), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)