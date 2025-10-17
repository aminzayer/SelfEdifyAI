from .models import Information, ShortTermMemory, LongTermMemory
from .serializers import InformationSerializer, ShortTermMemorySerializer, LongTermMemorySerializer

class MemoryService:
    def learn_information(self, data):
        info_serializer = InformationSerializer(data=data)
        if info_serializer.is_valid():
            information = info_serializer.save()

            stm_data = {
                'information': information.id,
                'relevance_score': data.get('relevance_score', 0.5),
                'context': data.get('context', ''),
                'priority_level': data.get('priority_level', 5)
            }
            stm_serializer = ShortTermMemorySerializer(data=stm_data)
            if stm_serializer.is_valid():
                stm_serializer.save()

            if data.get('confidence_score', 0) >= 0.7:
                ltm_data = {
                    'information': information.id,
                    'importance': data.get('importance', 5),
                    'confidence_score': data.get('confidence_score', 0.7)
                }
                ltm_serializer = LongTermMemorySerializer(data=ltm_data)
                if ltm_serializer.is_valid():
                    ltm_serializer.save()

            return {'status': 'success', 'message': 'Information processed and stored in memory'}, 201

        return {'status': 'error', 'errors': info_serializer.errors}, 400

    def consolidate_memory(self, stm_id, data):
        try:
            stm = ShortTermMemory.objects.get(pk=stm_id)

            ltm_data = {
                'information': stm.information.id,
                'importance': data.get('importance', 5),
                'confidence_score': data.get('confidence_score', 0.7),
                'associations': data.get('associations', {})
            }

            ltm_serializer = LongTermMemorySerializer(data=ltm_data)
            if ltm_serializer.is_valid():
                ltm_serializer.save()
                stm.delete()

                return {'status': 'success', 'message': 'Memory consolidated to long-term storage'}, 200

            return {'status': 'error', 'errors': ltm_serializer.errors}, 400

        except ShortTermMemory.DoesNotExist:
            return {'status': 'error', 'message': 'ShortTermMemory not found'}, 404