from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from .models import User, U2
from .serializer import UserSerializer, U2Serializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import generics, mixins

from .models import User
from .serializer import UserSerializer


# Genric Api View
class GenricApiListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):

    serializer_class = UserSerializer
    queryset = User.objects.all()   

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)

# Class based api view
    
class GetU2(APIView):
    def get(self, request):
        user = U2.objects.all()
        serializer = U2Serializer(user, many= True)
        return Response(serializer.data)


class GetUserList(APIView):

    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many= True)
        return Response(serializer.data)
    
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
    
        if user_serializer.is_valid():
            user_serializer.save()
            user2Link = U2()
            user2Link.name = user_serializer.data['name']
            user2Link.user = self.get_user(id=user_serializer.data["id"])
            user2Link.save()
            user_data = user_serializer.data
            user_data['u2'] = user2Link.id
            return Response(user_data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
    def get_u2(self, id):
        try:
            return U2.objects.get(user=id)
        except U2.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        user = self.get_user(id=id)
        try:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
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
        # u2 = self.get_u2(id=id)
        # u2.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateUserData(APIView):
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        user = self.get_user(id=request.data["id"])
        user_serialixer = UserSerializer(user, data=request.data)
        if user_serialixer.is_valid():
            user_serialixer.save()
            return Response(user_serialixer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serialixer.erro, status=status.HTTP_400_BAD_REQUEST)
        
    


# Function based api views
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many= True)
        return JsonResponse(serializer.data, safe=False, status=200)
    
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
        
