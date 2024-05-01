from flask import request,jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contaacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))    
    return jsonify({"contacts": json_contacts})
@app.route("/create_contact",methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    
    if not first_name or not last_name or not email:
        return(jsonify({"messege": "You must include your full name and email"},400,))

    new_contact= Contact(first_name=first_name,last_name=last_name,email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"messege": str(e)}),40
    
    return jsonify({"messege": "User Added Succesfully"}),201

@app.route("/update_contact/<int:user_id>")
def update_contact(user_id):
    contact = contact.query.get(user_id)
    
    if not contact: return jsonify({"messege":"User Not Found"}),404
    
    data=request.json
    contact.first_name = data.get("firstName",contact.first_name)
    contact.last_name = data.get("lastName",contact.last_name)
    contact.email = data.get("email",contact.email)
    
    db.session.commit()
    
    return jsonify({"messege": "User Updated Succesfully"}),201

@app.route("/delete_contact/<int:user_id>",methods=["DELETE"])
def delete_contact(user_id):
    contact = contact.query.get(user_id)
    
    if not contact: return jsonify({"messege":"User Not Found"}),404

    db.session.delete(contact)     
    db.session.commit()   
    return jsonify({"messege": "User Deleted Succesfully"}),201



if __name__ =="__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
    