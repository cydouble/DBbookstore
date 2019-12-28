#!/usr/bin/env python3

from flask import Flask, jsonify,request,render_template
from flask_httpauth import HTTPBasicAuth
from flask import Blueprint
from model import about_token
# from be.model import buyer # pytest
from model import buyer
from view import auth
import json
from model import error
# import user

bp_buyer = Blueprint("buyer",__name__,url_prefix="/buyer")
      
@bp_buyer.route("/book",methods=('GET','POST'))
def searching_book():
    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        user_info = request.values.to_dict()
        store_id = user_info.get('store_id')
        by = user_info.get('by')
        by_what = user_info.get('by_what')
        print(user_info)
        if store_id == None:
            sbk = buyer.search_bookstation_action()
            if by == 'title':
                code, msg = sbk.search_book_title(by_what)
            if by == 'tags':
                code, msg = sbk.search_book_tag(by_what)
            if by == 'author':
                code, msg = sbk.search_book_author(by_what)
            if by == 'content':
                code, msg = sbk.search_book_content(by_what)
            if by == 'bookintro':
                code, msg = sbk.search_book_intro(by_what)
        else:
            sbk = buyer.search_bookstore_action()
            if by == 'title':
                code, msg = sbk.search_book_title(by_what, store_id)
            if by == 'tags':
                code, msg = sbk.search_book_tag(by_what, store_id)
            if by == 'author':
                code, msg = sbk.search_book_author(by_what, store_id)
            if by == 'content':
                code, msg = sbk.search_book_content(by_what, store_id)
            if by == 'bookintro':
                code, msg = sbk.search_book_intro(by_what, store_id)
        out = []
        print(code)
        if code == 200:
            for m in msg:
                dic = {
                    'title': m[0], 
                    'original_title': m[1],
                    'author': m[2],
                    'tags': m[3],
                    'price': m[4],
                    'store_id': m[5],
                    'storage': m[6],
                    'book_intro': m[7],
                    'content': m[8]}
                js = json.dumps(dic,indent=4,ensure_ascii=False)
                print(js)
                out.append(js)
        return jsonify({"message":msg}),code

@bp_buyer.route("/myorder",methods=('GET','POST'))
def user_order():      
    if request.method == "GET":
        return render_template("userorder.html")
    if request.method == "POST":
        user_info = request.values.to_dict()
        user_orderlist = buyer.search_order_action()
        user_id = user_info.get('username')
        order_id = user_info.get('orderid')
        user = about_token.verify_token(auth.token)
        if user.user_id == user_id:
            if order_id == None:
                code,msg = user_orderlist.search_order_history(user_id)
            else:
                code,msg = user_orderlist.search_order_status(user_id,order_id)
            return jsonify({"message":msg}),code
        else:
            return error.error_and_message_code(522)

@bp_buyer.route("/myorder/seller", methods=("GET","POST"))
# @auth.login_required
def seller_order():   
    #拿到token，去换取用户信息
    # print(request.headers())
    # token = request.headers['Authorization']
    if request.method == "GET":
        return render_template("sellerorder.html")
    if request.method == "POST":
        user_info = request.values.to_dict()
        user_orderlist = buyer.search_order_action()
        user_id = user_info.get('username')
        store_id = user_info.get('storeid')
        user = about_token.verify_token(auth.token)
        if user.user_id == user_id:
            if store_id == None:
                code,msg = user_orderlist.search_order_history_seller(user_id)
            else:
                code,msg = user_orderlist.search_order_status_seller(user_id,store_id)
            return jsonify({"message":msg}),code
        else:
            return error.error_and_message_code(522)


