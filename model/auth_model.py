import pymysql
import json
from flask import make_response, request
from datetime import datetime, timedelta
import jwt
import re
from CONFIG.config import dbconfig
from functools import wraps
class auth_model():
    def __init__(self):
        try:
            self.con =pymysql.connect(host=dbconfig['hostname'],user=dbconfig['username'],password =dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit=True
            self.cur = self.con.cursor()
            print("connection successful")
        except:
            print("connection error")

    def token_auth(self ):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                # print(endpoint)
                authorization = request.headers.get("Authorization")
                if re.match("Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwt_decoded = jwt.decode(token,"yash",algorithms="HS256")
                        print(jwt_decoded)

                    except jwt.ExpiredSignatureError :
                        return make_response({"ERROR":"TOKEN_EXPIRED"}, 401)

                    role_id = jwt_decoded['payload'][5]
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint = '{endpoint}'")
                    result = self.cur.fetchall()
                    if len(result)>0:
                        allowed_roles =json.loads(result[0][0]) 
                        # print(allowed_roles)
                        if role_id in allowed_roles:
                            return func(*args)
                        return func(*args)
                    else:
                        return make_response({"ERROR":"UNKNOWN_ENDPOINT"}, 404)    

                else: 
                    return make_response({"ERROR":"INVALID_TOKEN"}, 401)    

            return inner2
        return inner1
