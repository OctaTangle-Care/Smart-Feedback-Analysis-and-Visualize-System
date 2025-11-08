from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from .models import MainUser, Feedback, ProductCategory, SentimentSummary
from .serializers import *
# from .sentiment import analyze_sentiment  # your sentiment analyzer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q, Count, Avg




from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from jwt import decode as jwt_decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

# def get_mainuser_from_token(request):
#     """
#     Safely extracts MainUser from JWT token in header.
#     Returns None if no/invalid token or user not found.
#     """
#     auth = JWTAuthentication()
#     header = auth.get_header(request)
#     if header is None:
#         return None  # anonymous

#     raw_token = auth.get_raw_token(header)
#     if raw_token is None:
#         return None

#     validated_token = auth.get_validated_token(raw_token)
#     user_id = validated_token.get("user_id")  # because we set USER_ID_CLAIM = user_id

#     from .models import MainUser
#     return MainUser.objects.filter(user_id=user_id).first()

 



def get_mainuser_from_token(request):
    """
    Safely extracts MainUser directly from JWT payload.
    Works even if using custom user model.
    """
    from .models import MainUser

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None  # No token

    token = auth_header.split(" ")[1]
    try:
        # Decode token payload (verify signature)
        payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return None
        return MainUser.objects.filter(user_id=user_id).first()
    except (ExpiredSignatureError, InvalidTokenError, TokenError, KeyError):
        return None




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MainUser, Feedback, ProductCategory
from django.contrib.auth.hashers import make_password, check_password
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # Initialize Sentiment Analyzer
# analyzer = SentimentIntensityAnalyzer()


# def analyze_sentiment(feedback_text):
#     scores = analyzer.polarity_scores(feedback_text)
#     compound = scores['compound']
#     if compound >= 0.05:
#         label = 'positive'
#     elif compound <= -0.05:
#         label = 'negative'
#     else:
#         label = 'neutral'
#     return label, compound



from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(feedback_text, category, rating):
    """
    Analyze sentiment for a given feedback text, with optional category and star rating.
    Returns sentiment label, compound score, and adjusted rating sentiment.
    """

    # Step 1: Base sentiment from feedback text
    scores = analyzer.polarity_scores(feedback_text)
    compound = scores['compound']

    # Step 2: Determine base label
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'

    # Step 3: Adjust compound score slightly based on user rating (if provided)
    if rating:
        try:
            rating = int(rating)
            # Normalize rating (1–5) → (-1 to +1)
            normalized_rating = (rating - 3) / 2  
            compound = (compound + normalized_rating) / 2  
            # Recalculate sentiment label based on adjusted score
            if compound >= 0.05:
                label = 'positive'
            elif compound <= -0.05:
                label = 'negative'
            else:
                label = 'neutral'
        except ValueError:
            pass  # Ignore invalid rating input

    # Step 4: Return structured result
    # result = {
    #     "label": label,
    #     "score": round(compound, 3),
    #     "category": category or "General",
    #     "rating": rating or "N/A",
    # }

    return label, round(compound, 3)
# ✅ 1. REGISTER API
class RegisterAPIView(generics.CreateAPIView):
    queryset = MainUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# # ✅ 2. LOGIN API
# class LoginAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = MainUser.objects.filter(email=email).first()

#         if user and check_password(password, user.password):
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'user': MainUserSerializer(user).data
#             })
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MainUser
from .serializers import MainUserSerializer

# class LoginAPIView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         user = MainUser.objects.filter(email=email).first()
#         if not user or not check_password(password, user.password):
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         # ✅ manually attach user_id so JWT can use it
#         class SimpleUser:
#             def __init__(self, user_id):
#                 self.user_id = user_id

#         pseudo_user = SimpleUser(user.user_id)
#         refresh = RefreshToken.for_user(pseudo_user)

#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": MainUserSerializer(user).data
#         })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MainUser
from .serializers import MainUserSerializer


