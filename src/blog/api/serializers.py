from rest_framework import serializers

from blog.models import BlogPost



class BlogPostSerializer(serializers.ModelSerializer):
	
	username=serializers.SerializerMethodField('get-username')
 
	
	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image','date_updated','username']



	def get_username(self, blog_post):
		username = blog_post.author.username
		return username






