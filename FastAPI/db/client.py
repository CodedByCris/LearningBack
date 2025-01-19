from pymongo import MongoClient

# Base de datos en la nube
db_client = MongoClient("mongodb+srv://crisTest:Test123*@clustercursopython.1gkrt.mongodb.net/?retryWrites=true&w=majority&appName=ClusterCursoPython").crisTest

# Base de datos local
# db_client = MongoClient().local