import django_filters
from django_filters import DateFilter,CharFilter
from .models import Trasaction

class TrnFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date',lookup_expr="gte")
    end_date = DateFilter(field_name="date",lookup_expr="lte")
    name = CharFilter(field_name="name",lookup_expr="icontains")
    class Meta:
        model = Trasaction
        fields = "__all__"
        exclude =['date','profile ']
