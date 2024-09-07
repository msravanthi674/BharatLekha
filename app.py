from flask import Flask, request, redirect, url_for, render_template,jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
# import pickle

# with open('model\recipient (1).pkl' ,'rb') as model_file:
#     model = pickle.load(model_file)

app = Flask(__name__, static_folder='static')    
CORS(app, resources={r"/api/*": {"origins": "*"}})  

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True  
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"
Session(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin1234@127.0.0.1/post_office'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Delivery model
class Delivery(db.Model):
    __tablename__ = 'deliveries' 
    consignment_id = db.Column(db.String(13), primary_key=True)
    recipient_phone_number = db.Column(db.String(15), nullable=False)
    delivery_time_slot = db.Column(db.String(20), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    sender_pincode = db.Column(db.String(6), nullable=False)
    recipient_pincode = db.Column(db.String(6), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    delivery_date = db.Column(db.Date,nullable=True)          

# login page endpoint
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        consignment_id = request.form.get('consignment_id', "").strip()
        phone_number = request.form.get('phone_number', "").strip()

        print(f"Received consignment_id: {consignment_id}")
        print(f"Received phone_number: {phone_number}")

        # Query the database to check if the consignment ID and phone number match
        delivery = Delivery.query.filter_by(consignment_id=consignment_id, recipient_phone_number=phone_number).first()

        if delivery:
            print("Match found!")
            return redirect(url_for('tracking', consignment_id=consignment_id))  # Pass consignment_id to tracking
        else:
            print("No match found.")
            return "Invalid consignment ID or phone number", 401

    return render_template('login.html')  # Adjust this to your login form template


#redirect to tracking page if authenticated
@app.route('/tracking')
def tracking():
    consignment_id = request.args.get('consignment_id')

    if consignment_id:
        delivery = Delivery.query.filter_by(consignment_id=consignment_id).first()
        if delivery:
            return render_template('tracking.html', tracking_id=delivery.consignment_id,
                                   recipient_name=delivery.recipient_name,
                                   time_slot=delivery.delivery_time_slot,
                                   sender_pincode=delivery.sender_pincode,
                                   recipient_pincode=delivery.recipient_pincode,
                                   status=delivery.status,
                                   delivery_date=delivery.delivery_date.strftime('%d %B %Y') if delivery.delivery_date else 'Date not available'
                                   )
        else:
            return "No delivery found for the given consignment ID", 404
    else:
        return "Consignment ID is required", 400
    

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        # Process selected date and time slot
        data = request.get_json()
        selected_date = data.get('selected_date')
        selected_time_slot = data.get('selected_time_slot')

        if selected_date and selected_time_slot:
            # Redirect to the recipient page (or `intimation` if you prefer)
            return redirect(url_for('intimation'))
        else:
            return jsonify({'success': False, 'error': 'Invalid data'}), 400

    return render_template('confirm.html')

@app.route('/intimation')
def intimation():
    return render_template('intimation.html')



@app.route('/app')
def index():
    return "Hello world"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




