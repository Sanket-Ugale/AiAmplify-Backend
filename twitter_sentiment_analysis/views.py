from django.shortcuts import render
import numpy as np
import pandas as pd
from rest_framework.views import APIView
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

from rest_framework.response import Response

from twitter_sentiment_analysis.serializers import tweetAnalysisSerializer


def preprocess_tweet(tweet):
    tweet_words = []
    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)
    return " ".join(tweet_words)

# Create your views here.
class tweetAnalysis(APIView):
    def post(self,request): 
        # print(request.data)
        serializer=tweetAnalysisSerializer(data=request.data)
        serializer.is_valid()
        if True:
            roberta = "cardiffnlp/twitter-roberta-base-sentiment"
            model = AutoModelForSequenceClassification.from_pretrained(roberta)
            tokenizer = AutoTokenizer.from_pretrained(roberta)

            labels = ['Negative', 'Neutral', 'Positive']
            print(request.data)
            # Replace this dictionary with your own containing the number of occurrences of each tweet as keys and the tweet text as values
            tweet_dict = dict(request.data).keys()[0]

            # Initialize counters for positive and negative tweets
            positive_count = 0
            negative_count = 0
            neutral_count = 0

            for item in tweet_dict.values():
                tweet_proc = preprocess_tweet(item)

                # Sentiment analysis
                encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
                output = model(**encoded_tweet)

                scores = output.logits[0].detach().numpy()
                scores = softmax(scores)

                # Find the label with the highest score
                index = scores.argmax()
                sentiment_label = labels[index]

                # Count positive and negative tweets
                if sentiment_label.lower() == "positive":
                    positive_count +=1
                elif sentiment_label.lower() == "negative":
                    negative_count += 1
                elif sentiment_label.lower() == "neutral":
                    neutral_count += 1
            
            # Calculate overall score out of 10
            total_tweets = len(request.data.items())
            if positive_count == total_tweets:
                overall_score = 10.0
            elif negative_count == total_tweets:
                overall_score = 0.0
            else:
                overall_score = (positive_count / total_tweets) * 10

            # Round the overall score to 2 decimal places
            overall_score = round(overall_score, 2)

            return Response({"result":[overall_score, positive_count, negative_count, neutral_count]})