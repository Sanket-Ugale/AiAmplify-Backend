import json
import pickle
from django.shortcuts import render
import json
import joblib
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from difflib import get_close_matches
import numpy as np
from autocorrect.serializers import *
from django.contrib.auth import get_user_model

# from autocorrect.task import sendEmailTask, sendForgotEmailTask

User=get_user_model()

with open("D:/Python Projects/Django Projects/AiAmplify Backend/AiAmplify/aiamplify/autocorrect/model/trained_model.pkl", 'rb') as file:
    loaded_model = pickle.load(file)
vectorizer=joblib.load("D:/Python Projects/Django Projects/AiAmplify Backend/AiAmplify/aiamplify/autocorrect/model/vectorizer.joblib")
data = pd.read_csv("D:/Python Projects/Django Projects/AiAmplify Backend/AiAmplify/aiamplify/autocorrect/model/dataset.csv")
corrected_words = data["Correct"].tolist()

def autocorrect(input_word, correct_words, model, vectorizer, max_suggestions=2):
        input_word_vectorized = vectorizer.transform(np.array([input_word]))  # Reshape to 2D array
        if not input_word_vectorized.getnnz():
            return input_word, ["No suggestions available."]

        input_word_str = vectorizer.inverse_transform(input_word_vectorized)[0][0]  # Convert back to string
        input_word_lower = input_word_str.lower()

        if input_word_lower in [word.lower() for word in correct_words]:
            return input_word_str, ["Word is already correct."]

        # Get close matches based on edit distance with the correct words
        close_matches = get_close_matches(input_word_lower, [word.lower() for word in correct_words], n=max_suggestions, cutoff=0.75)

        if not close_matches:
            # If no close matches found, use the SVM model to autocorrect the word
            corrected_word = model.predict(input_word_vectorized)[0]
            return input_word_str, [corrected_word]

        return input_word_str, close_matches
# Create your views here.
class autoCorrectApi(APIView):
    def post(self,request):
        # print(request.data['str'])
        serializer=autoCorrectSerializer(data=request.data)
        serializer.is_valid()
        if True:
            str = json.loads(next(iter(dict(request.data))))['str']
            print(str)
            # str=serializer.data['str']
            # Model call
            res = []
            for word in str.split(' '):
                word = word.lower()
                result, s = autocorrect(word, corrected_words, loaded_model, vectorizer)
                res.append({word : s})
            return Response({"Output":res})
        else:
            return Response({"Output":serializer.errors})
