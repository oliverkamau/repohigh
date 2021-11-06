from rest_framework import serializers
from .models import StudentDef
from .models import Select2Data

class StudentSerializer(serializers.Serializer):

        def update(self, instance, validated_data):
            pass

        def create(self, validated_data):
            pass

        stdCode = serializers.IntegerField()
        firstName = serializers.CharField(max_length=200)
        lastName = serializers.CharField(max_length=200)
        age = serializers.IntegerField(default=0)
        height = serializers.IntegerField(default=0)
        country = serializers.CharField(max_length=200)
        county = serializers.CharField(max_length=200)
        town = serializers.CharField(max_length=200)
        phone = serializers.CharField(max_length=200)
        website = serializers.CharField(max_length=200)

class Select2Serializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=200)

class CountriesSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    country_id = serializers.IntegerField()
    country_name = serializers.CharField(max_length=200)
    country_code = serializers.CharField(max_length=200)
    country_continent = serializers.CharField(max_length=200)


class CountiesSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    county_id = serializers.IntegerField()
    county_name = serializers.CharField(max_length=200)
    county_code = serializers.CharField(max_length=200)
    county_country = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
