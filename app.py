import os
import datetime
import cv2
from flask import Flask, jsonify, request, render_template

# để chạy chương trình cần cài đặt các thư viện flask, face_recognition
# pip install flask face_recognition
import face_recognition

app = Flask(__name__)

# tạo biến để ghi dữ liệu
registered_data = {}

# trang chủ
@app.route("/")
def index():
    return render_template("index.html")

#phương thức đăng ký
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name") #biến lưu tên user
    photo = request.files['photo'] #biến lưu trữ hình ảnh
    
    #truy cập vào folder uploads nếu không có sẽ tạo folder uploads
    uploads_folder = os.path.join(os.getcwd(), "static", "uploads")
    
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
  
    #lưu hình ảnh vào folder uploads      
    photo.save(os.path.join(uploads_folder, f'{datetime.date.today()}_{name}.jpg'))
    
    #lưu dữ liệu vào mảng register
    registered_data[name] = f"{datetime.date.today()}_{name}.jpg"
    
    # nếu tất cả thành công thì sẽ refesh trang login
    response = {"success": True, 'name': name}
    return jsonify(response)

# phương thức đăng nhập
@app.route("/login", methods=["POST"])
def login():
    photo = request.files['photo']
    
    # Lưu hình ảnh login vào folder uploads
    uploads_folder = os.path.join(os.getcwd(), "static", "uploads")
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
        
    login_filename = os.path.join(uploads_folder, "login_face.jpg")
    
    photo.save(login_filename)
    
    # kiểm tra có phát hiện mặt hay không
    login_image = cv2.imread(login_filename)
    gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)
    
    face_casade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_casade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    
    # nếu không thấy mặt trong camera
    if len(faces) == 0:
        response = {"success": False}
        return jsonify(response)
    
    login_image = face_recognition.load_image_file(login_filename)
    
    # nếu tìm thấy hình ảnh trong folder uploads gần giống với hình ảnh trong camera
    login_face_encodings = face_recognition.face_encodings(login_image)
    
    # nếu không tìm thấy hình ảnh tương ứng
    for name,filename in registered_data.items():
        registered_photo = os .path.join(uploads_folder,filename)
        registered_image = face_recognition.load_image_file(registered_photo)
        
        registered_face_encodings = face_recognition.face_encodings(registered_image)
        # so sánh ảnh đăng ký và ảnh đăng nhập
        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0 :
            matches = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])
            
            print("matches", matches)
            if any(matches):
                response = {"success": True, "name": name}
                return jsonify(response)
            
    response = {"success": False}
    return jsonify(response)

# chuyển tới trang home nếu login thành công
@app.route("/success")
def success():
    user_name = request.args.get("user_name")
    return render_template("home.html", user_name=user_name)

if __name__ == "__main__":
    app.run(debug=True)