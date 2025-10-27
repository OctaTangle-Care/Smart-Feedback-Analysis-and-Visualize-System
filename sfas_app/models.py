from django.db import models

# Create your models here.
from django.db import models

class MainUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)  # Store hashed password
    phonenumber = models.CharField(max_length=10, null=True)  # Optional, e.g., "+1234567890"
    role = models.CharField(
        max_length=10,
        choices=[('registered', 'registered'), ('admin', 'admin')],
        default='registered',
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.fullname
    
    


# -------------------------------------------------------
#  PRODUCT CATEGORY MODEL
# -------------------------------------------------------
class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.category_name


# -------------------------------------------------------
#  FEEDBACK MODEL
# -------------------------------------------------------
class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    feedback_id = models.AutoField(primary_key=True)
    mainuser = models.ForeignKey(MainUser, on_delete=models.SET_NULL, null=True)  # Null for guests
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)  # e.g., Laptop, Toys
    feedback_text = models.TextField(null=False)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)  # Star rating (1-5)
    sentiment_label = models.CharField(max_length=10, null=True)  # e.g., 'positive', 'negative', 'neutral'
    sentiment_score = models.FloatField(null=True)  # e.g., -1 to 1
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    

    def __str__(self):
        return self.feedback_text[:50] + "..." if len(self.feedback_text) > 50 else self.feedback_text



class SentimentSummary(models.Model):
    summary_id = models.AutoField(primary_key=True)
    positive_count = models.IntegerField(default=0, null=False)
    negative_count = models.IntegerField(default=0, null=False)
    neutral_count = models.IntegerField(default=0, null=False)
    total_feedback = models.IntegerField(default=0, null=False)
    last_updated = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return f"Summary (Total: {self.total_feedback})"