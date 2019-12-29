from flask import Flask, jsonify,request,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # 生产token
from itsdangerous import BadSignature, SignatureExpired  
# pytest
from be.model.db_conn import extra_func
# from model.db_conn import extra_func
from flask_httpauth import HTTPTokenAuth
import functools
func = extra_func()
# class a_token:
#     token = ''
def generate_auth_token(user_id, ter, expiration=7200):  # 2min过期
    current_app.config["SECRET_KEY"] = '1234'
    serializer = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    token = serializer.dumps({"user_id":user_id,"ter":ter})
    return token.decode("ascii")

def verify_token(token):
    #参数为私有秘钥，跟上面方法的秘钥保持一致
    current_app.config["SECRET_KEY"] = '1234'
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        #转换为字典
        data = s.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    #拿到转换后的数据，根据模型类去数据库查询用户信息
    now_user = func.get_user(data['user_id'])
    return now_user

# def login_required(view_func):
#     @functools.wraps(view_func)
#     def verify_token(*args,**kwargs):
#         try:
#             #在请求头上拿到token
#             # token = request.headers(['z-token'])
#         except Exception:
#             #没接收的到token,给前端抛出错误
#             #这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
#             return jsonify(code = 4103,msg = token)
#         current_app.config["SECRET_KEY"] = '1234'
#         s = Serializer(current_app.config["SECRET_KEY"])
#         try:
#             s.loads(token)
#         except Exception:
#             return jsonify(code = 4101,msg = "登录已过期")
#         return view_func(*args,**kwargs)
#     return verify_token

