import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import *


# class SalesModel:
#     def __init__(self, fio, total):
#         self.fio = fio
#         self.total = total


# class SalesSerializer(serializers.Serializer):
#     fio = serializers.SlugRelatedField(slug_field='name', queryset=Staff.objects.all())
#     extradition = serializers.IntegerField()
#     ti = serializers.DecimalField(max_digits=5, decimal_places=2)
#     kis = serializers.DecimalField(max_digits=5, decimal_places=2)
#     trener = serializers.DecimalField(max_digits=5, decimal_places=2)
#     client = serializers.DecimalField(max_digits=5, decimal_places=2)
#     total = serializers.DecimalField(max_digits=5, decimal_places=2, default=0.0)
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)




# def encode():
#     model = SalesModel('jora', '99.0')
#     model_sr = SalesSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Angelina Jolie","content":"Content: Angelina Jolie"}')
#     data = JSONParser().parse(stream)
#     serializer = SalesSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)



class SalesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Sales
        fields = '__all__'