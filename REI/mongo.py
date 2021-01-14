from .settings import *
from pymongo.mongo_client import MongoClient
MongoClient.HOST = 'mongodb://admin-munawar:L1GvzLE7C8VuCsUA@rei-database-shard-00-00.94yhc.mongodb.net:27017,rei-database-shard-00-01.94yhc.mongodb.net:27017,rei-database-shard-00-02.94yhc.mongodb.net:27017/REIMongo?ssl=true&replicaSet=atlas-770ftc-shard-0&authSource=admin&retryWrites=true&w=majority'

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'REIMongo',
        "CLIENT": {
            "host": 'mongodb://admin-munawar:L1GvzLE7C8VuCsUA@rei-database-shard-00-00.94yhc.mongodb.net:27017,rei-database-shard-00-01.94yhc.mongodb.net:27017,rei-database-shard-00-02.94yhc.mongodb.net:27017/REIMongo?ssl=true&replicaSet=atlas-770ftc-shard-0&authSource=admin&retryWrites=true&w=majority',
            "username": 'admin-munawar',
            "password": 'L1GvzLE7C8VuCsUA',
            "authMechanism": "SCRAM-SHA-1",
        },
    },
}