# class LoginAPIView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         # 1️⃣ Check credentials
#         user = MainUser.objects.filter(email=email).first()
#         if not user or not check_password(password, user.password):
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         # 2️⃣ Create a pseudo object with id attribute (required by JWT)
#         class PseudoUser:
#             def __init__(self, user):
#                 self.id = user.user_id   # 👈 JWT expects this field
#                 self.user_id = user.user_id

#         pseudo_user = PseudoUser(user)

#         # 3️⃣ Generate tokens
#         refresh = RefreshToken.for_user(pseudo_user)

#         # 4️⃣ Add custom claim so we can use user_id later
#         refresh["user_id"] = user.user_id
#         refresh["email"] = user.email
#         refresh["role"] = user.role

#         # 5️⃣ Return tokens + user info
#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": MainUserSerializer(user).data
#         }, status=status.HTTP_200_OK)



import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import MainUser
from .serializers import MainUserSerializer


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 1️⃣ Check credentials
        user = MainUser.objects.filter(email=email).first()
        if not user or not check_password(password, user.password):
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 2️⃣ Create custom payload for JWT
        payload = {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=3),  # Access token expiry (3 hours)
            "iat": datetime.utcnow(),
        }

        # 3️⃣ Encode JWT tokens manually
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        refresh_payload = {
            "user_id": user.user_id,
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7),  # Refresh token expiry (7 days)
            "iat": datetime.utcnow(),
        }
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

        # 4️⃣ Return tokens + user info
        return Response({
            "access": access_token,
            "refresh": refresh_token,
            "user": MainUserSerializer(user).data
        }, status=status.HTTP_200_OK)


# ✅ 3. CATEGORY LIST API
class CategoryListAPIView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]


# # ✅ 4. FEEDBACK LIST + CREATE API
# class FeedbackAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         feedbacks = Feedback.objects.select_related('mainuser', 'category').all().order_by('-created_at')
#         return Response(FeedbackSerializer(feedbacks, many=True).data)
    
#     def post(self, request):
#         feedback_text = request.data.get("feedback_text")
#         category_id = request.data.get("category")
#         rating = request.data.get("rating")

#         category = ProductCategory.objects.filter(pk=category_id).first()
#         sentiment_label, sentiment_score = analyze_sentiment(feedback_text, category, rating)

#         feedback = Feedback.objects.create(
#             mainuser=request.user,
#             feedback_text=feedback_text,
#             category=category,
#             rating=rating,
#             sentiment_label=sentiment_label,
#             sentiment_score=sentiment_score
#         )
#         return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)


# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import MainUser, Feedback, ProductCategory
# from .serializers import FeedbackSerializer
# # from .sentiment import analyze_sentiment

# class FeedbackAPIView(APIView):
#     permission_classes = [AllowAny]  # ✅ anyone can submit

#     def get(self, request):
#         feedbacks = Feedback.objects.select_related('mainuser', 'category').order_by('-created_at')
#         return Response(FeedbackSerializer(feedbacks, many=True).data)

#     def post(self, request):
#         feedback_text = request.data.get("feedback_text")
#         category_id = request.data.get("category")
#         rating = request.data.get("rating")

#         # ✅ Try to map Django's user to MainUser
#         user = None
#         if request.user and request.user.is_authenticated:
#             user = MainUser.objects.filter(email=request.user.email).first()

#         category = ProductCategory.objects.filter(pk=category_id).first() if category_id else None
#         sentiment_label, sentiment_score = analyze_sentiment(feedback_text, category, rating)

#         feedback = Feedback.objects.create(
#             mainuser=user,
#             feedback_text=feedback_text,
#             category=category,
#             rating=rating,
#             sentiment_label=sentiment_label,
#             sentiment_score=sentiment_score
#         )

#         return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)



# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.models import AnonymousUser
# from .models import MainUser, Feedback, ProductCategory
# from .serializers import FeedbackSerializer
# # from .sentiment import analyze_sentiment


