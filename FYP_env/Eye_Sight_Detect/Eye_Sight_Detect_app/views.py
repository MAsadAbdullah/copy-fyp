from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .forms import *
from .models import CustomUser
from PIL import Image
import io
from django.shortcuts import render, redirect
from .forms import PatientForm    
from .models import Patient   
from django.contrib.auth.decorators import login_required   
from .forms import PatientForm
from PIL import Image
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from PIL import Image
import numpy as np
import tensorflow as tf
import os
from django.conf import settings


def landingpage(request):
    return render(request, 'landingpage.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def faqs(request):
    return render(request, 'faqs.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')

@login_required(login_url='login')
def dashboard(request):
    current_doctor = request.user
    # Get the total number of patients
    total_patients = Patient.objects.filter(added_by_id=current_doctor).count()
    total_images = Patient.objects.filter(added_by_id=current_doctor).aggregate(
        total_images=Count('left_eye_fundus_image') + Count('right_eye_fundus_image')
    )['total_images']
    return render(request, 'dashboard.html', {'total_patients': total_patients, 'total_images': total_images})


def patient_personal_data(request):
    current_doctor = request.user
    patients = Patient.objects.filter(added_by_id=current_doctor)
    return render(request, 'patient_personal_data.html', {'patients': patients})


def patient_medical_data(request):
    current_doctor = request.user
    patients = Patient.objects.filter(added_by_id=current_doctor)
    return render(request, 'patient_medical_data.html', {'patients': patients})


def patient_profile(request, patient_id):
    # Assuming you have a 'Patient' model
    patient = get_object_or_404(Patient, id=patient_id)
    context = {
        'patient': patient,
    }
    return render(request, 'patient_profile.html', context)


@login_required(login_url='login')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def register_request(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user after registration
            login(request, user)
            # Redirect to a dashboard or profile page
            return redirect('login')  # Change 'dashboard' to your actual URL name
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def resize_and_convert_image(image, cnic, eye_side):
    img = Image.open(image)
    # Resize the image (you can adjust the size as needed)
    new_size = (224, 224)  # Example size, you can adjust it accordingly
    img_resized = img.resize(new_size)
    img_resized = img_resized.convert("RGB")
    output_buffer = io.BytesIO()
    img_resized.save(output_buffer, format="PNG")
    return output_buffer.getvalue()  # Return the resized image as bytes


def doctor_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                request.session['doctor_id'] = user.id
                # Redirect to a dashboard or profile page
                return redirect('dashboard')
                # Change 'dashboard' to your actual URL name
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.clear() 
    return redirect('landingpage')


@login_required  # This ensures the user is logged in before accessing the view
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        form.set_request(request)
        if form.is_valid():
            patient = form.save(commit=False)  # Do not save to the database yet
            print(request.user)
            patient.added_by_id = request.user
            patient.arival_date_time = timezone.now()
            print(patient.added_by_id)
            # Convert and crop left eye image
            if 'left_eye_fundus_image' in request.FILES:
                left_eye_image = request.FILES['left_eye_fundus_image']
                resized_left_image = resize_and_convert_image(left_eye_image, patient.cnic, 'left')
                patient.left_eye_fundus_image.save(f"{patient.cnic}_left.png", ContentFile(resized_left_image), save=False)
            # Convert and crop right eye image
            if 'right_eye_fundus_image' in request.FILES:
                right_eye_image = request.FILES['right_eye_fundus_image']
                resized_right_image = resize_and_convert_image(right_eye_image, patient.cnic, 'right')
                patient.right_eye_fundus_image.save(f"{patient.cnic}_right.png", ContentFile(resized_right_image), save=False)
            patient.save()  # Now save the patient instance with updated images
            return redirect('results', patient_id=patient.id)
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})



def get_eyesight_predictions(image_bytes):
    # Assuming you have a function to load your deep learning model
    model_path = os.path.join(settings.BASE_DIR, 'eyesightdetact_model.h5')
    model = tf.keras.models.load_model(model_path)  # Update with the actual path or use the DeepLearningModel model to store the path

    # Preprocess the image
    img = Image.open(io.BytesIO(image_bytes))
    # img = img.resize((224, 224))  # Resize to 224x224 as you mentioned
    img_array = np.expand_dims(img, axis=0)
    # img_array = img_array / 255.0  # Normalize the pixel values

    # Add any additional preprocessing steps if needed

    # Make predictions
    prediction = model.predict(img_array)

    # Get the index of the class with the highest probability
    predicted_class_index = np.argmax(prediction.real)

    # Define your class labels
    class_labels = ['Normal', 'Myopia', 'Glaucoma']

    # Get the corresponding class label
    predicted_class_label = class_labels[predicted_class_index]

    # Return the prediction probabilities and the predicted class label
    return  predicted_class_label, 

def results(request, patient_id):
    # Retrieve the patient using the patient_id
    patient = get_object_or_404(Patient, pk=patient_id)

    # Perform predictions for left eye image if available
    if patient.left_eye_fundus_image:
        left_eye_image = patient.left_eye_fundus_image.read()
        left_eye_predictions = get_eyesight_predictions(left_eye_image)  # Replace with your actual function
        print("Left eye pred : ", left_eye_predictions)
        patient.left_eye_result = left_eye_predictions
        patient.save()

    # Perform predictions for right eye image if available
    if patient.right_eye_fundus_image:
        right_eye_image = patient.right_eye_fundus_image.read()
        right_eye_predictions = get_eyesight_predictions(right_eye_image)  # Replace with your actual function
        patient.right_eye_result = right_eye_predictions
        patient.save()

    return render(request, 'results.html', {'patient': patient})