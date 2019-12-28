#import app
from flask import Blueprint, jsonify, request, render_template
import json
# from model import seller
from be.model import seller # pytest

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")

@bp_seller.route("/create_store", methods=('GET','POST'))
def seller_create_store():
    if request.method == "GET":
        return render_template("create_store.html")
    if request.method == "POST":
        store_info = request.json
        # store_info = request.values.to_dict()
        user_id = store_info.get("user_id")
        store_id = store_info.get("store_id")
        new_seller = seller.seller_action()
        code, message = new_seller.create_store(user_id, store_id)
        return jsonify({"message": message}), code


@bp_seller.route("/add_book", methods=('GET','POST'))
def add_book():
    if request.method == "GET":
        return render_template("add_book.html")
    if request.method == "POST":
        book_infomation = request.json
        seller_id = book_infomation.get("user_id")
        store_id = book_infomation.get("store_id")
        book_info = book_infomation.get("book_info")
        storage = book_infomation.get("stock_level")
        new_seller = seller.seller_action()
        code, message = new_seller.add_book(seller_id, store_id, json.dumps(book_info), storage)
        return jsonify({"message": message}), code


@bp_seller.route("/add_stock_level", methods=('GET','POST'))
def add_stock_level():
    if request.method == "GET":
        return render_template("add_stock_level.html")
    if request.method == "POST":
        # storage_info = request.values.to_dict()
        storage_info = request.json
        user_id = storage_info.get("user_id")
        store_id = storage_info.get("store_id")
        book_id = storage_info.get("book_id")
        add_stock_level = storage_info.get("add_stock_level")

        new_seller = seller.seller_action()
        code, message = new_seller.add_stock_level(user_id, store_id, book_id, add_stock_level)
        return jsonify({"message": message}), code


@bp_seller.route("/deliver", methods=('GET','POST'))
def deliver():
    if request.method == "GET":
        return render_template("deliver.html")
    if request.method == "POST":
        # order_info = request.values.to_dict()
        order_info = request.json
        order_id = order_info.get("order_id")

        the_order  = seller.seller_action()
        code, message = the_order.deliver(order_id)
        return jsonify({"message": message}), code


@bp_seller.route("/recieve", methods=('GET','POST'))
def recieve():
    if request.method == "GET":
        return render_template("deliver.html")
    if request.method == "POST":
        # order_info = request.values.to_dict()
        order_info = request.json
        order_id = order_info.get("order_id")

        the_order  = seller.seller_action()
        code, message = the_order.recieve(order_id)
        return jsonify({"message": message}), code
