from flask import Flask
from flask_restful import Resource,Api,reqparse
from resources.hotel import Hoteis,Hotel
from con_sql_alchemy import bd

app=Flask(__name__)
api =Api(app)

#configs
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///hoteis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all()#cria tds as tabelas defenidas nk modelo sqlalchemy
    app.run(debug=True)