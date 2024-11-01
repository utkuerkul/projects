from django.contrib import admin
from .models import ExamModel, ResultModel, DailyReportModelAYT, DailyReportModelTYT
from .models import APICall

admin.site.register(ExamModel)
admin.site.register(ResultModel)
admin.site.register(DailyReportModelAYT)
admin.site.register(DailyReportModelTYT)
admin.site.register(APICall)