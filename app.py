from flask import Flask, render_template, request ,flash ,session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate
from secret import SECRET_KEY
# import logging

# Setup logging
# logging.basicConfig(filename='app_debug.log', level=logging.DEBUG, 
                    # format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#  IPv4 Address. . . . . . . . . . . : 192.168.31.150

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Harsh%40123@localhost/coding'
app.config['SECRET_KEY'] = SECRET_KEY
# Define the upload folder
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
# Folder to store generated QR codes
# Define the folder for QR codes using BASE_DIR
app.config['QR_CODES_FOLDER'] = os.path.join(BASE_DIR, 'static', 'qrcodes')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['QR_CODES_FOLDER'], exist_ok=True)


# Optionally, set allowed file extensions for better security
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
db= SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

#####class models for databases
class User(db.Model):
    __tablename__ = 'users'  # Table name

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)  # Store hashed password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    events = db.relationship('Event', back_populates='user', lazy=True)


    def __repr__(self):
        return f"<User {self.id} - {self.email}>"

    def set_password(self, password):
        """Hash the password before storing it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    
# Event model
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship('Image', backref='event', lazy=True)
    user = db.relationship('User', back_populates='events')  # Back reference to the User model

    def __repr__(self):
        return f"<Event {self.id} - {self.event_name}>"

# Image model
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    folder_name = db.Column(db.String(100), nullable=True)  # Store folder name if applicable
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    # Check if passwords match
    if password != confirm_password:
        flash("Passwords do not match!", 'error')
        return redirect(url_for('index'))

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already registered!", 'error')
        return redirect(url_for('index'))

    # Create and store user
    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash("Signup successful! Please log in.", 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user_id'] = user.id  # Store the user session
        session['user_email'] = user.email  # Store the user email in the session
        flash("Login successful!", 'success')
        return redirect(url_for('home'))
    else:
        flash("Invalid email or password.", 'error')
        return redirect(url_for('home'))




@app.route("/")
def home():
    # user_email = session.get('user_email')
    # print("User email in session:", user_email)
    # return render_template('index.html', user_email=user_email, user_events=user_events)
    user_email = session.get('user_email')  # Check if a user is logged in
    user_events = []

    if user_email:
        # Query the database to get the user and their events
        user = User.query.filter_by(email=user_email).first()
        if user:
            user_events = user.events  # Access the events relationship in the User model

    return render_template('index.html', user_email=user_email, user_events=user_events)

@app.route("/contact")
def about():
    return render_template('contact.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash("Logged out successfully.", 'success')
    return redirect(url_for('home'))


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'GET':
        return render_template('create_event.html')

    elif request.method == 'POST':
        event_name = request.form['event_name']  # Get the event name from the form
        # description = request.form.get('description', '')  # Optional description

        # Check if event name is provided
        if not event_name:
            flash('Event name is required', 'error')
            return redirect(url_for('create_event'))

        # Get the current user (assuming user is logged in)
        user_id = session.get('user_id')

        if not user_id:
            flash('You need to be logged in to create an event', 'error')
            return redirect(url_for('login'))

        # Create and save the new event
        # new_event = Event(name=event_name, user_id=user_id)
        new_event = Event(event_name=event_name, user_id=user_id)
        db.session.add(new_event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('home'))



# @app.route('/upload_images/<int:event_id>', methods=['GET', 'POST'])
# def upload_images(event_id):
#     event = Event.query.get_or_404(event_id)
    
#     if request.method == 'POST':
        
#         folder_name = request.form.get('folder_name', '')  # Optional folder name
#         files = request.files.getlist('images')
        
#         for file in files:
#             if file:
#                 filename = secure_filename(file.filename)
#                 folder_path = os.path.join('static/uploads', str(event_id), folder_name)
#                 os.makedirs(folder_path, exist_ok=True)
                
#                 file_path = os.path.join(folder_path, filename)
#                 file.save(file_path)
                
#                 # Save image details to the database
#                 new_image = Image(event_id=event_id, file_path=file_path, folder_name=folder_name)
#                 db.session.add(new_image)
#             else:
#                     # If file type is not allowed, flash an error
#                     flash("Invalid file type. Please upload an image.", "error")
#                     return redirect(url_for('upload_images', event_id=event_id))
        
#         db.session.commit()
#         flash("Images uploaded successfully!", "success")
#         return redirect(url_for('view_event', event_id=event_id))
    
#     return render_template('upload_images.html', event=event)

@app.route('/upload_images/<int:event_id>', methods=['POST'])
def upload_images(event_id):
    try:
        if 'images' not in request.files:
            # logging.error("No file part in the request")
            return "No file part in the request", 400

        files = request.files.getlist('images')
        folder_name = request.form.get('folder_name', 'default_folder')

        # Path to save images for the event
        event_folder = os.path.join(app.config['UPLOAD_FOLDER'], f'event_{event_id}', folder_name)
        os.makedirs(event_folder, exist_ok=True)
        # logging.info(f"Created/Found folder: {event_folder}")

        for file in files:
            if file.filename == '':
                # logging.warning("Skipping empty file")
                continue
            
            # Sanitize and secure the filename
            filename = secure_filename(file.filename)
            file_path = os.path.join(event_folder, filename)
            # logging.debug(f"Saving file {filename} to path {file_path}")

            # Save the file to the calculated path
            file.save(file_path)

            # Normalize the path for database storage (convert to forward slashes)
            relative_path = os.path.relpath(file_path, app.static_folder).replace("\\", "/")
            # logging.debug(f"Relative file path for DB: {relative_path}")

            # Save the relative path to the database
            new_image = Image(event_id=event_id, file_path=relative_path, folder_name=folder_name)
            db.session.add(new_image)

        # Generate QR code for the event
        # custom_domain = "7zh73d83-4000.inc1.devtunnels.ms"
        # qr_url = f"/view_event/{event_id}"  # Construct the QR URL using your custom domain
        qr_url = url_for('view_event', event_id=event_id, _external=True) 
        qr_code_path = os.path.join(app.config['QR_CODES_FOLDER'], f'event_{event_id}.png')
        
        # Generate and save the QR code
        qr = qrcode.make(qr_url)
        qr.save(qr_code_path)
        # logging.info(f"QR Code saved at: {qr_code_path}")

        # Commit database changes
        db.session.commit()

        flash("Images uploaded successfully!", "success")
        return redirect(url_for('view_event', event_id=event_id))

    except Exception as e:
        # logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}", 500


@app.route('/show_qr/<event_id>')
def show_qr(event_id):
    # Render a template that shows the QR code
    qr_path = f'static/qrcodes/event_{event_id}.png'
    return f'''
        <h1>QR Code for Your Event</h1>
        <img src="/{qr_path}" alt="QR Code">
        <p>Scan this QR code to access your event images.</p>
        <a href="/view_event/{event_id}">View Event</a>
    '''

def generate_qr_code(event_id, qr_url):
    qr_code_path = os.path.join(app.config['QR_CODES_FOLDER'], f'event_{event_id}.png')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_code_path)

    return qr_code_path


@app.route('/view_event/<int:event_id>', methods=['GET'])
def view_event(event_id):
    event = Event.query.get_or_404(event_id)  # Fetch the event from the database
    images = Image.query.filter_by(event_id=event.id).all()  # Fetch all images for the event

    print('ttest')
    # Debugging images
    # for img in images:
        # logging.debug(f"test----Image: {img.file_path}, Folder: {img.folder_name}")

    event = {
        'event_name': event.event_name,
        'description': event.description,
        'images': [{'folder_name': img.folder_name, 'file_path': img.file_path} for img in images],
        'qr_code': f'qrcodes/event_{event_id}.png'  # Path to the QR code image
    }


    return render_template('view_event.html', event=event)

@app.route('/my_events')
def my_events():
    user_email = session.get('user_email')  # Check if a user is logged in
    user_events = []

    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            user_events = user.events  # Access the `events` relationship
    print(user_events)
    return render_template('my_events.html', user_events=user_events)



if __name__ == '__main__':
     with app.app_context():
        db.create_all()
     app.run(debug=True, port=4000)