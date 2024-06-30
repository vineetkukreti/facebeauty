from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from roboflow import Roboflow

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PREDICTION_FOLDER'] = 'static/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Initialize Roboflow
rf = Roboflow(api_key="MWKwtodgqS8xtJC2REzI")
project = rf.workspace().project("face_beauty_new")
model = project.version("1").model

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file)
            print(filename)
            print(file_path)






            
            file.save(file_path)
            
            # Process the image using Roboflow model
            result = model.predict(file_path, confidence=40).json()
            print(result)
            prediction_image_path = os.path.join(app.config['PREDICTION_FOLDER'], 'prediction.jpg')
            model.predict(file_path, confidence=40).save(prediction_image_path)
            
            # Calculate the areas and percentages
            image_width = 640
            image_height = 640
            data = result
            class_areas = {}
            for item in data['predictions']:
                class_name = item['class']
                area = item['width'] * item['height']
                if class_name in class_areas:
                    class_areas[class_name] += area
                else:
                    class_areas[class_name] = area
            
            total_face_area = image_width * image_height
            results = {}
            for class_name, area in class_areas.items():
                percentage_affected = (area / total_face_area) * 100
                results[class_name] = percentage_affected
            
            return render_template('result.html', results=results, filename= filename,result=result)
    
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
