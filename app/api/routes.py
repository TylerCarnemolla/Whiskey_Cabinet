from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, Whiskey, User, booze_schema, bottles_schema


api = Blueprint('api', __name__, url_prefix='/api') #prefix means that it goes before the slug


@api.route('/whiskeys', methods = ['POST'])
@token_required
def add_whiskey(current_User_token):
    brand = request.json['brand']
    kind = request.json['kind']
    proof = request.json['proof']
    notes = request.json['notes']
    origin = request.json['origin']
    user_token = current_User_token.token

    print(f'BIG TESTER: {current_User_token.token}')

    whiskey = Whiskey(brand, kind, proof, notes, origin, user_token=user_token) #we do_User_token =_User_toked to over-write
    #the previous value for that variable

    db.session.add(whiskey)
    db.session.commit()

    response = booze_schema.dump(whiskey)
    return jsonify(response)

# this route is to bring back all whiskeys in the inventory

@api.route('/whiskeys', methods = ['GET'])
@token_required
def get_all_whiskeys(current_User_token):
    a_whiskey = current_User_token.token
    whiskeys = Whiskey.query.filter_by(user_token = a_whiskey).all()
    response = bottles_schema.dump(whiskeys)
    return jsonify(response)

# this route is to bring back one specific whiskey from the inventory
@api.route('/whiskeys/<id>', methods = ['GET'])
@token_required
def get_a_whiskey(current_User_token, id):
    whiskey = Whiskey.query.get(id)
    response = booze_schema.dump(whiskey)
    return jsonify(response)


#this route allows us to update a whiskey in case of a mistake

@api.route('/whiskeys/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey_info(current_User_token, id):
    whiskey = Whiskey.query.get(id)
    whiskey.brand = request.json['brand']
    whiskey.kind = request.json['kind']
    whiskey.proof = request.json['proof']
    whiskey.notes = request.json['notes']
    whiskey.origin = request.json['origin']
    whiskey.user_token = current_User_token.token

    db.session.commit()
    response = booze_schema.dump(whiskey)
    return jsonify(response)

# then if we need to delete a whiskey from the companies inventory
@api.route('/whiskeys/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_User_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = booze_schema.dump(whiskey)
    return jsonify(response)
