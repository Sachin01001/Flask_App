# Flask_App
Connect to Your EC2 Instance
ssh -i /path/to/your-key.pem ubuntu@44.242.208.133

Update and Install Dependencies
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-dev build-essential -y

Upload Your Application Files on EC2
scp -i /path/to/your-key.pem /path/to/your/app.py ubuntu@44.242.208.133:/home/ubuntu/

Set Up the Application
Install Python Packages
pip3 install flask flask_sqlalchemy flask_jwt_extended werkzeug

Navigate to the directory where you uploaded your Flask application:
cd /home/ubuntu/

Run the Flask Application
Install Gunicorn
pip3 install gunicorn

Run the Flask Application with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8990 app:app

Run Application File
python3 app.py

Sample API requests for testing (Postman)
http://localhost:8990/register
http://localhost:8990/login
http://localhost:8990/dashboard

AWS EC2 url to access your application

http://44.242.208.133:8990/






