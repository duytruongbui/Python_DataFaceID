# Face Identification System
## Requirements
- python 3.7+
## Installation
```
pip install -r requirements.txt
```
## Model weights:
- Detector [link](https://drive.google.com/drive/folders/1jULDZCfUWC_jDzZYz4bw3InirKeewbBS?usp=sharing): download and put into ```core/face_detector```
- Put image frames into ```database/data```
```
 ___database
 |___data
    |__ name1
    | |__ img1.jpg
    | |__ img2.jpg
    |__ name2
    |  |__ img1.jpg
    |  |__ img2.jpg
    ...
```
## Getting Started
```
python main.py -v -s --src video.mp4 -c
```

  - ```-v```: if input is video or stream
  - ```-s```: if you wanna show on screen
  - ```--src```: source to image/video file or stream
  - ```-c```: if you wanna include gallery computing step into the pipeline
