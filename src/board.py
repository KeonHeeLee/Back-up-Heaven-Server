import util

class board:
    '''
        "title": title,
        "storename" : storename,
        "start_time": start_time,
        "end_time": end_time,
        "urgency" : urgency,
    '''
    def get_home(self, args):
        local_name, job_name = self.parse_args_in_home(args)
        response = self.select_home_with_unfilter(local_name, job_name)

        return response


    def select_home_with_unfilter(self, local_name, job_name):
        conn = util.open_db()

        with conn.cursor() as cursor:
            simple_board_list = {}
            query = "select no, title, storename, start_time, end_time, urgency from board "
            filter = self.adjust_filter(cursor=cursor, local_name=local_name, job_name=job_name)

            if filter != None:
                query = query + filter

            query = query + ";"
            print(query)
            cursor.execute(query)
            rows = cursor.fetchall()

            simple_board_list = self.set_json(rows, simple_board_list)

        util.close_db(conn=conn)
        return simple_board_list


    def parse_args_in_home(self, args):
        local_name = None
        job_name = None

        if args["local"] != None:
            local_name = args["local"]
        if args["job"] != None:
            job_name = args["job"]

        return local_name, job_name

    def set_json(self, rows, simple_board_list):
        for row in rows:
            board_row = str(row[0])
            simple_board_list.update(
                {
                    board_row: {
                        "title": row[1],
                        "storename": row[2],
                        "start_time": row[3],
                        "end_time": row[4],
                        "urgency": row[5]
                    }
                })
        return simple_board_list

    def adjust_filter(self, cursor, local_name, job_name):
        adder = None
        if local_name == None and job_name == None:
            return adder

        adder = "where "

        if local_name != None:
            local_id = None
            query = "select local_id from local where local_name=%s;"
            cursor.execute(query, local_name)
            rows = cursor.fetchall()

            for row in rows:
                local_id = row[0]

            query = "select local_id from local where local_upper=%d;" %(local_id)
            cursor.execute(query)
            lower_rows = cursor.fetchall()

            if lower_rows == None:
                adder = adder + "local = " + str(local_id)
            else:
                for lower_row in lower_rows:
                    adder = adder + "local = " + str(lower_row[0]) + " or "
                adder = adder[:-4]

        if job_name != None:
            if local_name != None:
                adder += " and "
            job = None
            query = "select id from data_code where name=%s;"
            cursor.execute(query, job_name)
            rows = cursor.fetchall()

            for row in rows:
                job = row[0]

            adder = adder + "job =" + str(job)

        return adder

    def get_board_info(self, args):
        response = {}
        board_no = int(args["no"])
        conn = util.open_db()

        with conn.cursor() as cursor:
            query = "select * from board where no=%d" %(board_no)
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                job = None
                job_query = "select name from data_code where id=%d" %(row[7])
                cursor.execute(job_query)
                x = cursor.fetchall()
                for i in x :
                    job = i[0]

                local = None
                local_query = "select local_name from local where local_id=%d" %(row[10])
                cursor.execute(local_query)
                x = cursor.fetchall()
                for i in x :
                    local = i[0]

                response.update({
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
                })

        util.close_db(conn=conn)
        return response

    def regist_board(self, request):
        conn = util.open_db()
        job = None
        local = None

        title = request["title"]
        storename = request["storename"]
        start_time = request["start_time"]
        end_time = request["end_time"]
        urgency = int(request["urgency"])
        job_condition = request["job_condition"]
        job_name = request["job"]
        favorable_condition = request["favorable_condition"]
        detail = request["detail"]
        local_name = request["local"]
        local_sub = request["local_sub"]
        id = request["id"]

        with conn.cursor() as cursor:
            job_query = "select id from data_code where name=%s" %(job_name)
            cursor.execute(job_query)
            x = cursor.fetchall()
            for i in x:
                job = i[0]

            local_query = "select local_id from local where local_name=%s" % (local_name)
            cursor.execute(local_query)
            x = cursor.fetchall()
            for i in x:
                local = i[0]

            query = "insert into board values(null, %s, %s, %s, %s, %d, %s, %d, %s, %s, %d, %s, %s" %(
                title, storename, start_time, end_time, urgency, job_condition, job,
                favorable_condition, detail, local, local_sub, id)
            cursor.execute(query)
            conn.commit()

        util.close_db(conn=conn)