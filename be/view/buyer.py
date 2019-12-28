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


@bp_buyer.route("/new_order", methods=["GET","POST"])
def new_order_page():
    if request.method == "GET":
        return render_template("new_order.html")
    if request.method == "POST":
        order_info = request.values.to_dict()
        print(order_info)
        user_id = order_info.get("user_id")
        print(user_id)
        store_id = order_info.get("store_id")
        print(store_id)
        books_str = order_info.get("book_info")
        books: [] = json.loads(books_str)
        print(books)

        id_and_count = []
        for book in books:
            book_id = book.get("id")
            count = book.get("count")
            id_and_count.append((book_id, count))

        b = buyer_action()
        code, message, order_id = b.new_order(user_id, store_id, id_and_count)
        return jsonify({"message": message, "order_id": order_id}), code


@bp_buyer.route("/payment", methods=["GET","POST"])
def payment_page():
    if request.method == "GET":
        return render_template("payment.html")
    if request.method == "POST":
        payment_info = request.values.to_dict()
        user_id: str = payment_info.get("username")
        order_id: str = payment_info.get("order_id")
        password: str = payment_info.get("password")
        b = buyer_action()
        code, message = b.payment(user_id, password, order_id)
        return jsonify({"message": message}), code


@bp_buyer.route("/add_funds", methods=["GET","POST"])
def add_funds_page():
    if request.method == "GET":
        return render_template("add_funds.html")
    if request.method == "POST":
        add_funds_info = request.values.to_dict()
        user_id = add_funds_info.get('username')
        password = add_funds_info.get('password')
        add_value = int(add_funds_info.get('add_value'))
        b = buyer_action()
        code, message = b.add_funds(user_id, password, add_value)
        return jsonify({"message": message}), code


@bp_buyer.route("/cancel_order", methods=["GET","POST"])
def cancel_order_page():
    if request.method == "GET":
        return render_template("cancel_order.html")
    if request.method == "POST":
        cancel_info = request.values.to_dict()
        user_id = cancel_info.get('username')
        password = cancel_info.get('password')
        order_id = cancel_info.get('order_id')
        b = buyer_action()
        code, message = b.cancel_order(user_id, password, order_id)
        return jsonify({"message": message}), code


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


