from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category, Information, ShortTermMemory, LongTermMemory
from .serializers import (
    CategorySerializer,
    InformationSerializer,
    ShortTermMemorySerializer,
    LongTermMemorySerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        category = self.get_object()
        subcats = Category.objects.filter(parent=category)
        serializer = self.get_serializer(subcats, many=True)
        return Response(serializer.data)

class InformationViewSet(viewsets.ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        information = self.get_object()
        information.verification_status = True
        information.save()
        return Response({'status': 'verification updated'})

    @action(detail=True, methods=['get'])
    def access(self, request, pk=None):
        information = self.get_object()
        information.access()
        return Response({'status': 'access recorded'})

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', None)
        
        queryset = self.queryset
        if query:
            queryset = queryset.filter(title__icontains=query) | queryset.filter(content__icontains=query)
        if category:
            queryset = queryset.filter(categories__id=category)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ShortTermMemoryViewSet(viewsets.ModelViewSet):
    queryset = ShortTermMemory.objects.all()
    serializer_class = ShortTermMemorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def update_comprehension(self, request, pk=None):
        memory = self.get_object()
        new_level = float(request.data.get('comprehension_level', memory.comprehension_level))
        memory.comprehension_level = max(0.0, min(1.0, new_level))
        memory.last_reviewed = timezone.now()
        memory.save()
        return Response({'status': 'comprehension updated'})

    @action(detail=False, methods=['get'])
    def priority_queue(self, request):
        memories = self.queryset.order_by('-priority_level', 'last_reviewed')
        serializer = self.get_serializer(memories, many=True)
        return Response(serializer.data)

class LongTermMemoryViewSet(viewsets.ModelViewSet):
    queryset = LongTermMemory.objects.all()
    serializer_class = LongTermMemorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def reinforce(self, request, pk=None):
        memory = self.get_object()
        memory.reinforce()
        return Response({'status': 'memory reinforced'})

    @action(detail=True, methods=['post'])
    def update_mastery(self, request, pk=None):
        memory = self.get_object()
        new_level = float(request.data.get('mastery_level', memory.mastery_level))
        memory.mastery_level = max(0.0, min(1.0, new_level))
        memory.save()
        return Response({'status': 'mastery updated'})

    @action(detail=False, methods=['get'])
    def get_by_confidence(self, request):
        min_confidence = float(request.query_params.get('min_confidence', 0.0))
        memories = self.queryset.filter(confidence_score__gte=min_confidence)
        serializer = self.get_serializer(memories, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@csrf_exempt
def learn_information(request):
    """
    Endpoint to process new information and create appropriate memory entries
    """
    try:
        # Create Information entry
        info_serializer = InformationSerializer(data=request.data)
        if info_serializer.is_valid():
            information = info_serializer.save()
            
            # Create ShortTermMemory
            stm_data = {
                'information': information.id,
                'relevance_score': request.data.get('relevance_score', 0.5),
                'context': request.data.get('context', ''),
                'priority_level': request.data.get('priority_level', 5)
            }
            stm_serializer = ShortTermMemorySerializer(data=stm_data)
            if stm_serializer.is_valid():
                stm_serializer.save()
            
            # Create LongTermMemory if confidence is high enough
            if request.data.get('confidence_score', 0) >= 0.7:
                ltm_data = {
                    'information': information.id,
                    'importance': request.data.get('importance', 5),
                    'confidence_score': request.data.get('confidence_score', 0.7)
                }
                ltm_serializer = LongTermMemorySerializer(data=ltm_data)
                if ltm_serializer.is_valid():
                    ltm_serializer.save()
            
            return Response({
                'status': 'success',
                'message': 'Information processed and stored in memory'
            }, status=status.HTTP_201_CREATED)
        
        return Response(info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@csrf_exempt
def consolidate_memory(request, stm_id):
    """
    Endpoint to convert short-term memory to long-term memory
    """
    try:
        stm = get_object_or_404(ShortTermMemory, pk=stm_id)
        
        # Create LongTermMemory
        ltm_data = {
            'information': stm.information.id,
            'importance': request.data.get('importance', 5),
            'confidence_score': request.data.get('confidence_score', 0.7),
            'associations': request.data.get('associations', {})
        }
        
        ltm_serializer = LongTermMemorySerializer(data=ltm_data)
        if ltm_serializer.is_valid():
            ltm_serializer.save()
            stm.delete()  # Remove from short-term memory
            
            return Response({
                'status': 'success',
                'message': 'Memory consolidated to long-term storage'
            })
            
        return Response(ltm_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
