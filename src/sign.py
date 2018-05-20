import util
import exception

class sign:
    def sign_up(self, request):
        id = request["id"]
        pwd = request["pwd"]
        name = request["name"]
        gender_name = request["gender"]
        birthday = request["birthday"]
        phone = request["phone"]
        local_main = request["local_main"]
        local_sub = request["local_sub"]
        job_name = request["job"]

        conn = util.open_db()

        with conn.cursor() as cursor:
            if self.check_user_duplication(cursor=cursor, name=name, birthday=birthday, phone=phone):
                util.close_db(conn=conn)
                return exception.REGISTED_USER

            if self.check_id_duplication(cursor, id):
                util.close_db(conn=conn)
                return exception.ID_DUPLCATION

            gender = util.get_gender_code(cursor=cursor, gender_name=gender_name)
            local = util.get_local_id(cursor=cursor, local_name=local_main)
            job = util.get_job_id(cursor=cursor, job_name=job_name)

            query = "insert into member values(%s, %s, %s, %d, %s, %s, %d, %s, %d)"
            cursor.execute(query, [id, pwd, name, gender, birthday, phone, local, local_sub, job])
            conn.commit()

        util.close_db(conn=conn)

    def check_user_duplication(self, cursor, name, birthday, phone):
        check_user = "select * from member where name=%s and birthday=%s and phone=%s;"
        cursor.execute(check_user, [name, birthday, phone])
        rows = cursor.fetchall()

        if rows == None:
            return False
        else:
            return True

    def check_id_duplication(self, cursor, id):
        check_id = "select * from member where id=%s;"
        cursor.execute(check_id, id)
        rows = cursor.fetchall()

        if rows == None:
            return False
        else:
            return True