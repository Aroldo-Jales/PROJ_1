from datetime import date
from django.db.models import Sum

def days_between_dates(date):
    today = date.today()
    return abs((today-date).days)
