from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
# Create your views here.65
class ChildrenViews(APIView):
    def get(self, request, child_id=None):
        if child_id is not None:
            try:
                child = Children.objects.select_related('parent').get(id=child_id)
            except Children.DoesNotExist:
                return Response({"error": "Child not found"}, status=status.HTTP_404_NOT_FOUND)
            child_serializer = ChildrenSerializer(child)
            return Response(child_serializer.data, status=status.HTTP_200_OK)
        else:
            all_children = Children.objects.select_related('parent').all()
            all_children_serializer = ChildrenSerializer(all_children, many=True)
            return Response(all_children_serializer.data, status=status.HTTP_200_OK)

    
    def post(self,request):
        create_child_serializer=ChildrenSerializer(data=request.data)
        if create_child_serializer.is_valid():
            create_child_serializer.save()
            return Response(create_child_serializer.data,status=status.HTTP_201_CREATED)
        return Response(create_child_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request,child_id):
        try:
            child=Children.objects.get(id=child_id)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
        update_child_serializer = ChildrenSerializer(child,data=request.data,partial=True, context={'request': request})
        if update_child_serializer.is_valid():
            update_child_serializer.save()
            return Response(update_child_serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(update_child_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,child_id):
        try:
            child=Children.objects.get(id=child_id)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
        child.delete()
        return Response({"message":f"Child with id {child_id} deleted successfully"},status=status.HTTP_202_ACCEPTED)
    

class ParentViews(APIView):
    def get(self,request,parent_id=None):
        if parent_id is not None:
            try:
                parent=Parent.objects.get(id=parent_id)
            except Exception as e:
                return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
            parent_serializer=ParentSerializer(parent)
            return Response(parent_serializer.data,status=status.HTTP_200_OK)
        else:
            all_parent=Parent.objects.all()
            all_parent_serializer=ParentSerializer(all_parent,many=True)
            return Response(all_parent_serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        create_parent_serializer=ParentSerializer(data=request.data)
        if create_parent_serializer.is_valid():
            create_parent_serializer.save()
            return Response(create_parent_serializer.data,status=status.HTTP_201_CREATED)
        return Response(create_parent_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request,parent_id):
        try:
            parent=Parent.objects.get(id=parent_id)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
        update_parent_serializer = ParentSerializer(parent,data=request.data,partial=True)
        if update_parent_serializer.is_valid():
            update_parent_serializer.save()
            return Response(update_parent_serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(update_parent_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,parent_id):
        try:
            parent=Parent.objects.get(id=parent_id)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_404_NOT_FOUND)
        parent.delete()
        return Response({"message":f"parent with id {parent_id} deleted successfully"},status=status.HTTP_202_ACCEPTED)
