import os
import csv
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from supabase import create_client, Client

# Supabase setup
SUPABASE_URL = "https://aufgvpbzsffzjhrxcnhl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1Zmd2cGJ6c2ZmempocnhjbmhsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDQ3MzYxMSwiZXhwIjoyMDcwMDQ5NjExfQ.RtG1sZHCTOlzGSBgtbVT_hTp0uahsJY9hRUXlRFzOAs"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'FR_PROJECT_ECE025_copy\FR_webapp_main\static\images'
BUCKET_NAME = 'image-attendance'  # your Supabase bucket name
CSV_FILE_PATH = 'registered_students.csv'

# Ensure upload and CSV file exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
if not os.path.isfile(CSV_FILE_PATH):
    with open(CSV_FILE_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Reg No', 'Courses','photo_filename'])  # Header

# Make sure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def register():
    message = None
    name = reg_no = courses = image_url = None

    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            reg_no = request.form.get('reg_no', '').strip()
            courses_raw = request.form.get('courses', '').strip()
            photo = request.files.get('photo')

            # Check for missing fields
            if not name or not reg_no or not courses_raw or not photo:
                message = "All fields are required."
                return render_template('register_reg.html', message=message)

            # Convert and validate reg_no
            try:
                reg_no = int(reg_no)
            except ValueError:
                message = "Registration number must be a valid integer."
                return render_template('register_reg.html', message=message)

            courses = [course.strip() for course in courses_raw.split(',') if course.strip()]
            if not courses:
                message = "Please provide at least one course."
                return render_template('register_reg.html', message=message)

            # Check duplicate reg_no
            existing = supabase.table("Attendance List").select("*").eq("Reg No", reg_no).execute()
            if existing.data:
                message = f"Registration failed: reg_no {reg_no} already exists."
                return render_template('register_reg.html', message=message)

            # Save photo locally
            filename = secure_filename(f"{reg_no}.jpg")
            local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(local_path)

            # Upload to Supabase (remove if already exists)
            bucket = supabase.storage.from_(BUCKET_NAME)
            existing_files = bucket.list()
            if any(obj['name'] == filename for obj in existing_files):
                bucket.remove([filename])
            with open(local_path, "rb") as f:
                bucket.upload(filename, f)

            # Insert student data
            data = {
                "Name": name,
                "Reg No": reg_no,
                "Courses": courses,
                "Photo Filename": filename
            }
            response = supabase.table("Attendance List").insert(data).execute()
            if not response.data:
                message = "Database insert failed."
                return render_template('register_reg.html', message=message)
            # Append to CSV
            with open(CSV_FILE_PATH, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, reg_no, ', '.join(courses), filename])

            image_url = '/' + local_path.replace('\\', '/')
            message = "Registration successful!"

        except Exception as e:
            message = f"Unexpected error: {str(e)}"

    return render_template('register_reg.html', message=message, name=name, reg_no=reg_no, courses=courses, image_url=image_url)
@app.route('/webapp.html')
def home():
    return render_template('webapp.html')   # Renders home page

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(port=5001)
