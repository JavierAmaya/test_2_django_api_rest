from django.shortcuts import render
from django.views import View
from django.utils import decorators
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.http.response import JsonResponse
import json


# Create your views here.
class UserView(View):
    # Este metodo sirve para saltarse el crossline, que es el que evita que entren
    #peticiones desde otro cliente no autorizado
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=0):
        
        if (id > 0):
            users = list(User.objects.filter(id=id).values())
            if len(users) > 0:
                user = users[0]
                datos = {'message': "success", 'user':user}
            else:
                datos = {'message':"error user no encontrada"}
                
            return JsonResponse(datos)
        
        else: 
            users = list(User.objects.values())
            if len(users) > 0 :
                datos = {'message': "success", 'users': users}
            else: 
                datos = {'message': "no data"}
            return JsonResponse(datos)
    
    def post(self, request):
        # # print(request.body)
        jd = json.loads(request.body)
        # # print(jd)
        User.objects.create(name = jd['name'], s_name = jd['s_name'], phone = jd['phone'])
        datos = {'message': "success"}
        return JsonResponse(datos)
    
    def put(self, request, id):
        jd = json.loads(request.body)
        users = list(User.objects.filter(id=id).values())
        if len(users) > 0:
            user = User.objects.get(id=id)
            user.name = jd['name']
            user.s_name = jd['s_name']
            user.phone = jd['phone']
            user.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "User not found..."}
        return JsonResponse(datos)
    
    def delete(self, request, id):
        users = list(User.objects.filter(id=id).values())
        if len(users) > 0:
            User.objects.filter(id=id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "user not found..."}
        return JsonResponse(datos)