# class FeedbackAPIView(APIView):
#     permission_classes = [AllowAny]  # allow both registered and anonymous users

#     def get(self, request):
#         feedbacks = Feedback.objects.select_related('mainuser', 'category').order_by('-created_at')
#         return Response(FeedbackSerializer(feedbacks, many=True).data)

#     def post(self, request):
#         feedback_text = request.data.get("feedback_text")
#         category_id = request.data.get("category")
#         rating = request.data.get("rating")

#         # --- Identify user safely ---
#         # user = None
#         # if not isinstance(request.user, AnonymousUser):
#         #     # If JWT or Django user is present, try to match by email or username
#         #     if hasattr(request.user, "email"):
#         #         user = MainUser.objects.filter(email=request.user.email).first()
#         #     elif hasattr(request.user, "username"):
#         #         user = MainUser.objects.filter(fullname=request.user.username).first()

#         user = None
#         token_user_id = request.data.get("user_id") or request.user.__dict__.get("user_id")

#         if token_user_id:
#             user = MainUser.objects.filter(user_id=token_user_id).first()

#         # --- Get category safely ---
#         category = None
#         if category_id:
#             category = ProductCategory.objects.filter(pk=category_id).first()

#         # --- Analyze sentiment ---
#         sentiment_label, sentiment_score = analyze_sentiment(feedback_text, category, rating)

#         # --- Save feedback ---
#         feedback = Feedback.objects.create(
#             mainuser=user,
#             feedback_text=feedback_text,
#             category=category,
#             rating=rating,
#             sentiment_label=sentiment_label,
#             sentiment_score=sentiment_score,
#         )

#         return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)



from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import MainUser, Feedback, ProductCategory
from .serializers import FeedbackSerializer
# from .sentiment import analyze_sentiment


# class FeedbackAPIView(APIView):
#     permission_classes = [AllowAny]  # allow anyone to submit

#     def get(self, request):
#         feedbacks = Feedback.objects.select_related('mainuser', 'category').order_by('-created_at')
#         return Response(FeedbackSerializer(feedbacks, many=True).data)

#     def post(self, request):
#         feedback_text = request.data.get("feedback_text")
#         category_id = request.data.get("category")
#         rating = request.data.get("rating")

#         # ✅ Safely get MainUser from JWT (if any)
#         user = get_mainuser_from_token(request)

#         # ✅ Get category safely
#         category = ProductCategory.objects.filter(pk=category_id).first() if category_id else None

#         # ✅ Analyze sentiment
#         sentiment_label, sentiment_score = analyze_sentiment(feedback_text, category, rating)

#         # ✅ Save feedback
#         feedback = Feedback.objects.create(
#             mainuser=user,
#             feedback_text=feedback_text,
#             category=category,
#             rating=rating,
#             sentiment_label=sentiment_label,
#             sentiment_score=sentiment_score
#         )

#         return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)

class FeedbackAPIView(APIView):
    authentication_classes = []  # 👈 disables JWT’s default authentication
    permission_classes = [AllowAny]  # allows guests & registered users

    def get_mainuser_from_token(self, request):
        """Decode token manually and get MainUser (if valid)."""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return None
            return MainUser.objects.filter(user_id=user_id).first()
        except (ExpiredSignatureError, InvalidTokenError, KeyError):
            return None

    def get(self, request):
        feedbacks = Feedback.objects.select_related('mainuser', 'category').order_by('-created_at')
        return Response(FeedbackSerializer(feedbacks, many=True).data)

    def post(self, request):
        feedback_text = request.data.get("feedback_text")
        category_id = request.data.get("category")
        rating = request.data.get("rating")

        # ✅ Decode token manually
        user = self.get_mainuser_from_token(request)

        # ✅ Category lookup
        category = ProductCategory.objects.filter(pk=category_id).first() if category_id else None

        # ✅ Sentiment
        sentiment_label, sentiment_score = analyze_sentiment(feedback_text, category, rating)

        # ✅ Save
        feedback = Feedback.objects.create(
            mainuser=user,
            feedback_text=feedback_text,
            category=category,
            rating=rating,
            sentiment_label=sentiment_label,
            sentiment_score=sentiment_score
        )

        return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)

