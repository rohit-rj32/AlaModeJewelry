from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import viewsets, status
from Orders.models import Person
from Orders.serializer import PersonSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator



# Create your views here.
class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status' : False,
                'messaage' : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username = serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'messaage': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'status': True, 'message': 'user login', 'token':str(token)
        } , status=status.HTTP_201_CREATED)

class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status' : False,
                'messaage' : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': True, 'message' : 'user created'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def index(request):
    cources = dict(cource_name='Python', learn=['Django', 'Flask'])
    return Response(cources)


class PersonAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            objts = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3
            paginater = Paginator(objts, page_size)
            serializer = PersonSerializer(paginater.page(page), many=True)
        except Exception as e:
            return Response({
                'status' : False,
                'message' : 'invalid page'
            })

        return Response(serializer.data)

    def put(self, request):
        data = request.data
        objt = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(objt, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        objt = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(objt, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        objt = Person.objects.get(id=data['id'])
        objt.delete()
        return Response({"message": "Person deleted"})


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objts = Person.objects.all()
        serializer = PersonSerializer(objts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        objt = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(objt, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        objt = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(objt, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    elif request.method == 'DELETE':
        data = request.data
        objt = Person.objects.get(id=data['id'])
        objt.delete()
        return Response({"message": "Person deleted"})


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        serialiser = PersonSerializer(queryset, many=True)
        return Response({'data': serialiser.data}, status=status.HTTP_204_NO_CONTENT)

