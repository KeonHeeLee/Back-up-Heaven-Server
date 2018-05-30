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
            query = "select no, storename from board where id=\'%s\';" %(id)
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                id_query = "select id from getAlba where no=%d;" %(row[0])
                cursor.execute(id_query)
                x = cursor.fetchall()

                for i in x:
                    info_query = "select gender, local, local_sub, phone from member where id=\'%s\';" %(i[0])
                    cursor.execute(info_query)
                    y = cursor.fetchall()

                    upper = util.get_local_name(cursor, util.get_upper_local(cursor, y[0][1]))
                    lower = util.get_local_name(cursor, y[0][1])
                    local = upper + " " + lower + " " + y[0][2]

                    list.append({
                        "no": row[0],
                        "storename": x[1],
                        "id": i[0],
                        "gender": util.get_gender_name(cursor, y[0][0]),
                        "local": local,
                        "phone": y[0][3]
                    })

        response = {"applyer":list}
        util.close_db(conn=conn)
        return response

    def applying(self, args):
        id = args["id"]
        list = []
        conn = util.open_db()

        with conn.cursor() as cursor:
            applying_alba = "select no from getAlba where id=\'%s\';" %(id)
            cursor.execute(applying_alba)
            rows = cursor.fetchall()

            for row in rows:
                #                 0      1              2             3         4         5
                query = "select no, storename, start_time, end_time, local, local_sub from board where row=%d;" %(row[0])
                cursor.execute(query)
                x = cursor.fetchall()

                upper = util.get_local_name(cursor, util.get_upper_local(cursor, x[0][4]))
                lower = util.get_local_name(cursor, x[0][4])
                local = upper + " " + lower + " " + x[0][5]

                list.append({
                    "no": x[0][0],
                    "storename": x[0][1],
                    "start_time": x[0][2],
                    "end_time": x[0][3],
                    "local": local
                })

        util.close_db(conn)
        response = {"applying": list}
        return response