# Face Beauty

> Face beauty assessment app — upload a face image and get an AI-powered beauty score using Roboflow model inference.

## What it does

Runs face images through a custom-trained Roboflow model to detect facial features and produce a beauty assessment score.

**Features:**
- Face image upload (Flask web UI)
- Roboflow model inference (face_beauty_new v1)
- Prediction visualisation with bounding boxes
- Confidence threshold: 30%

## Tech Stack

Flask · Roboflow API · OpenCV · Python

## Getting Started

```bash
git clone https://github.com/vineetkukreti/facebeauty.git
cd facebeauty

pip install -r requirements.txt

# Add your Roboflow API key
export ROBOFLOW_API_KEY=your_key

python app.py
# Open http://localhost:5000
```

## Usage

1. Open the web app
2. Upload a face image
3. View the beauty assessment prediction and confidence score
