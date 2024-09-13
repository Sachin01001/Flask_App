from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask application
app = Flask(__name__)

# Configure the database and JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Set the access token expiration time to 1 hour
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create the database and the initial Superadmin user
def create_initial_user():
    with app.app_context():  # Create an application context
        db.create_all()
        if not User.query.filter_by(username='superadmin').first():
            hashed_password = generate_password_hash('superadmin_password')
            superadmin = User(username='superadmin', password=hashed_password, role='Superadmin')
            db.session.add(superadmin)
            db.session.commit()

# Create the database and initial user when the application starts
create_initial_user()

# Define a simple route for the root URL
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the User Authentication System!"})

# Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

# User dashboard
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    try:
        current_user = get_jwt_identity()
        role = current_user['role']
        
        # Debugging: Log the current user's role
        print(f"Current user role: {role}")
        
        if role == 'Superadmin':
            users = User.query.all()
            return jsonify({"users": [{"id": user.id, "username": user.username, "role": user.role} for user in users]}), 200
        elif role == 'Admin':
            # Assuming Admin can only see users they created
            users = User.query.filter_by(role='User').all()  # Adjust this as needed
            return jsonify({"users": [{"id": user.id, "username": user.username, "role": user.role} for user in users]}), 200
        else:
            return jsonify({"msg": "Access denied"}), 403
    except Exception as e:
        print(f"Error accessing dashboard: {e}")
        return jsonify({"msg": "Error accessing dashboard"}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=8990)  # Change the port number here

