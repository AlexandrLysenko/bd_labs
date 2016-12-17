from django.shortcuts import render, redirect
from  DBManager import  DB
import time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

db = DB()

def main(request):
    msgs = ""
    status = ""
    if('client_id' in request.GET and request.GET['client_id'] != '0'):
        if db.status(request) == 0:
            status =  "using cash"
        else: status = "without cash"

        start_time = time.time()
        orderslist = db.search(request)
        time_res = time.time() - start_time
        msgs = str(time_res)
        print db.status(request)
    else:
        orderslist = db.getOrderList()

    customers = db.getCustomerList()

    paginator = Paginator(orderslist, 25)  # Show per page
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)

    return render(request, 'main_page.html', {'status': status, 'msgs': msgs, 'orders': orders, 'customers': customers, 'total': str(len(orderslist))})

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

