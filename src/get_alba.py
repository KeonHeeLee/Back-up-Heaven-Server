import util, exception

class get_alba:
    def __init__(self):
        self.GET_ALBA_SUCCESS = {"message": "get_alba success!!"}

    def get_alba(self, request):
        id = request["id"]
        no = request["no"]

        if id == None or no == None:
            return exception.UNLOGINED_USER

        conn = util.open_db()
        with conn.cursor() as cursor:
            query = "insert into getAlba values(%s, %d)"
            cursor.execute(query, (id, no))
            conn.commit()

        util.close_db(conn=conn)
        return self.GET_ALBA_SUCCESS

    def supporter_list(self, args):
        supporter_list = {}
        id = args["id"]
        no = args["no"]

        conn = util.open_db()
        with conn.cursor() as cursor:
            board_list_query = "select no from board where id=%s;"
            cursor.execute(board_list_query, id)
            rows = cursor.fetchall()

            for row in rows:
                board_no = str(row[0])
                supporter_list.update({
                    board_no: self.get_supporter_info(cursor=cursor, no=row[0])
                })

        util.close_db(conn=conn)
        return supporter_list


    def get_supporter_info(self, cursor, no):
        get_id_query = "select id from getAlba where no=%d;" %(no)
        cursor.execute(get_id_query)
        rows = cursor.fetchall()
        supporter_list_in_board = {}

        for row in rows:
            query = "select birthday, gender from member where id=%s"
            cursor.execute(query, row[0])
            x = cursor.fetchall()
            gender_name = util.get_gender_name(cursor, x[0][1])
            supporter_list_in_board.update({
                row[0] : {
                    "birthday": x[0][0],
                    "gender": gender_name
                }
            })
            return supporter_list_in_board

    def get_support_storename(self, cursor, id):
        query = "select no"