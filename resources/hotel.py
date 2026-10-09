from flask import Flask
from flask_restful import Resource,reqparse
from models.hotel import HotelModel
hoteis =[
    {"hotel_id": "paraiso","Nome":"Hotel paraiso","estrelas":4.8,"diaria":125.75,"cidade":"Porto"},
    {"hotel_id": "fukui","Nome":"Hotel Fukiu paradise","estrelas":4.9,"diaria":127,"cidade":"Lisboa"},
    {"hotel_id": "roxo","Nome":"Hotel do cabelo Roxo","estrelas":5,"diaria":1000,"cidade":"Trofa"}
]


class Hoteis(Resource):
    def get(self):
        return {"hoteis": hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome",type=str, required = True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("estrelas",type=float, required = True, help="As estrelas do hotel são obrigatório")
    argumentos.add_argument("diaria",type=float, required = True, help="A diaria do hotel é obrigatória")
    argumentos.add_argument("cidade",type=str, required = True, help="A cidade do hotel é obrigatório")
    def encontrar_hotel(self, hotel_id):
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return hotel
    def get(self, hotel_id):
        hotel = self.encontrar_hotel(hotel_id)
        if hotel is not None:
            return hotel, 200
        return{"mensagem": "Hotel não foi encontrado"}
    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = self.encontrar_hotel(hotel_id)
        if hotel is not None:
            return{"mensagem": f"O hotel com id {hotel_id} já existe na minha lista."}
        
        novo_hotel = {"hotel_id": hotel_id, **dados}
        hoteis.append(novo_hotel)
        return novo_hotel,200
    def put(self, hotel_id):
       
        dados = Hotel.argumentos.parse_args()
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                hotel.update(dados)
                return hotel, 200
        novo_hotel = {"hotel_id": hotel_id, **dados}        
        hoteis.append(novo_hotel)
        return novo_hotel,200
    

    def delete(self,hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return { "mensagem": f"O hotel com id {hotel_id} foi removido cm sucesso"},200