from django.db import models

class ResultModel(models.Model):
    field = models.CharField(max_length=100)
    true_answers = models.IntegerField()
    false_answers = models.IntegerField()
    clear_answers = models.FloatField()

    def __str__(self):
        return f"{self.field} - True: {self.true_answers}, False: {self.false_answers}, Clear: {self.clear_answers}"


class ExamModel(models.Model):
    exam_type = models.CharField(max_length=100)
    date = models.DateField()
    result_list = models.ManyToManyField(ResultModel, related_name='exams')

    def __str__(self):
        return f"{self.exam_type} on {self.date}"


class DailyReportModelTYT(models.Model):
    date = models.DateField()
    daily_list = models.ManyToManyField(ResultModel, related_name='daily_reports_tyt')

    def __str__(self):
        return f"TYT Report on {self.date}"


class DailyReportModelAYT(models.Model):
    date = models.DateField()
    daily_list = models.ManyToManyField(ResultModel, related_name='daily_reports_ayt')

    def __str__(self):
        return f"AYT Report on {self.date}"
    

class APICall(models.Model):
    prompt = models.TextField()  # Gönderilen istek
    response = models.TextField()  # Alınan yanıt
    timestamp = models.DateTimeField(auto_now_add=True)  # İsteğin yapıldığı zaman

    def __str__(self):
        return f"API Call at {self.timestamp}"
    
class UserModel(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birth_date = models.DateField()
    field = models.CharField(max_length=255)

    # İlişkiler için ForeignKey kullan
    daily_report_list_tyt = models.ManyToManyField(DailyReportModelTYT, related_name='users', blank=True)
    daily_report_list_ayt = models.ManyToManyField(DailyReportModelAYT, related_name='users', blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

class UserActivitySuggestion(models.Model):
    uid = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    usingCigar = models.BooleanField()
    usingAlcohol = models.BooleanField()
    height = models.FloatField()
    weight = models.FloatField()
    birth_date = models.DateTimeField()
    suggestion = models.TextField()

    def __str__(self):
        return f"{self.name} {self.surname} - Suggestion: {self.suggestion}"