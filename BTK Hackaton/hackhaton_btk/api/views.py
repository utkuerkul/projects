from django.shortcuts import render
from rest_framework import viewsets
from .models import ExamModel, ResultModel, DailyReportModelTYT, DailyReportModelAYT, UserActivitySuggestion, UserModel
from .serializers import ExamModelSerializer, ResultModelSerializer, DailyReportModelTYTSerializer, DailyReportModelAYTSerializer, UserModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequestSerializer
from .utils import call_gemini_api
from django.http import JsonResponse
import google.generativeai as genai

class ResultModelViewSet(viewsets.ModelViewSet):
    queryset = ResultModel.objects.all()
    serializer_class = ResultModelSerializer

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

class ExamModelViewSet(viewsets.ModelViewSet):
    queryset = ExamModel.objects.all()
    serializer_class = ExamModelSerializer

class DailyReportModelTYTViewSet(viewsets.ModelViewSet):
    queryset = DailyReportModelTYT.objects.all()
    serializer_class = DailyReportModelTYTSerializer

class DailyReportModelAYTViewSet(viewsets.ModelViewSet):
    queryset = DailyReportModelAYT.objects.all()
    serializer_class = DailyReportModelAYTSerializer

genai.configure(api_key="AIzaSyBzz-mPuEHIEftIDogexuPLn5gy734ERgU")

# Model yapılandırma
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 5096,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def call_gemini_api(prompt):
    
    response = model.generate_content(prompt)
    return response

class UserActivitySuggestionView(APIView):
    def post(self, request):
        serializer = RequestSerializer(data=request.data)

        # Serializer doğrulaması
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.validated_data
        prompt = (
            f"Kullanıcı Bilgileri:\n"
            f"İsim: {user_data['name']}\n"
            f"Soyisim: {user_data['surname']}\n"
            f"Doğum Tarihi: {user_data['birth_date']}\n"
            f"Sigara Kullanımı: {'Evet' if user_data['usingCigar'] else 'Hayır'}\n"
            f"Alkol Kullanımı: {'Evet' if user_data['usingAlcohol'] else 'Hayır'}\n"
            f"Boy: {user_data['height']} cm\n"
            f"Kilo: {user_data['weight']} kg\n\n"
            "Adım adım düşünme süreci:\n"
            "1. Doğum tarihine göre kullanıcının yaşını ve optimum eğitim durumunu düşün\n"
            "2. Sigara ve alkol kullanımı gibi yaşam tarzı faktörlerinin eğitim durumu açısından etkilerini göz önünde bulundur.\n"
            "3. Boy ve kilo bilgilerini kullanarak BMI (Vücut Kitle İndeksi) hesaplayın ve genel sağlık durumunun eğitim durumuna etkilerini  analiz et\n"
            "4. Yaş, BMI ve yaşam tarzı faktörlerine göre, kullanıcının günlük aktivitelerini özellikle ve özellikle eğitim hayatını iyileştirmeye ve daha başarılı olmasına yönelik kişisel önerilerde bulunun.\n\n"
            "Yukarıdaki faktörleri dikkate alarak bu kullanıcı için eğitim hayatını iyileştirecek ve daha iyi duruma getirecek önerilerde bulun."
        )

        try:
            # API çağrısı
            gemini_response = call_gemini_api(prompt)

            # Öneri metnini alma
            suggestion_text = gemini_response.text
            
            # Kullanıcı önerisini veritabanına kaydetme
            user_suggestion = UserActivitySuggestion.objects.create(
                uid=user_data["uid"],
                name=user_data['name'],
                surname=user_data['surname'],
                usingCigar=user_data['usingCigar'],
                usingAlcohol=user_data['usingAlcohol'],
                height=user_data['height'],
                weight=user_data['weight'],
                birth_date=user_data['birth_date'],  # Bu alanı ekleyin
                suggestion=suggestion_text
            )

            # Yanıt verisi hazırlama
            response_data = {
                "uid": user_suggestion.uid,
                "name": user_suggestion.name,
                "surname": user_suggestion.surname,
                "usingCigar": user_suggestion.usingCigar,
                "usingAlcohol": user_suggestion.usingAlcohol,
                "height": user_suggestion.height,
                "weight": user_suggestion.weight,
                "birth_date": user_suggestion.birth_date,  # Bu alanı ekleyin
                "suggestion": user_suggestion.suggestion
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Bir hata oluştu: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserActivitySuggestionListView(APIView):
    def get(self, request):
        suggestions = UserActivitySuggestion.objects.all()
        data = [
            {
                "uid": suggestion.uid,
                "name": suggestion.name,
                "surname": suggestion.surname,
                "usingCigar": suggestion.usingCigar,
                "usingAlcohol": suggestion.usingAlcohol,
                "height": suggestion.height,
                "weight": suggestion.weight,
                "birth_date":suggestion.birth_date,
                "suggestion": suggestion.suggestion,
            }
            for suggestion in suggestions
        ]
        return Response(data, status=status.HTTP_200_OK)
    
class ResultView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ExamModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)