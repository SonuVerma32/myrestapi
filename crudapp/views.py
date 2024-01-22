from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from .models import User
from .serializer import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import generics, mixins


# Genric Api View
class GenricApiListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):

    serializer_class = UserSerializer
    queryset = User.objects.all()   

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


# Class based api view
class GetUserList(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many= True)
        return Response(serializer.data)
    
    def post(self, request):
        user_serialixer = UserSerializer(data=request.data)

        if user_serialixer.is_valid():
            user_serialixer.save()
            return Response(user_serialixer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serialixer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        user = self.get_user(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, id):
        user = self.get_user(id=id)
        user_serialixer = UserSerializer(user, data=request.data)

        if user_serialixer.is_valid():
            user_serialixer.save()
            return Response(user_serialixer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serialixer.erro, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user = self.get_user(id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# Function based api views
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many= True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        user_serialixer = UserSerializer(data=data)

        if user_serialixer.is_valid():
            user_serialixer.save()
            return JsonResponse(user_serialixer.data, status=201)
        else:
            return JsonResponse(user_serialixer.error_messages, status=400)
        


@csrf_exempt
def get_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        user_serialixer = UserSerializer(user, data=data)

        if user_serialixer.is_valid():
            user_serialixer.save()
            return JsonResponse(user_serialixer.data, status=201)
        else:
            return JsonResponse(user_serialixer.error_messages, status=400)
        
    elif request.method == "DELETE":
        user.delete()
        return HttpResponse(status=200)
        
