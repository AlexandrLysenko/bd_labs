from django.shortcuts import render, redirect
from  DBManager import  DB

db = DB()

def test(request):
    if request.method == 'GET':
        products = db.getProductList()
        for product in products:
            print product.name