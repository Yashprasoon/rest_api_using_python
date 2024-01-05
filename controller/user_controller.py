from flask import request,send_file
from app import app
from model.user_model import use_model
from model.auth_model import auth_model
from datetime import datetime 
import os
user_model_obj = use_model()
auth = auth_model()

@app.route('/user/getall',methods=['GET']) 
@auth.token_auth()
def user_getall_controller(): 
    return user_model_obj.user_getall_model()

@app.route('/user/addone',methods=['POST']) 
@auth.token_auth()
def user_addone_controller(): 
    data =request.form
    data.get
    return user_model_obj.user_addone_model(request.form)
 
@app.route("/user/addmultiple", methods=["POST"])
@auth.token_auth()
def add_multiple_users():
    return user_model_obj.add_multiple_users_model(request.json) 

@app.route('/user/update',methods=["PUT"])
@auth.token_auth()
def user_update_controller():
    
    return user_model_obj.user_update_model(request.form)

@app.route('/user/delete/<id>', methods=["DELETE"])
@auth.token_auth()
def user_delete_controller(id):
    return user_model_obj.user_delete_model(id)

@app.route('/user/patch/<id>',methods=["PATCH"])
@auth.token_auth()
def user_patch_controller(id):
    return user_model_obj.user_patch_model(id,request.form)

@app.route('/user/getall/limit/<limit>/page/<page>', methods=["GET"])
@auth.token_auth()
def user_pagination_controller(limit,page):
    return user_model_obj.user_pagination_model(limit,page)

@app.route("/user/<uid>/upload/avatar",methods=["PUT"])
@auth.token_auth()
def user_upload_avatar_controller(uid):
    file = request.files['avatar']
    print(file)
    file.save(f"uploads/{file.filename}")
    new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating unique name for the file
    print(new_filename)
    split_filename = file.filename.split(".") # Spliting ORIGINAL filename to seperate extenstion
    print(split_filename)
    ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
    ext = split_filename[ext_pos] # Using last index to get the file extension
    db_path = f"uploads/{new_filename}.{ext}"
    file.save(db_path)
    return user_model_obj.user_upload_avatar_model(uid, db_path)
    

@app.route("/uploads/<filename>",methods=["GET"])
@auth.token_auth()
def user_get_avatar_controller(filename):
    return send_file(f"uploads/{filename}")


@app.route("/user/login",methods=['POST'])
def user_login_controller(): 
    request.form
    return user_model_obj.user_login_model(request.form)
    

@app.route("/user/addmultiple", methods=["POST"])
def add_multiple_users():
    return user_model_obj.add_multiple_users_model(request.json)