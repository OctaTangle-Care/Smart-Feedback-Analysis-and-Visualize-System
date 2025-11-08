# # from django.shortcuts import render




 

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

# # Helper function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import MainUser, Feedback


# ---------- REGISTER ----------
def register(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # This clears existing messages
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if MainUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        hashed_password = make_password(password)
        MainUser.objects.create(
            fullname=fullname,
            email=email,
            password=hashed_password,
            phonenumber=phonenumber,
            role=role
        )
        storage = messages.get_messages(request)
        for _ in storage:
            pass  # This clears existing messages

        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')


# ---------- LOGIN ----------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        storage = messages.get_messages(request)
        for _ in storage:
            pass  # This clears existing messages

        try:
            user = MainUser.objects.get(email=email)
        except MainUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

        if check_password(password, user.password):
            request.session['user_id'] = user.user_id
            request.session['role'] = user.role
            request.session['fullname'] = user.fullname

            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            storage = messages.get_messages(request)
            for _ in storage:
                pass  # This clears existing messages

            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


# ---------- LOGOUT ----------
def logout_view(request):
    request.session.flush()
    # messages.success(request, "You have been logged out.")
    return redirect('home')







from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MainUser, Feedback,  SentimentSummary
# from .sentiment_utils import analyze_sentiment


from django.db.models import F
from .models import Feedback, SentimentSummary

def home(request):
    categories = ProductCategory.objects.all()
    if request.method == "POST":
        category_id = request.POST.get("category")
        rating = request.POST.get("rating")
        feedback_text = request.POST.get("feedback_text")
        category = ProductCategory.objects.filter(category_id=category_id).first() if category_id else None
        # category_id = request.POST.get("category")
        sentiment_label, sentiment_score = analyze_sentiment(feedback_text, category, rating)
        # sentiment_label, sentiment_score = analyze_sentiment(feedback_text)
        # print(f"Sentiment: {sentiment_label}, Score: {sentiment_result}")
        # Anonymous user (no session)
        mainuser = None
        # sentiment_score = float(sentiment_result.get('score', 0.0))
        # sentiment_score = sentiment_result.get('score', 0.0)  # ✅ Safely get the float value
        print(f"Sentiment: {sentiment_label}, Score: {sentiment_score}")
        # Save feedback
        # Feedback.objects.create(
        #     mainuser=mainuser,
        #     feedback_text=feedback_text,
        #     sentiment_label=sentiment_label,
        #     sentiment_score=sentiment_score
        # )
        # sentiment_label, sentiment_score = analyze_sentiment(feedback_text,category, rating)

        Feedback.objects.create(
            mainuser=None,
            feedback_text=feedback_text,
            category=category,
            rating=rating if rating else None,
            sentiment_label=sentiment_label,
            sentiment_score=sentiment_score,
            
        )


        # Update SentimentSummary
        summary, created = SentimentSummary.objects.get_or_create(summary_id=1)

        if sentiment_label == "positive":
            summary.positive_count = F('positive_count') + 1
        elif sentiment_label == "negative":
            summary.negative_count = F('negative_count') + 1
        elif sentiment_label == "neutral":
            summary.neutral_count = F('neutral_count') + 1

        summary.total_feedback = F('total_feedback') + 1
        summary.save()
        summary.refresh_from_db()  # Ensure updated values are loaded

        # messages.success(request, f"Feedback analyzed as {sentiment_label.upper()} ({sentiment_score})")
        return redirect('feedback_success')

    return render(request, 'home.html', {'categories': categories})


from django.db.models import F
from .models import Feedback, SentimentSummary, ProductCategory

def user_dashboard(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # This clears existing messages

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = MainUser.objects.get(pk=user_id)
    user_feedbacks = Feedback.objects.filter(mainuser=user).order_by('-created_at')
    categories = ProductCategory.objects.all()
    
    # Fetch other users' feedbacks
    other_feedbacks = Feedback.objects.exclude(mainuser=user).select_related('mainuser').order_by('-created_at')[:]


    if request.method == "POST":
        feedback_text = request.POST.get("feedback_text")
        category_id = request.POST.get("category")
        rating = request.POST.get("rating")
        
        category = ProductCategory.objects.filter(category_id=category_id).first() if category_id else None
        # print(f"Category selected: {category.category_id if category else 'None'}")
        print(f"Category selected: {category_id} -> {category}")
        # category = ProductCategory.objects.filter(pk=category_id).first() if category_id else None
        # # category = ProductCategory.objects.get(id=category_id) if category_id else None
        # print(f"Category selected: {category.category_id if category else 'None'}")
        sentiment_label, sentiment_score = analyze_sentiment(feedback_text,category, rating)

        Feedback.objects.create(
            mainuser=user,
            feedback_text=feedback_text,
            category=category,
            rating=rating if rating else None,
            sentiment_label=sentiment_label,
            sentiment_score=sentiment_score,
            
        )

        # Update SentimentSummary
        summary, created = SentimentSummary.objects.get_or_create(summary_id=1)

        if sentiment_label == "positive":
            summary.positive_count = F('positive_count') + 1
        elif sentiment_label == "negative":
            summary.negative_count = F('negative_count') + 1
        elif sentiment_label == "neutral":
            summary.neutral_count = F('neutral_count') + 1

        summary.total_feedback = F('total_feedback') + 1
        summary.save()
        summary.refresh_from_db()

        # messages.success(request, f"Feedback analyzed as {sentiment_label.upper()} ({sentiment_score})")
        return redirect('feedback_success')

    return render(request, 'user_dashboard.html', {
        'user': user,
        'user_feedbacks': user_feedbacks,
        'other_feedbacks': other_feedbacks,
        'categories': categories
    })
    
    


def feedback_success(request):
    user_id = request.session.get('user_id')
    if user_id:
        return render(request, 'feedback_success.html', {'next_url': 'user_dashboard'})
    else:
        return render(request, 'feedback_success.html', {'next_url': 'home'})
    
def aboutus(request):
    return render(request, 'aboutus.html')





# from django.shortcuts import render, redirect
# from django.db.models import Q, Count, Avg
# from django.db.models.functions import TruncDate
# from .models import MainUser, Feedback, SentimentSummary
# import re
# from collections import Counter

# def admin_dashboard(request):
#     admin_id = request.session.get('user_id')
#     admin = MainUser.objects.filter(pk=admin_id, role='admin').first()
#     if not admin:
#         return redirect('login')

#     feedbacks = Feedback.objects.all().order_by('created_at')  # ascending for visualization
#     total_feedback = feedbacks.count()
#     positive = feedbacks.filter(sentiment_label='positive').count()
#     negative = feedbacks.filter(sentiment_label='negative').count()
#     neutral = feedbacks.filter(sentiment_label='neutral').count()

#     avg_positive = feedbacks.filter(sentiment_label='positive').aggregate(avg=Avg('sentiment_score'))['avg'] or 0
#     avg_negative = feedbacks.filter(sentiment_label='negative').aggregate(avg=Avg('sentiment_score'))['avg'] or 0
#     avg_neutral = feedbacks.filter(sentiment_label='neutral').aggregate(avg=Avg('sentiment_score'))['avg'] or 0

#     satisfaction_score = ((positive - negative) / total_feedback) * 50 + 50 if total_feedback > 0 else 50

#     # Sentiment trends
#     trends = feedbacks.annotate(date=TruncDate('created_at')).values('date').annotate(
#         positive_count=Count('feedback_id', filter=Q(sentiment_label='positive')),
#         negative_count=Count('feedback_id', filter=Q(sentiment_label='negative')),
#         neutral_count=Count('feedback_id', filter=Q(sentiment_label='neutral'))
#     ).order_by('date')

#     trend_dates = [t['date'].strftime('%Y-%m-%d') for t in trends]
#     positive_trends = [t['positive_count'] for t in trends]
#     negative_trends = [t['negative_count'] for t in trends]
#     neutral_trends = [t['neutral_count'] for t in trends]

#     # Prepare scatter plot data (each point = one feedback)
#     scatter_data = []
#     for i, f in enumerate(feedbacks):
#         sentiment_color = (
#             '#22c55e' if f.sentiment_label == 'positive' else
#             '#ef4444' if f.sentiment_label == 'negative' else
#             '#eab308'
#         )
#         scatter_data.append({
#             'x': i + 1,
#             'y': round(f.sentiment_score or 0, 2),
#             'label': f.sentiment_label.capitalize(),
#             'backgroundColor': sentiment_color,
#         })

#     # Word cloud preparation (optional, from earlier step)
#     all_text = " ".join([f.feedback_text.lower() for f in feedbacks])
#     words = re.findall(r'\b[a-z]{3,}\b', all_text)
#     stopwords = {'the','and','for','you','are','this','that','with','have','was','but','not','from','your','all','has','had','will','can','our','they','what','when','how','why','about','more','been','very'}
#     filtered_words = [w for w in words if w not in stopwords]
#     word_counts = Counter(filtered_words).most_common(30)
#     wordcloud_data = [[word, count] for word, count in word_counts]

#     pie_labels = ['Positive', 'Negative', 'Neutral']
#     pie_data = [positive, negative, neutral]
#     radar_labels = ['Positive', 'Negative', 'Neutral']
#     radar_data = [avg_positive, abs(avg_negative), avg_neutral]

#     summary, _ = SentimentSummary.objects.get_or_create(pk=1)
#     summary.positive_count = positive
#     summary.negative_count = negative
#     summary.neutral_count = neutral
#     summary.total_feedback = total_feedback
#     summary.save()

#     return render(request, 'admin_dashboard.html', {
#         'admin': admin,
#         'feedbacks': feedbacks,
#         'total_feedback': total_feedback,
#         'positive': positive,
#         'negative': negative,
#         'neutral': neutral,
#         'summary': summary,
#         'chart_labels': pie_labels,
#         'chart_data': pie_data,
#         'trend_dates': trend_dates,
#         'positive_trends': positive_trends,
#         'negative_trends': negative_trends,
#         'neutral_trends': neutral_trends,
#         'radar_labels': radar_labels,
#         'radar_data': radar_data,
#         'satisfaction_score': satisfaction_score,
#         'wordcloud_data': wordcloud_data,
#         'scatter_data': scatter_data,  # 👈 NEW data
#     })




from django.shortcuts import render, redirect
from django.db.models import Q, Count, Avg
from django.db.models.functions import TruncDate
from .models import MainUser, Feedback, SentimentSummary, ProductCategory
import re
from collections import Counter

def admin_dashboard(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # This clears existing messages

    admin_id = request.session.get('user_id')
    admin = MainUser.objects.filter(pk=admin_id, role='admin').first()
    if not admin:
        return redirect('login')

    feedbacks = Feedback.objects.select_related('category').all().order_by('created_at')
    total_feedback = feedbacks.count()
    positive = feedbacks.filter(sentiment_label='positive').count()
    negative = feedbacks.filter(sentiment_label='negative').count()
    neutral = feedbacks.filter(sentiment_label='neutral').count()

    avg_positive = feedbacks.filter(sentiment_label='positive').aggregate(avg=Avg('sentiment_score'))['avg'] or 0
    avg_negative = feedbacks.filter(sentiment_label='negative').aggregate(avg=Avg('sentiment_score'))['avg'] or 0
    avg_neutral = feedbacks.filter(sentiment_label='neutral').aggregate(avg=Avg('sentiment_score'))['avg'] or 0

    satisfaction_score = ((positive - negative) / total_feedback) * 50 + 50 if total_feedback > 0 else 50

    # 📈 Sentiment trends over time
    trends = feedbacks.annotate(date=TruncDate('created_at')).values('date').annotate(
        positive_count=Count('feedback_id', filter=Q(sentiment_label='positive')),
        negative_count=Count('feedback_id', filter=Q(sentiment_label='negative')),
        neutral_count=Count('feedback_id', filter=Q(sentiment_label='neutral'))
    ).order_by('date')

    trend_dates = [t['date'].strftime('%Y-%m-%d') for t in trends]
    positive_trends = [t['positive_count'] for t in trends]
    negative_trends = [t['negative_count'] for t in trends]
    neutral_trends = [t['neutral_count'] for t in trends]

    # 🟢 Scatter plot
    scatter_data = []
    for i, f in enumerate(feedbacks):
        color = (
            '#22c55e' if f.sentiment_label == 'positive' else
            '#ef4444' if f.sentiment_label == 'negative' else
            '#eab308'
        )
        scatter_data.append({
            'x': i + 1,
            'y': round(f.sentiment_score or 0, 2),
            'label': f.sentiment_label.capitalize(),
            'backgroundColor': color,
        })

    # ☁️ Word cloud
    all_text = " ".join([f.feedback_text.lower() for f in feedbacks])
    words = re.findall(r'\b[a-z]{3,}\b', all_text)
    stopwords = {'the','and','for','you','are','this','that','with','have','was','but','not','from','your','all','has','had','will','can','our','they','what','when','how','why','about','more','been','very'}
    filtered_words = [w for w in words if w not in stopwords]
    word_counts = Counter(filtered_words).most_common(30)
    wordcloud_data = [[word, count] for word, count in word_counts]

    # 🧩 Category-wise sentiment and ratings
    category_stats = (
        feedbacks.values('category__category_name')
        .annotate(
            avg_rating=Avg('rating'),
            positive=Count('feedback_id', filter=Q(sentiment_label='positive')),
            negative=Count('feedback_id', filter=Q(sentiment_label='negative')),
            neutral=Count('feedback_id', filter=Q(sentiment_label='neutral')),
            total=Count('feedback_id')
        )
        .order_by('category__category_name')
    )

    category_labels = [c['category__category_name'] or 'Uncategorized' for c in category_stats]
    avg_ratings = [round(c['avg_rating'] or 0, 2) for c in category_stats]
    cat_pos = [c['positive'] for c in category_stats]
    cat_neg = [c['negative'] for c in category_stats]
    cat_neu = [c['neutral'] for c in category_stats]

    # 🧠 Sentiment summary update
    summary, _ = SentimentSummary.objects.get_or_create(pk=1)
    summary.positive_count = positive
    summary.negative_count = negative
    summary.neutral_count = neutral
    summary.total_feedback = total_feedback
    summary.save()

    # 📊 Return context
    return render(request, 'admin_dashboard.html', {
        'admin': admin,
        'feedbacks': feedbacks,
        'total_feedback': total_feedback,
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'summary': summary,
        'chart_labels': ['Positive', 'Negative', 'Neutral'],
        'chart_data': [positive, negative, neutral],
        'trend_dates': trend_dates,
        'positive_trends': positive_trends,
        'negative_trends': negative_trends,
        'neutral_trends': neutral_trends,
        'radar_labels': ['Positive', 'Negative', 'Neutral'],
        'radar_data': [avg_positive, abs(avg_negative), avg_neutral],
        'satisfaction_score': satisfaction_score,
        'wordcloud_data': wordcloud_data,
        'scatter_data': scatter_data,
        # new category/rating data
        'category_labels': category_labels,
        'avg_ratings': avg_ratings,
        'cat_pos': cat_pos,
        'cat_neg': cat_neg,
        'cat_neu': cat_neu,
    })





import csv
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import datetime
from .models import Feedback

def download_feedbacks(request, file_format):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    feedbacks = Feedback.objects.all().order_by('-created_at')

    # Filter by date range if provided
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            feedbacks = feedbacks.filter(created_at__date__range=[start, end])
        except ValueError:
            return HttpResponse("Invalid date format. Please use YYYY-MM-DD.", status=400)
    elif start_date:
        feedbacks = feedbacks.filter(created_at__date__gte=start_date)
    elif end_date:
        feedbacks = feedbacks.filter(created_at__date__lte=end_date)

    if not feedbacks.exists():
        return HttpResponse("No feedbacks found for the selected date range.", status=404)

    # -------------------------------
    # CASE 1: CSV Export
    # -------------------------------
    if file_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        filename = f"feedbacks_{start_date or 'all'}_to_{end_date or 'all'}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(['Feedback ID', 'User Name', 'Email', 'Feedback Text', 'Sentiment Label', 'Sentiment Score', 'Date'])

        for f in feedbacks:
            writer.writerow([
                f.feedback_id,
                f.mainuser.fullname if f.mainuser else 'Guest',
                f.mainuser.email if f.mainuser else 'N/A',
                f.feedback_text,
                f.sentiment_label,
                round(f.sentiment_score or 0, 2),
                f.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ])
        return response

    # -------------------------------
    # CASE 2: Excel Export
    # -------------------------------
    elif file_format == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = f"feedbacks_{start_date or 'all'}_to_{end_date or 'all'}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        wb = Workbook()
        ws = wb.active
        ws.title = "Feedback Data"

        headers = ['Feedback ID', 'User Name', 'Email', 'Feedback Text', 'Sentiment Label', 'Sentiment Score', 'Date']
        ws.append(headers)

        for f in feedbacks:
            ws.append([
                f.feedback_id,
                f.mainuser.fullname if f.mainuser else 'Guest',
                f.mainuser.email if f.mainuser else 'N/A',
                f.feedback_text,
                f.sentiment_label,
                round(f.sentiment_score or 0, 2),
                f.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ])

        # Auto-fit column widths
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            ws.column_dimensions[column].width = max_length + 2

        wb.save(response)
        return response

    else:
        return HttpResponse("Invalid file format. Use 'csv' or 'xlsx'.", status=400)



from django.contrib import messages

from django.core.mail import send_mail
from .models import MainUser, Feedback

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Email configuration (replace with your admin email)
        admin_email = 'admin@example.com'  # Update this with the actual admin email
        subject = f'New Contact Message from {name}'
        body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        from_email = email
        
        try:
            send_mail(
                subject,
                body,
                from_email,
                [admin_email],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'Failed to send your message. Please try again later.')
    
    return render(request, 'contact_us.html')



def privacy_policy(request):
    return render(request, 'privacy_policy.html')




from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Feedback, SentimentSummary

def delete_feedback(request, feedback_id):
    user_id = request.session.get('user_id')
    user = MainUser.objects.get(pk=user_id)
    feedback = get_object_or_404(Feedback, feedback_id=feedback_id)

    # Update sentiment summary before deletion
    try:
        summary = SentimentSummary.objects.first()
        if summary:
            if feedback.sentiment_label == 'positive':
                summary.positive_count = max(0, summary.positive_count - 1)
            elif feedback.sentiment_label == 'negative':
                summary.negative_count = max(0, summary.negative_count - 1)
            elif feedback.sentiment_label == 'neutral':
                summary.neutral_count = max(0, summary.neutral_count - 1)
            summary.total_feedback = max(0, summary.total_feedback - 1)
            summary.save()
    except SentimentSummary.DoesNotExist:
        pass  # Optional: log or handle missing summary

    feedback.delete()

    # Send only success message and redirect
    messages.success(request, "Feedback deleted successfully.")
    if user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')
    # return redirect('feedback_list')  # Replace with your actual URL name
    
    
    


    # return redirect('dashboard ')

def dashboard(request):
    role = request.session.get('role')
    if role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')