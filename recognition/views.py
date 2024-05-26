from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from deepface import DeepFace
from django.core.files.storage import FileSystemStorage
import os 
import logging

logger = logging.getLogger(__name__)

def handle_uploaded_image(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)
    absolute_file_path = os.path.join(settings.MEDIA_ROOT, filename)
    logger.info(f"Uploaded file URL: {uploaded_file_url}")
    logger.info(f"Absolute file path: {absolute_file_path}")
    return uploaded_file_url, absolute_file_path

def recognize_image(image_path):
    logger.info(f"Recognizing image at path: {image_path}")
    analysis = DeepFace.analyze(img_path=image_path, actions=['gender', 'emotion'])
    gender = analysis[0].get('dominant_gender')
    emotion = analysis[0].get('dominant_emotion')
    return gender, emotion


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            uploaded_file_url, absolute_file_path = handle_uploaded_image(request.FILES['image'])
            gender, emotion = recognize_image(absolute_file_path)
            if gender == 'Man':
                message = f"Sir, you are {emotion}."
            else:
                message = f"Ma'am, you are {emotion}."
            return render(request, 'recognition/result.html', {'message': message, 'image_url': uploaded_file_url})
    else:
        form = ImageUploadForm()
    return render(request, 'recognition/upload.html', {'form': form})


def result(request):
    # Assume result is passed via session or another method
    message = request.GET.get('message')
    image_url = request.GET.get('image_url')
    return render(request, 'recognition/result.html', {'message': message, 'image_url': image_url})