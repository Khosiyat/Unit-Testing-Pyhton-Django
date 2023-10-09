@login_required
def follow(request, username, option):
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=request.user).all().delete()
		else:
			 posts = Post.objects.all().filter(user=following)[:25]

			 with transaction.atomic():
			 	for post in posts:
			 		stream = Stream(post=post, user=request.user, date=post.posted, following=following)
			 		stream.save()

		return HttpResponseRedirect(reverse('profile', args=[username]))
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))
