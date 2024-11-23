from rest_framework import serializers
from .models import *

class ParentSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(max_length=50)
    last_name=serializers.CharField(max_length=50)
    age=serializers.IntegerField(default=18)

    def create(self,validated_data):
        if Parent.objects.filter(first_name=validated_data["first_name"],last_name=validated_data["last_name"]).exists():
            raise serializers.ValidationError(f"this parent first name and last name is already taken")
        return Parent.objects.create(**validated_data)

    def update(self,instance,validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance


class ChildrenSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(max_length=50)
    last_name=serializers.CharField(max_length=50)
    age=serializers.IntegerField(default=1)
    parent_first_name=serializers.CharField(max_length=50,write_only=True)
    parent_last_name=serializers.CharField(max_length=50,write_only=True)
    
    def create(self,validated_data):
        parent_first_name=validated_data.pop("parent_first_name")
        parent_last_name=validated_data.pop("parent_last_name")
        try:
            parent=Parent.objects.filter(first_name=parent_first_name,last_name=parent_last_name).first()
            return Children.objects.create(parent=parent,**validated_data)
        except Exception as e:
            raise serializers.ValidationError(f"parent with first name : {parent_first_name} and last name : {parent_last_name} does not exist")
        
    
    def update(self, instance, validated_data):
        # Extract parent details if provided
        parent_first_name = validated_data.pop("parent_first_name", None)
        parent_last_name = validated_data.pop("parent_last_name", None)

        # Update parent only if both first and last names are provided
        if parent_first_name and parent_last_name:
            parent = Parent.objects.filter(first_name=parent_first_name, last_name=parent_last_name).first()
            if not parent:
                raise serializers.ValidationError(
                    f"Parent with first name '{parent_first_name}' and last name '{parent_last_name}' does not exist"
                )
            instance.parent = parent

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["parent_first_name"]=instance.parent.first_name
        rep["parent_last_name"]=instance.parent.last_name
        return rep 