# dashboard/context_processors.py

from .models import Message

def global_message(request):
    try:
        info = Message.objects.get(id=1)
        return {'global_message': info.message}
    except Message.DoesNotExist:
        return {'global_message': ''}
