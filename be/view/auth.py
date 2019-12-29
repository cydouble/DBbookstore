#!/usr/bin/env python3

from flask import Flask, jsonify,request,render_template
from flask_httpauth import HTTPBasicAuth
from flask import Blueprint
from be.model import about_token # pytest
from be.model import user # pytest
# from model import about_token
# from model import user 
# import user

bp = Blueprint("mul",__name__,url_prefix="/auth")
token = ''
auth = HTTPBasicAuth()
# @bp.route("/")
# def home_page():
#     return "please give url like login or register to buy some books."
  
@bp.route("/register",methods=('GET','POST'))
def register_page():
  # if request.method == "GET":
    # return render_template("register.html")
  if request.method == "POST":
    user_info = request.json
    # user_info = request.values.to_dict()
    regis = user.register_action()
    code,msg = regis.register(user_info.get('user_id'),user_info.get('password'))
    return jsonify({"message":msg}),code

@bp.route("/unregister",methods=('GET','POST'))
def unregister_page():
  # if request.method == "GET":
  #   return render_template("register.html")
  if request.method == "POST":
    user_info = request.json
    # user_info = request.values.to_dict()
    regis = user.register_action()
    code,msg = regis.unregister(user_info.get('user_id'),user_info.get('password'))
    return jsonify({"message":msg}),code
  
@bp.route("/login", methods=("GET", "POST"))  # 指定请求方式，如果不指定，则无法匹配到请求
def login():
  # if request.method == "GET":   # GET请求
  #   return render_template("login.html")
  if request.method == "POST":   # POST请求
    user_info = request.json
    # user_info = request.values.to_dict()   # request.values获取数据并转化成字典
    logi = user.loginout_action()
    code,msg = logi.login(user_info.get('user_id'),user_info.get('password'),user_info.get('terminal'))
    global token
    if code == 200:
      token = about_token.generate_auth_token(user_info.get('user_id'),user_info.get('terminal'))
    else:
      token = ''
    return jsonify({"message":msg,"token":token}),code

@bp.route("/logout", methods=("GET", "POST"))  # 指定请求方式，如果不指定，则无法匹配到请求
def logout():
  # if request.method == "GET":   # GET请求
  #   return render_template("logout.html")
  if request.method == "POST":   # POST请求
    user_info = request.json
    # user_info = request.values.to_dict()   # request.values获取数据并转化成字典
    logo = user.loginout_action()
    token = request.headers['token']
    # global token
    # print("@@@@@@@@@@@@@@@@@",token)
    user_exit = about_token.verify_token(token)
    if user_exit != None:
      code,msg = logo.logout(user_info.get('user_id'))
      return jsonify({"message":msg}),code
    else:
      return jsonify({'message':"logout failed for bad token you do not login"}),401

@bp.route("/password", methods=("GET", "POST"))  # 指定请求方式，如果不指定，则无法匹配到请求
def change_pwd():
  # if request.method == "GET":   # GET请求
  #   return render_template("password.html")
  if request.method == "POST":   # POST请求
    user_info = request.json
    # user_info = request.values.to_dict()   # request.values获取数据并转化成字典
    old2new = user.loginout_action()
    code,msg = old2new.change_password(user_info.get('user_id'),user_info.get('oldPassword'),user_info.get('newPassword'))
    return jsonify({'message':msg}),code

# @bp.route("/fun", methods=["GET"])
# # @auth.login_required
# def fun():   # 测试是否需要token才能执行函数
#     #拿到token，去换取用户信息
#     # print(request.headers())
#     # token = request.headers['Authorization']
#     user = about_token.verify_token(token)
#     if user != None:
#       data = {
#           "name":user.user_id,
#           "user_money":user.user_money
#       }
#       return jsonify({"msg":"success","data":data})
#     else:
#       return jsonify({"msg":"bad signature or signature expired"})


