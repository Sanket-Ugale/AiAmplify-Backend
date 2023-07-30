import pickle
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from keras.preprocessing import image
from joblib import load
import numpy as np
from PIL import Image

from recognizing_flower.serializers import flowerPredictSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
# Load the trained model
# model = load('model/flower.pkl')
with open("recognizing_flower/model/flower.pkl", 'rb') as file:
    loaded_model = pickle.load(file)
class flowerPredict(APIView):
    def post(self, request):
        serializer = flowerPredictSerializer(data=request.data)
        if serializer.is_valid():
            flower_image = request.data.get("flowerImage")  # Get the uploaded image data

            # Read the image data and resize it to match the expected input shape of the model
            pil_image = Image.open(flower_image)
            pil_image = pil_image.convert('RGB')  # Ensure the image is in RGB format
            pil_image = pil_image.resize((180, 180))  # Resize the image to (180, 180)

            # Convert the resized image to a NumPy array
            x = image.img_to_array(pil_image)
            test_img = np.expand_dims(x, axis=0)

            result = loaded_model.predict(test_img)
            pred = np.argmax(result)
            return Response({"Result": pred})
        else:
            return Response(serializer.errors, status=400)