# # ✅ 5. DELETE FEEDBACK
# class DeleteFeedbackAPIView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request, feedback_id):
#         feedback = Feedback.objects.filter(pk=feedback_id, mainuser=request.user).first()
#         if feedback:
#             feedback.delete()
#             return Response({'message': 'Feedback deleted successfully'}, status=200)
#         return Response({'error': 'Feedback not found'}, status=404)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Feedback, MainUser


# class DeleteFeedbackAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]  # ❗ Anonymous users not allowed

#     def delete(self, request, feedback_id):
#         try:
#             # Extract user info from JWT
#             user = None
#             payload_user_id = getattr(request.user, "id", None)
#             if payload_user_id:
#                 user = MainUser.objects.filter(user_id=payload_user_id).first()

#             if not user:
#                 return Response(
#                     {"error": "User not found or unauthorized"},
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )

#             # Get feedback
#             feedback = Feedback.objects.filter(pk=feedback_id).first()
#             if not feedback:
#                 return Response({"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND)

#             # ✅ Admin can delete any feedback
#             if user.role == "admin":
#                 feedback.delete()
#                 return Response({"message": "Feedback deleted by admin successfully"}, status=status.HTTP_200_OK)

#             # ✅ Registered users can only delete their own feedback
#             elif user.role == "registered":
#                 if feedback.mainuser_id == user.user_id:
#                     feedback.delete()
#                     return Response({"message": "Your feedback deleted successfully"}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"error": "You can only delete your own feedback"}, status=status.HTTP_403_FORBIDDEN)

#             # 🚫 Just in case any other role exists
#             else:
#                 return Response({"error": "Not authorized to delete feedback"}, status=status.HTTP_403_FORBIDDEN)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from .models import Feedback, MainUser


