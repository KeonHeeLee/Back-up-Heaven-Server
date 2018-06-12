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
            query = "insert into getAlba values(\'%s\', %d);" %(id,no)
            cursor.execute(query)
            conn.commit()

        util.close_db(conn=conn)
        return self.GET_ALBA_SUCCESS

    def supporter_list(self, args):
        list = []
        id = args["id"]

        conn = util.open_db()
        with conn.cursor() as cursor:
            get_board_query = "select no, storename from board where id=\'%s\';" %(id)
            cursor.execute(get_board_query)
            rows = cursor.fetchall()

            for row in rows:
                #                                            0                 1                  2                 3
                applyer_query = "select distinct member.id, member.gender, member.local_main, member.phone from member left join getAlba on member.id = getAlba.id where getAlba.no = %d" %(row[0])
                cursor.execute(applyer_query)
                x = cursor.fetchall()

                for y in x:
                    upper = util.get_local_name(cursor, util.get_upper_local(cursor, y[2]))
                    lower = util.get_local_name(cursor, y[2])
                    local = upper + " " + lower

                    list.append({
                        "no": row[0],
                        "storename" : row[1],
                        "id": y[0],
                        "gender": util.get_gender_name(cursor, y[1]),
                        "local":  local,
                        "phone": y[3]
                    })

        response = {"applyer":list}
        util.close_db(conn=conn)
        return response

    def applying(self, args):
        id = args["id"]
        list = []
        conn = util.open_db()

        with conn.cursor() as cursor:
            #                                           0                1                2               3               4                5
            applying_alba = "select distinct board.no,board.storename,board.start_time,board.end_time,board.local,board.local_sub from board left join getAlba on board.no = getAlba.no where getAlba.id =\'%s\'" %(id)
            cursor.execute(applying_alba)
            rows = cursor.fetchall()

            for row in rows:
                upper = util.get_local_name(cursor, util.get_upper_local(cursor, row[4]))
                lower = util.get_local_name(cursor, row[4])
                local = upper + " " + lower + " " + row[5]

                list.append({
                    "no": row[0],
                    "storename": row[1],
                    "start_time": row[2],
                    "end_time": row[3],
                    "local": local
                })

        util.close_db(conn)
        response = {"applying": list}
        print(response)
        return response

    def recruitment(self, args):
        no = int(args)
        conn = util.open_db()

        with conn.cursor() as cursor:
            recruit_query_in_board = "delete from board where no=%d;" %(no)
            cursor.execute(recruit_query_in_board)
            conn.commit()

            recruit_query_in_getAlba = "delete from board where no=%d;" %(no)
            cursor.execute(recruit_query_in_getAlba)
            conn.commit()
