from flask import Flask, request, jsonify
import numpy as np
import base64
from object_detection import ObjectDetector
import io
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['get'])
def test():
    return jsonify({"id": "success"}), 200
    
@app.route('/api/objects', methods=['POST'])
def upload():
    try:
        # validation
        data = request
        if 'image' not in data.files:
            return jsonify({"error": "'image' is required."}), 400

        # Decode base64 image
        image_file = request.files['image']
        im_bytes = image_file.read()
        im_file = io.BytesIO(im_bytes)  
        img = Image.open(im_file)
        img = np.array(img)
        objectDetector = ObjectDetector()
        
        objects = objectDetector.detectImage(img)
        # Return detected objects
        return jsonify({"objects": objects}), 200
    except Exception as e:
         return jsonify({"error": str(e)}), 500

   



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000, debug=True)
