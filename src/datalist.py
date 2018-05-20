import util

class datalist:
    def get_datalist(self, args):
        response = None
        filter = args["filter"]

        if filter == util.GET_LOCAL:
            local_name = args["local_name"]
            response = self.get_local_list(local_name=local_name)
        else: #filter = util.GET_JOB:
            response = self.get_job_list()

        return response

    def get_local_list(self, local_name):
        response = {}
        local_list = []
        conn = util.open_db()

        with conn.cursor() as cursor:
            t_local_id = util.get_local_id(cursor=cursor, local_name=local_name)

            query = "select local_name from local where local_upper=%d;" %(t_local_id)
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                local_list.append(row[0])

        util.close_db(conn=conn)
        response.update({"local_list": local_list})
        return response

    def get_job_list(self):
        response = {}
        job_list = []

        conn = util.open_db()

        with conn.cursor() as cursor:
            query = "select name from data_code where type=%s;"
            cursor.execute(query, '직종')
            rows = cursor.fetchall()

            for row in rows:
                job_list.append(row[0])

        util.close_db(conn=conn)
        response.update({"job_list": job_list})
        return response