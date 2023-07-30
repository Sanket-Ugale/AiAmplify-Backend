from django.contrib import admin
from django.urls import path
from autocorrect import views as autoCorrectView
from twitter_sentiment_analysis import views as twitterView
from recognizing_flower import views as flowerPredictView
urlpatterns = [
    path("admin/", admin.site.urls),
    path("autocorrect/login", autoCorrectView.login_api),
    path("autocorrect/register",autoCorrectView.RegisterUser.as_view()),
    path("autocorrect/verifyOTP",autoCorrectView.verifyOTP.as_view()),
    path("autocorrect/forgotPassword",autoCorrectView.forgotPassword.as_view()),
    path("autocorrect/resetPassword",autoCorrectView.resetPassword.as_view()),
    path("tweetAnalysis/",twitterView.tweetAnalysis.as_view()),
    path("autoCorrect/api",autoCorrectView.autoCorrectApi.as_view()),
    path("flowerPredict/api",flowerPredictView.flowerPredict.as_view()),
]
