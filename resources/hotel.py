from flask import Flask
from flask_restful import Resource,reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {"hoteis":[hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome",type=str, required = True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("estrelas",type=float, required = True, help="As estrelas do hotel são obrigatório")
    argumentos.add_argument("diaria",type=float, required = True, help="A diaria do hotel é obrigatória")
    argumentos.add_argument("cidade",type=str, required = True, help="A cidade do hotel é obrigatório")
    
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)#ou devolve o hotel ou nada
        if hotel is not None:
            return hotel.json(), 200
        return{"mensagem": "Hotel não foi encontrado"}
    
    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        Hotel= HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            return{"mensagem": f"O hotel com id {hotel_id} já existe na minha lista."}
        novo_hotel = HotelModel(hotel_id,**dados)  
        try:
            novo_hotel.save_hotel()
            return novo_hotel.json(),200
        except:
            return{"mensagem": "Um erro interno do server aconteceu"},500
    
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        if HotelModel.find_hotel(hotel_id):
            try:
                hotel.update_hotel(*dados)
                return hotel,json(), 200
            except:
                return{"mensagem": "Um erro interno do server aconteceu"},500
            
        
        novo_hotel = HotelModel(hotel_id,**dados)  
        novo_hotel.save_hotel()
        return novo_hotel.json,201
    

    def delete(self,hotel_id):
        hotel =HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            try:
                hotel.delete_hotel()
            except:
                return{"mensagem": "Um erro interno do server aconteceu"},500
            
            return {"Mensagem": "Hotel removido"},200
        return {"Mensagem": "Hotel n encontrado"},404
