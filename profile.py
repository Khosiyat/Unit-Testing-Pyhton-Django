from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile, Post, Post_StartUp, Follow


def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name

	# template = loader.get_template('base.html')
	
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')
		posts_StartUp = Post_StartUp.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()
		posts_StartUp = profile.favorites_StartUp.all()

	template = loader.get_template('profile.html') 

	#favorite count
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count() 


	context = {
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,

	}

	return HttpResponse(template.render(context, request))

