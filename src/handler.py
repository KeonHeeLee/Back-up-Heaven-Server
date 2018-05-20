from board import board
from datalist import datalist
from sign import sign
from flask import jsonify
import util

class handler:
    def __init__(self):
        self.board = board()
        self.datalist = datalist()
        self.sign = sign()

    def get_request(self, type, request_data, args):
        response = None

        if type == util.HOME:
            response = self.board.get_home(args=args)

        elif type == util.BOARD_INFO:
            response = self.board.get_board_info(args=args)

        elif type == util.LOGIN:
            print(util.LOGIN)

        elif type == util.LOGOUT:
            print(util.LOGOUT)

        elif type == util.SIGNUP:
            self.sign.sign_up(request_data)

        elif type == util.REGIST_BOARD:
            self.board.regist_board(request=request_data)

        elif type == util.SURPPORT:
            print(util.SURPPORT)

        elif type == util.LOCAL_LIST:
            response = self.datalist.get_datalist(args=args)

        elif type == util.JOB_LIST:
           response = self.datalist.get_job_list()

        else:
            return jsonify(util.ERROR), 404

        return response