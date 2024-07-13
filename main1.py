from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/imgdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ImageRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_name = db.Column(db.String(50))
    date = db.Column(db.Date, default=datetime.utcnow().date)  
    time = db.Column(db.Time, default=datetime.utcnow().time)
    image = db.Column(db.LargeBinary)
    detected_category = db.Column(db.String(50))
    

    def __init__(self, camera_name, date, time, image, detected_category):
        self.camera_name = camera_name
        self.date = date
        self.time = time
        self.image = image
        self.detected_category = detected_category


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'camera_name' not in request.form  or 'image' not in request.files or 'detected_category' not in request.form:
        return 'Bad Request: Required fields missing in the request.', 400
    
    camera_name = request.form['camera_name']
    #date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    #time = datetime.strptime(request.form['time'], '%H:%M:%S').time()
    image = request.files['image'].read()
    detected_category = request.form['detected_category']

    current_utc_datetime = datetime.utcnow()
    current_date = current_utc_datetime.date()
    current_time = current_utc_datetime.time()
    
    # Create a new record in the database
    record = ImageRecord(camera_name=camera_name, date=current_date, time=current_time,image=image, detected_category=detected_category)
    db.session.add(record)
    db.session.commit()

    return 'Image record successfully uploaded.', 200

# Route for retrieving an image
@app.route('/get-image', methods=['GET'])
def get_image():
    record_id = request.args.get('id')

    if not record_id:
        return 'Bad Request: ID parameter is missing.', 400

    record = ImageRecord.query.get(record_id)
    if not record:
        return f'Image record with ID {record_id} not found.', 404

    return send_file(
        BytesIO(record.image),
        mimetype='image/jpeg',
        as_attachment=True,
        download_name=f'record_{record.id}.jpg'
    )

if __name__ == '__main__':
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True)
