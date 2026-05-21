Web-based Attendance System
Overview

The Web-based Attendance System is a real-time attendance management application that uses face recognition technology and cloud-based storage to automate student attendance tracking. The system is designed to improve accuracy, reduce manual attendance processes, and provide secure attendance verification for educational institutions.

This project integrates computer vision, Flask web development, and Supabase cloud services to deliver an intelligent and scalable attendance solution.

Features
Real-time face recognition for student verification
Automated attendance recording
Student registration with image upload
Secure cloud database integration using Supabase
Course enrollment verification
Live camera feed integration
Attendance logs and student records management
Responsive web interface
CSV attendance export support
Scalable and modular architecture

Technologies Used
Backend
Python
Flask
Frontend
HTML
CSS
JavaScript
AI / Computer Vision
OpenCV
face_recognition
NumPy
Database & Cloud
Supabase
PostgreSQL

Additional Tools
Git & GitHub
Pandas
System Architecture
Student registration with facial image capture/upload
Face encoding generation and storage
Live camera feed for attendance verification
Face recognition and identity matching
Course enrollment validation from Supabase
Attendance logging and record storage
Attendance visualization and export

Installation
Clone the Repository
git clone https://github.com/your-username/Web-based-Attendance-System.git
cd Web-based-Attendance-System
Create Virtual Environment
python -m venv venv
Activate Virtual Environment
Windows (PowerShell)
.\venv\Scripts\Activate.ps1
Windows (CMD)
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root and add:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key
Run the Application
python app.py

Open your browser and navigate to:

http://127.0.0.1:5000
Project Structure
Web-based-Attendance-System/
│
├── static/
├── templates/
├── uploads/
├── encodings/
├── attendance/
├── app.py
├── requirements.txt
├── README.md
└── .env

Use Cases
Universities and Colleges
Secondary Schools
Training Centers
Organizations requiring automated attendance systems
Future Improvements
Multi-camera support
Mobile application integration
Advanced analytics dashboard
Anti-spoofing and liveness detection
Role-based authentication system
AI-powered attendance insights
Email/SMS attendance notifications
Research Contribution

This project contributes to research in:

Artificial Intelligence
Computer Vision
Biometric Authentication
Smart Education Systems
Real-time Cloud-based Applications
Author

Favour Ibezim
Electronic Engineering Graduate | AI & Software Developer

License

This project is licensed under the MIT License.

Acknowledgements

Special thanks to:

OpenCV
Flask
Supabase
face_recognition Library
The open-source AI and developer community
