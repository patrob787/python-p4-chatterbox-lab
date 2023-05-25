from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", 'POST'])
def messages():
    
    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            messages.append(message_dict)
        
        resp = make_response(messages, 200)
        
    
    elif request.method == 'POST':
        request_data = request.get_json()
        new_message = Message(
            body = request_data['body'],
            username = request_data['username']
        )
        db.session.add(new_message)
        db.session.commit()

        new_dict = new_message.to_dict()
        resp = make_response(new_dict, 201)
    
    return resp



@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
 
    if request.method == 'GET':
        message_dict = message.to_dict()
        
        resp = make_response(jsonify(message_dict), 200)
    
    elif request.method == 'PATCH':
        
        data = request.get_json()

        for attr in data:
            setattr(message, attr, data[attr])

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        resp = make_response(message_dict, 200)
        

    elif request.method == 'DELETE':

        db.session.delete(message)
        db.session.commit()

        resp_body = {
            "message": "delete successful"
        }

        resp = make_response(jsonify(resp_body), 200)
    
         
    return resp


if __name__ == '__main__':
    app.run(port=5555)
