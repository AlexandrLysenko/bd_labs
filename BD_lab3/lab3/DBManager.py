from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import redis
import pickle


class DB(object):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.local
        self.r = redis.StrictRedis()

    def getOrderList(self):
        orders = [order for order in self.db.order.find()]
        return orders

    def getProductList(self):
        products = [product for product in self.db.products.find()]
        return products

    def getStoreList(self):
        stores = [store for store in self.db.stores.find()]
        return stores

    def getCustomerList(self):
        customers = [customer for customer in self.db.customers.find()]
        return customers

    def getOrder(self, id):
        order = self.db.order.find_one({'_id': ObjectId(id)})
        return order

    def removeOrder(self, id):
        order = self.db.order.find_one({'_id': ObjectId(id)})
        self.r.delete(order["customers"]["_id"])
        self.db.order.delete_one({'_id': ObjectId(id)})

    def saveOrder(self, info):
        product = self.db.products.find_one({'_id': ObjectId(info['product'])})
        customer = self.db.customers.find_one({'_id': ObjectId(info['customer'])})
        store = self.db.stores.find_one({'_id': ObjectId(info['store'])})

        order = {'products': product, 'customers': customer, 'stores': store}
        self.db.order.insert(order)
        self.r.delete(ObjectId(info['customer']))

    def updateOrder(self, info):
        product = self.db.products.find_one({'_id': ObjectId(info['product'])})
        customer = self.db.customers.find_one({'_id': ObjectId(info['customer'])})
        store = self.db.stores.find_one({'_id': ObjectId(info['store'])})

        order = {'products': product, 'customers': customer, 'stores': store}

        lastorder = self.db.order.find_one({'_id': ObjectId(info['order'])})
        self.r.delete(lastorder["customers"]["_id"])

        self.db.order.update_one({'_id': ObjectId(info['order'])}, {'$set': order})

        self.r.delete(ObjectId(info['customer']))

    def generate(self):
        for i in range(0, 10000):
            rand_product = random.randint(0, 6)
            rand_customer = random.randint(0, 4)
            rand_store = random.randint(0, 2)
            product = self.db.products.find().skip(rand_product).next()
            customer = self.db.customers.find().skip(rand_customer).next()
            store = self.db.stores.find().skip(rand_store).next()

            order = {'products': product, 'customers': customer, 'stores': store}
            self.db.order.insert(order)

    def search(self, request):
        if self.r.exists(request.GET['client_id']) != 0:
            order = pickle.loads(self.r.get(request.GET['client_id']))
        else:
            query = {}
            if request.GET['client_id'] != '0':
                query["customers._id"] = ObjectId(request.GET['client_id'])
            order = list(self.db.order.find(query))
            self.r.set(request.GET['client_id'], pickle.dumps(order))
        return list(order)

    def status(self, request):
        if self.r.exists(request.GET['client_id']) != 0:
            return 0
        else:
            return 1



