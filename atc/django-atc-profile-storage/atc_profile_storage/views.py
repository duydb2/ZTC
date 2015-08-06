from atc_profile_storage.models import Profile
from atc_profile_storage.serializers import ProfileSerializer

from functools import wraps
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import JSONParser

class BadGateway(APIException):
    status_code = 502
    default_detail = 'Could not connect to ATC gateway.'


def serviced(method):
    '''
    A decorator to check if the service is available or not.
    Raise a BadGateway exception on failure to connect to the atc gateway
    '''
    @wraps(method)
    def decorator(cls, request, *args, **kwargs):
	service = None
#        service = atcdClient()
#        if service is None:
#            raise BadGateway()
        return method(cls, request, service, *args, **kwargs)
    return decorator


class ProfilesApi(APIView):

    @serviced
    def get(self, request, service):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @serviced
    def post(self, request, service):
       	data = request.DATA 
        profiles = Profile.objects.all()
	profiles.delete()
      	serializer = ProfileSerializer(data=data, many=True)
       	if not serializer.is_valid():
       	     raise ParseError(detail=serializer.errors)

	serializer.save()

       	return Response(
       	    serializer.data,
       	    status=status.HTTP_201_CREATED
       	)
 
    @serviced
    def delete(self, request, service, pk=None):
	profiles = Profile.objects.all() 
	profiles.delete()
       	return Response(
       	    status=status.HTTP_204_NO_CONTENT
       	)


class ProfileApi(APIView):
      
    def get_object(self, pk, create=None):
	""" get exist object if not, create """
     	try:
       	  profile = Profile.objects.get(pk=pk)
     	except Profile.DoesNotExist as e:
	 if create: 
	   profile = Profile.objects.create(id=pk, name='profile id=%s'%pk, content={u'up': [], u'down':[]})
	 else:
       	   return Response(
               e.message,
	       status=status.HTTP_404_OK
           )
	return profile

		
    @serviced
    def get(self, request, service, pk=None, format=None):
	profile = self.get_object(pk, create=True)
        serializer = ProfileSerializer(profile)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @serviced
    def post(self, request, service, pk=None, format=None):
	profile = self.get_object(pk)
 	data = request.DATA
       	serializer = ProfileSerializer(profile, data=data)
       	if not serializer.is_valid():
       	     raise ParseError(detail=serializer.errors)

       	serializer.save()
       	return Response(
       	    serializer.data,
       	    status=status.HTTP_201_CREATED
       	)

    @serviced
    def delete(self, request, service, pk=None):
	profile = self.get_object(pk)
	if profile:
	    profile.delete()
       	return Response(
       	    status=status.HTTP_204_NO_CONTENT
       	)

# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)
# 
# 
# @csrf_exempt
# def profile_list(request):
#     if request.method == 'GET':
#         return JSONResponse(serializer.data)
#     elif request.method == 'POST':
#         return HttpResponse(status=405)
#     else:
#         return HttpResponse(status=405)
# 
# 
# @csrf_exempt
# def profile_detail(request, pk):
#     try:
#         profile = Profile.objects.get(pk=pk)
#     except Profile.DoesNotExist:
#         return HttpResponse(status=404)
# 
#     if request.method == 'GET':
#         serializer = ProfileSerializer(profile)
#         return JSONResponse(serializer.data)
# 
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ProfileSerializer(profile, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)
# 
#     elif request.method == 'DELETE':
#         profile.delete()
#         return HttpResponse(status=204)
# 
#     else:
#         return HttpResponse(status=405)
