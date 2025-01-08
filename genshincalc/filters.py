import django_filters
from django_filters import CharFilter
from .models import *

class CharacterFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Character
        fields = ['element',
                  'rarity',
                  'weapon_type']