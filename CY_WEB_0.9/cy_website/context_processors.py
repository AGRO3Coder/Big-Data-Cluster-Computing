# your_project/context_processors.py
from django.conf import settings

def asset_root(request):
    return {
        'config': {
            'ASSETS_ROOT': settings.ASSETS_ROOT
        }
    }
