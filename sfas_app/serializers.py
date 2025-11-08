from rest_framework import serializers
from .models import MainUser, Feedback, ProductCategory, SentimentSummary

class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['user_id', 'fullname', 'email', 'phonenumber', 'role', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['fullname', 'email', 'password', 'phonenumber']

    def create(self, validated_data):
        from django.contrib.auth.hashers import make_password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    mainuser = MainUserSerializer(read_only=True)
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'

class SentimentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentSummary
        fields = '__all__'
