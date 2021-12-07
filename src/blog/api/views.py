from re import search
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from account.models import Account
from rest_framework.authentication import TokenAuthentication
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

@api_view(['GET', ])
@permission_classes((IsAuthenticated))
def api_detail_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = BlogPostSerializer(blog_post)
		return Response(serializer.data)


@api_view(['PUT',])
@permission_classes((IsAuthenticated))
def api_update_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if blog_post.author != user:
		return Response({'response': "You are not authorized to change the content"})
     


	if request.method == 'PUT':
		serializer = BlogPostSerializer(blog_post, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data[SUCCESS] = UPDATE_SUCCESS
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated))

def api_delete_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	user = request.user
	if blog_post.author != user:
		return Response({'response': "You are not authorized to change the content"})
	
	if request.method == 'DELETE':
		operation = blog_post.delete()
		data = {}
		if operation:
			data[SUCCESS] = DELETE_SUCCESS
		return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated))

def api_create_blog_view(request):

	# account = Account.objects.get(pk=1)
	account =  request.user
	blog_post = BlogPost(author=account)

	if request.method == 'POST':
		serializer = BlogPostSerializer(blog_post, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBlogListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer = BlogPostSerializer
    authentication_classes= (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class= PageNumberPagination
    filter_back = (SearchFilter,OrderingFilter)	
    search_fields = ('title' , 'body','author__username')
