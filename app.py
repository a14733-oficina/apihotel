from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis,Hotel
from con_sql_alchemy import bd
from resources.user import User,UserRegister,UserLogin,Userlogout
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from datetime import timedelta


app=Flask(__name__)
api =Api(app)
jwt=JWTManager(app)#inicializa o jwt para dar autentificacao de pag

#configs
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///hoteis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_SECRET_KEY"]= "a_minha_chave_secreta_longa_e_intrasnsmissivel"
app.config["JWT_BLACKLIST_ENABLE"]=True 
app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(minutes=10)
@jwt.token_in_blocklist_loader
def verifica_blocklist(jwt_header,jwt_payload):
    jti = jwt_payload["jti"]
    return  jti in BLOCKLIST
@jwt.revoked_token_loader
def token_invalido(jwt_header,jwt_payload):
    return {"mensagem":"Logout efetuado faça login para aceder novamente"}

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")
api.add_resource(User, "/user/<string:username>")
api.add_resource(UserRegister, "/registar")
api.add_resource(UserLogin,"/login")
api.add_resource(UserLogin,"/logout")
if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all()#cria tds as tabelas defenidas nk modelo sqlalchemy
    app.run(debug=True)