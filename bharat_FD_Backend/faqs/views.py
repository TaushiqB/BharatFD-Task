# faqs/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'en')
        return context

    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        cache_key = f'faqs_list_{lang}'
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # If not in cache, get from DB
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=86400)  # Cache for 24 hours
        
        return Response(serializer.data)
    
@ratelimit(key='ip', rate='100.minute', method='GET', block=True)
def get_faqs(request):
    return JsonResponse({"message": "Success"})