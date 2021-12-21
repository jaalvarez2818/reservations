from django.views.generic import ListView

from misc.models import RoomTypology
from misc.utils import words


class RoomTypologyListView(ListView):
    template_name = 'room_typology/list.html'
    model = RoomTypology
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': words.ROOM_TYPOLOGIES.capitalize(),
            'content_title': words.ROOM_TYPOLOGIES.capitalize(),
            'content_subtitle': words.LIST.capitalize()
        })
        return context