class DeleteFeedbackAPIView(APIView):
    """
    Allows:
      - Admins to delete any feedback
      - Registered users to delete their own feedback
      - Blocks anonymous/invalid tokens
    """
    authentication_classes = []  # Disable DRF default JWT auth
    permission_classes = [AllowAny]  # Allow manual token validation

    def get_mainuser_from_token(self, request):
        """Decode JWT manually and get MainUser instance."""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No token found

        token = auth_header.split(" ")[1]
        try:
            payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return None
            return MainUser.objects.filter(user_id=user_id).first()
        except (ExpiredSignatureError, InvalidTokenError, KeyError):
            return None

    def delete(self, request, feedback_id):
        # ✅ Extract user from token
        user = self.get_mainuser_from_token(request)
        if not user:
            return Response(
                {"error": "Unauthorized or invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ✅ Fetch feedback
        feedback = Feedback.objects.filter(pk=feedback_id).first()
        if not feedback:
            return Response(
                {"error": "Feedback not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Admin can delete any feedback
        if user.role == "admin":
            feedback.delete()
            return Response(
                {"message": "Feedback deleted successfully by admin"},
                status=status.HTTP_200_OK
            )

        # ✅ Registered users can delete only their own feedback
        elif user.role == "registered":
            if feedback.mainuser_id == user.user_id:
                feedback.delete()
                return Response(
                    {"message": "Your feedback deleted successfully"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "You can only delete your own feedback"},
                    status=status.HTTP_403_FORBIDDEN
                )

        # 🚫 Any other role or invalid
        return Response(
            {"error": "Not authorized to delete feedback"},
            status=status.HTTP_403_FORBIDDEN
        )



# # ✅ 6. SENTIMENT SUMMARY
# class SentimentSummaryAPIView(generics.RetrieveAPIView):
#     queryset = SentimentSummary.objects.all()
#     serializer_class = SentimentSummarySerializer
#     permission_classes = [permissions.IsAuthenticated]



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from .models import SentimentSummary, MainUser
from .serializers import SentimentSummarySerializer


class SentimentSummaryAPIView(APIView):
    """
    Returns sentiment summary stats.
    Only accessible to registered users or admin (verified via JWT).
    """
    authentication_classes = []  # disable default JWT auth
    permission_classes = [AllowAny]  # we’ll check manually

    def get_mainuser_from_token(self, request):
        """Extract MainUser directly from JWT token payload."""
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]
        try:
            payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return None
            return MainUser.objects.filter(user_id=user_id).first()
        except (ExpiredSignatureError, InvalidTokenError, KeyError):
            return None

    def get(self, request, *args, **kwargs):
        # ✅ Verify user from token
        user = self.get_mainuser_from_token(request)
        if not user:
            return Response(
                {"error": "Unauthorized or invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ✅ Only admins or registered users allowed
        if user.role not in ["admin", "registered"]:
            return Response(
                {"error": "Access denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ Fetch and serialize sentiment summary
        summary = SentimentSummary.objects.first()
        if not summary:
            return Response(
                {"message": "No summary data found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SentimentSummarySerializer(summary)
        return Response(serializer.data, status=status.HTTP_200_OK)

# # ✅ 7. ADMIN ANALYTICS
# class AdminAnalyticsAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         if request.user.role != 'admin':
#             return Response({'error': 'Unauthorized'}, status=403)

#         feedbacks = Feedback.objects.all()
#         total = feedbacks.count()
#         positive = feedbacks.filter(sentiment_label='positive').count()
#         negative = feedbacks.filter(sentiment_label='negative').count()
#         neutral = feedbacks.filter(sentiment_label='neutral').count()

#         category_summary = feedbacks.values('category__category_name').annotate(
#             total=Count('feedback_id'),
#             avg_rating=Avg('rating')
#         ).order_by('-total')

#         data = {
#             "total_feedbacks": total,
#             "positive": positive,
#             "negative": negative,
#             "neutral": neutral,
#             "category_summary": list(category_summary)
#         }
#         return Response(data)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from django.db.models import Count, Avg
from .models import Feedback, MainUser


class AdminAnalyticsAPIView(APIView):
    """
    Admin-only API: Returns analytics summary of all feedback.
    """
    authentication_classes = []  # disable DRF's JWT auth (avoid default User model)
    permission_classes = [AllowAny]  # manual verification via token

    def get_mainuser_from_token(self, request):
        """Decode JWT manually and return MainUser if valid."""
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            payload = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return None
            return MainUser.objects.filter(user_id=user_id).first()
        except (ExpiredSignatureError, InvalidTokenError, KeyError):
            return None

    def get(self, request):
        # ✅ Get admin user from token
        user = self.get_mainuser_from_token(request)
        if not user:
            return Response({"error": "Unauthorized or invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # ✅ Ensure only admin can access
        if user.role != "admin":
            return Response({"error": "Access denied — Admins only"}, status=status.HTTP_403_FORBIDDEN)

        # ✅ Analytics logic
        feedbacks = Feedback.objects.all()
        total = feedbacks.count()
        positive = feedbacks.filter(sentiment_label='positive').count()
        negative = feedbacks.filter(sentiment_label='negative').count()
        neutral = feedbacks.filter(sentiment_label='neutral').count()

        # ✅ Category-wise summary
        category_summary = feedbacks.values('category__category_name').annotate(
            total=Count('feedback_id'),
            avg_rating=Avg('rating')
        ).order_by('-total')

        # ✅ Response
        data = {
            "total_feedbacks": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "category_summary": list(category_summary)
        }
        return Response(data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutAPIView(APIView):
    """
    Stateless logout — client simply discards tokens.
    """

    def post(self, request):
        # You can optionally log activity or audit trail here
        return Response(
            {"message": "Logout successful — please remove tokens on client side"},
            status=status.HTTP_200_OK
        )
