from board import board
from datalist import datalist
from sign import sign
from get_alba import get_alba
from flask import jsonify
import util

class handler:
    def __init__(self):
        self.board = board()
        self.datalist = datalist()
        self.sign = sign()
        self.get_alba = get_alba()

    def get_request(self, type, request_data, args):
        response = None

        if   type == util.HOME:             response = self.board.get_home(args=args)
        elif type == util.BOARD_INFO:       response = self.board.get_board_info(args=args)
        elif type == util.LOGIN:            response = self.sign.login(request=request_data)
        elif type == util.LOGOUT:           response = self.sign.logout(request=request_data)
        elif type == util.SIGNUP:           response = self.sign.sign_up(request=request_data)
        elif type == util.REGIST_BOARD:     self.board.regist_board(request=request_data)
        elif type == util.SURPPORT:         response = self.get_alba.get_alba(request=request_data)
        elif type == util.APPLYING:         response = self.get_alba.applying(args=args)
        elif type == util.GET_SUPPORTERS:   response = self.get_alba.supporter_list(args=args)
        elif type == util.LOCAL_LIST:       response = self.datalist.get_datalist(args=args)
        elif type == util.JOB_LIST:         response = self.datalist.get_job_list()

        else:
            return jsonify(util.ERROR), 404

        return response