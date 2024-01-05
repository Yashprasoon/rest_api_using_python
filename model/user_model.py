import pymysql
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
from CONFIG.config import dbconfig
class use_model():
    def __init__(self):
        try:
            self.con =pymysql.connect(host=dbconfig['hostname'],user=dbconfig['username'],password =dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit=True
            self.cur = self.con.cursor()
            print("connection successful")
        except:
            print("connection error")

    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users;")
        result = self.cur.fetchall()
        # print(type(result))
        # return json.dumps(result)
        if len(result)>0:
            res =make_response({"payload":result},200)
            res.headers['Acess-Control-Allow-Origin'] = '*'
            # res.headers['yash'] =True
            return res
        else:
            return  make_response({"message":"No Data Found"},204)
        
    def user_addone_model(self,data):
        print(self.cur.execute(f"INSERT into users values ({0},'{data['name']}','{data['email']}','{data['phone']}','{data['role']}','{data['password']}');"))
        print(data)
        return  make_response({"message":"User Created Successfully"},201)
    
    def add_multiple_users_model(self, data):
        # Generating query for multiple inserts
        qry = "INSERT INTO users(name, email, phone, roleid, password) VALUES "
        for userdata in data:
            qry += f" ('{userdata['name']}', '{userdata['email']}', '{userdata['phone']}', {userdata['roleid']},'{userdata['password']}'),"
        finalqry = qry.rstrip(",")
        self.cur.execute(finalqry)
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)
    
    def user_update_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role='{data['role']}',password='{data['password']}' WHERE id ={data['id']};")
        if self.cur.rowcount>0:return( make_response({"message":"User data updated successfully"},201))
        else: return  make_response({"message":"Nothing to update"},202)

    def user_delete_model(self,id):
        self.cur.execute(f"DELETE from users WHERE id={id}")
        if self.cur.rowcount>0:return make_response({"message":"User data deleted successfully"},200)
        else: make_response({"message":"Nothing to delete"},202)

    def user_patch_model(self,id,data):
        query = "UPDATE users SET "
        for key, values in data.items():
            query = query + f" {key} ='{data[key]}',"
        query=query[:-1]
        query+=f" WHERE id = {id};"
        self.cur.execute(query)
        if self.cur.rowcount>0:return( make_response({"message":"User data updated successfully"},201))
        else: return  make_response({"message":"Nothing to update"},202)
       
       
    def user_pagination_model(self,limit,page):
        limit=int(limit)
        page = int(page)
        start =(page*limit)-limit
        query = f"SELECT * FROM users LIMIT {start},{limit};"
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result)>0:
            res =make_response({"limit":limit,"page_no":page,"payload":result},200)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            return  make_response({"message":"No Data Found"},204)

    def user_upload_avatar_model(self,uid,filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"FILE_UPLOADED_SUCCESSFULLY", "path":filepath},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)
        
    def user_login_model(self,data):
        self.cur.execute(f"SELECT id, name, email,phone, avatar, role_id FROM users WHERE email='{data['email']}' and password ='{data['password']}';")
        result = self.cur.fetchall()
        userdata= result[0]
        exp_time = datetime.now()+ timedelta(minutes = 15)
        exp_epoch_time = int(exp_time.timestamp())
        payload ={
            "payload":userdata,
            "exp":exp_epoch_time
        }
        jwt_token =jwt.encode(payload,"yash",algorithm="HS256")
        return make_response({"jwt_token":jwt_token},200)
        

    def add_multiple_users_model(self, data):
        # Generating query for multiple inserts
        qry = "INSERT INTO users(name, email, phone, roleid, password) VALUES "
        for userdata in data:
            qry += f" ('{userdata['name']}', '{userdata['email']}', '{userdata['phone']}', {userdata['roleid']},'{userdata['password']}'),"
        finalqry = qry.rstrip(",")
        self.cur.execute(finalqry)
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)