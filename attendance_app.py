from flask import Flask, render_template, Response, request, jsonify
import cv2
import face_recognition
import numpy as np
import pickle
import json
import os
from supabase import create_client, Client

app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = "https://aufgvpbzsffzjhrxcnhl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1Zmd2cGJ6c2ZmempocnhjbmhsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDQ3MzYxMSwiZXhwIjoyMDcwMDQ5NjExfQ.RtG1sZHCTOlzGSBgtbVT_hTp0uahsJY9hRUXlRFzOAs"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load encodings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
encode_file_path = "C:\\Users\\FAVOUR\\Documents\\AI\\Facial_biometric_attendance_system\\web_dev\\FR_PROJECT_ECE025_copy\\FR_webapp_main\\EncodeFile.p"

with open(encode_file_path, 'rb') as f:
    encodeListKnownWithIds = pickle.load(f)

encodeListKnown, studentIds = encodeListKnownWithIds

cap = cv2.VideoCapture(0)
current_student = {}
course_to_check = ""

@app.route('/set_course', methods=['POST'])
def set_course():
    global course_to_check
    data = request.get_json()
    course_to_check = data.get('course', '').strip().upper()
    return jsonify({"message": f"Course set to {course_to_check}"})

def gen_frames():
    global current_student, course_to_check
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (640, 480))  # Resize camera view
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        try:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
           
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
                face_distances = face_recognition.face_distance(encodeListKnown, face_encoding)
                best_match_index = np.argmin(face_distances)
                best_value= face_distances[best_match_index]

                if best_value < 0.4:
                    if matches[best_match_index]:
                        id = studentIds[best_match_index]

                        # Fetch student profile from Supabase
                        profile_response = supabase.table("Attendance List").select("*").eq("Reg No", id).execute()
                        records = profile_response.data

                        if records:
                            record = records[0]
                            name = record.get('Name', 'Unknown')
                            course_str = record.get("Courses", "[]")
                            courses = json.loads(course_str)

                            status = "Registered" if course_to_check in courses else "Not Registered"

                            current_student = {
                                "name": name,
                                "reg_no": id,
                                "courses": courses,
                                "status": status,
                                "course_checked": course_to_check
                            }

                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4

                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f'ID: {id}', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    status = "Not in Database"
        except Exception as e:
            print(f"Error in frame processing: {e}")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera')
def camera():
    return render_template('camera_att.html', student=current_student)

@app.route('/student_info')
def student_info():
    return jsonify(current_student)

@app.route('/webapp.html')
def home():
    return render_template('webapp.html')   # Renders home page

if __name__ == '__main__':
    app.run(port=5002)

