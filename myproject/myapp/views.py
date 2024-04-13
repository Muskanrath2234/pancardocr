from django.shortcuts import render
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import re
import numpy as np

def extract_information(image):
    # Perform OCR on the image to extract information
    text = pytesseract.image_to_string(image)

    # Define regular expressions for pattern matching
    date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    pan_num_pattern = re.compile(r'Permanent Account Number Card\n.+')
    name_pattern = re.compile(r'Name\n.+')
    father_pattern = re.compile(r"Father's Name\n.+")

    # Search for patterns in the extracted text
    date_match = re.search(date_pattern, text)
    pan_match = re.search(pan_num_pattern, text)
    name_match = re.search(name_pattern, text)
    father_match = re.search(father_pattern, text)

    # Extract the matched information
    date = date_match.group(0) if date_match else None
    pan = pan_match.group(0).split('\n')[-1].strip() if pan_match else None
    name = name_match.group(0).split('\n')[-1].strip() if name_match else None
    father_name = father_match.group(0).split('\n')[-1].strip() if father_match else None

    return date, pan, name, father_name

def upload_pan(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded image
            image = Image.open(request.FILES['image'])

            # Extract information from the image
            date, pan, name, father_name = extract_information(image)

            # Render the result template with extracted information
            return render(request, 'result.html', {'date': date, 'pan': pan, 'name': name, 'father_name': father_name})
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

def result(request):
    return render(request, 'result.html')

# Create your views here.
