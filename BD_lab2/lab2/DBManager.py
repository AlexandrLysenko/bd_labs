import math
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.code import Code

class DB(object):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.local


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
        self.db.order.delete_one({'_id': ObjectId(id)})


    def saveOrder(self, info):
        product = self.db.products.find_one({'_id': ObjectId(info['product'])})
        customer = self.db.customers.find_one({'_id': ObjectId(info['customer'])})
        store = self.db.stores.find_one({'_id': ObjectId(info['store'])})

        order = {'products': product, 'customers': customer, 'stores': store}
        self.db.order.insert(order)


    def updateOrder(self, info):
        product = self.db.products.find_one({'_id': ObjectId(info['product'])})
        customer = self.db.customers.find_one({'_id': ObjectId(info['customer'])})
        store = self.db.stores.find_one({'_id': ObjectId(info['store'])})

        order = {'products': product, 'customers': customer, 'stores': store}
        self.db.order.update_one({'_id': ObjectId(info['order'])}, {'$set': order})

    def getTopProductsAggregate(self):
        products = list(self.db.order.aggregate(
            [{"$unwind": "$products.name"}, {"$project": {"name": "$products.name", "count": {"$add": [1]}}},
             {"$group": {"_id": "$name", "number": {"$sum": "$count"}}}, {"$sort": {"number": -1}}, {"$limit": 3}]))
        return products

    def mapTopProduct(self):
        mapper = Code("""
                        function() {
                               var key = this.products.name;
                               var value = {count : 1};
                               emit(key, value);
                        };
                        """)
        reducer = Code("""
                            function (key, values) {
                                var count = 0;
                                for(var i in values){
                                    count += values[i].count;
                                }
                                return {count: count};
                            };
                            """)
        result = self.db.order.map_reduce(mapper, reducer, "result")
        res = list(result.find())
        print res

    def mapTopCustomer(self):
        mapper = Code("""
                        function() {
                               var key = this.customers.name;
                               var value = {count : 1};
                               emit(key, value);
                        };
                        """)
        reducer = Code("""
                            function (key, values) {
                                var count = 0;
                                for(var i in values){
                                    count += values[i].count;
                                }
                                return {count: count};
                            };
                            """)
        result = self.db.order.map_reduce(mapper, reducer, "result")
        res = list(result.find())
        print res

db = DB()
db.mapTopProduct()
db.mapTopCustomer()