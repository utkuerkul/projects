# serializers.py

from rest_framework import serializers
from .models import UserModel, ExamModel, ResultModel, DailyReportModelTYT, DailyReportModelAYT, UserActivitySuggestion

class ResultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultModel
        fields = '__all__'  # Tüm alanları dahil etmek için '__all__' kullanıyoruz

class ExamModelSerializer(serializers.ModelSerializer):
    result_list = ResultModelSerializer(many=True)  # İlişkili result listesi

    class Meta:
        model = ExamModel
        fields = '__all__'

class DailyReportModelTYTSerializer(serializers.ModelSerializer):
    daily_list = ResultModelSerializer(many=True)

    class Meta:
        model = DailyReportModelTYT
        fields = '__all__'

class DailyReportModelAYTSerializer(serializers.ModelSerializer):
    daily_list = ResultModelSerializer(many=True)

    class Meta:
        model = DailyReportModelAYT
        fields = '__all__'

class UserModelSerializer(serializers.ModelSerializer):
    daily_report_list_tyt = DailyReportModelTYTSerializer(many=True, read_only=True)
    daily_report_list_ayt = DailyReportModelAYTSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = [
            'uid', 
            'name', 
            'surname', 
            'birth_date', 
            'field', 
            'daily_report_list_tyt', 
            'daily_report_list_ayt'
        ]
class UserActivitySuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivitySuggestion
        fields = '__all__'

class RequestSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    usingCigar = serializers.BooleanField()
    usingAlcohol = serializers.BooleanField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
    birth_date = serializers.DateTimeField()