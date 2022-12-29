from django.shortcuts import render
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from pymongo import MongoClient
from bson.objectid import ObjectId
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import BasePermission
from django.conf import settings
import os
import jwt
from recon_home.logics import sub_finds

# Create your views here.
sample_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiNjM3NjJkZGJiN2UwZWZhNmI5NTE2OGNkIiwiaWF0IjoxNjcxMjg5MTUxfQ.nY_jl12EhsxZNNICNrFAeGFoxt6fbNCxaR_9c_GrjWc"


class IsManager(BasePermission):
    def has_permission(self, request, view):
        try:
            server = MongoClient(os.environ['SECRET_IS_HEREBRO'])
            pers = server.test.schema_beta_roles
            permission_obj = pers.find_one(
                {'role_id': request.user['role_id']})

            return (request.user and permission_obj['role_name'] == "Manager")
        except Exception as e:
            print(e)
            return (False)


def jwt_decode(token):
    decoded = jwt.decode(token, options={'verify_signature': False})
    return decoded['data']


class CustomUserAuth(BaseAuthentication):
    def authenticate(self, request):
        server = MongoClient(os.environ['SECRET_IS_HEREBRO'])
        col = server.test.schema_beta_users
        user_data = col.find_one({"_id": ObjectId(jwt_decode(sample_token))})
        if user_data is None:
            raise AuthenticationFailed("No User Found with these cridentials")
        else:
            return (user_data, sample_token)


@api_view(['GET'])
@authentication_classes([CustomUserAuth])
@permission_classes([IsManager])
def home(request):
    return Response({
        'data': f"Hello the sentnce you are reading is coming from api :) by {request.user['fname']}"
    })


@api_view(['POST'])
def adding_target(request):
    url = request.data['url']
    process = request.data['fun']
    if url == 'none' or url == "":
        return Response({
            'res': 'Please Enter a valid url and it must not be blank'
        })
    if process != "0" and process != "1":
        return Response({
            'res': 'Please enter a valid process'
        })
    prock_data = sub_finds.get_sub_domains(url)
    print(prock_data)
    return Response({
        'res': prock_data[2]
    })
