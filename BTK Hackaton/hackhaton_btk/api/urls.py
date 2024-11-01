from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import admin
from api.views import ResultModelViewSet, ExamModelViewSet, DailyReportModelTYTViewSet, DailyReportModelAYTViewSet, UserActivitySuggestionListView,UserModelViewSet, UserActivitySuggestionView
from . import views

router = DefaultRouter()
router.register(r'results', ResultModelViewSet)
router.register(r'exams', ExamModelViewSet)
router.register(r'users', UserModelViewSet)
router.register(r'daily_reports_tyt', DailyReportModelTYTViewSet)
router.register(r'daily_reports_ayt', DailyReportModelAYTViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # API yollarını buraya ekliyoruz
    path('admin/', admin.site.urls),      # Admin paneli
    path('user-suggestion/', UserActivitySuggestionView.as_view(),),
    path('results/', views.ResultsView.as_view()),
    path('user-list/', UserActivitySuggestionListView.as_view(), name='user-suggestion-list'),
]

