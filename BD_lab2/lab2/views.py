from django.shortcuts import render, redirect
from  DBManager import  DB

db = DB()

def main(request):
    orders = db.getOrderList()
    return render(request, 'main_page.html', {'orders': orders})

def remove(request, id):
    db.removeOrder(id)
    return redirect('/')


def add(request):
    if request.method == 'GET':
        products = db.getProductList()
        stores = db.getStoreList()
        customers = db.getCustomerList()
        return render(request, 'add_page.html', {'products': products, 'stores': stores, 'customers': customers})
    elif request.method == 'POST':
        db.saveOrder({'product': request.POST['product'], 'customer': request.POST['customer'],
                      'store': request.POST['store']})
        return redirect('/')

def edit(request, id):
    if request.method == 'GET':
        products = db.getProductList()
        stores = db.getStoreList()
        customers = db.getCustomerList()
        order = db.getOrder(id)

        return render(request, 'edit_page.html',
                      {'products': products, 'stores': stores, 'customers': customers, 'order': order})
    elif request.method == 'POST':
        db.updateOrder({'order': id, 'product': request.POST['product'], 'customer': request.POST['customer'],
                      'store': request.POST['store']})
        return redirect('/')

def topproducts(request):
    products = db.getTopProductsAggregate()
    return render(request, 'top_products.html', {'products': products})

