

@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	BASE_WIDTH = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	user_SELF =request.user.id
	posts_self  = Post.objects.filter(user=user_SELF).order_by('-posted')


	context = {
		'form':form,

		'posts_self':posts_self,
	}

	return render(request, 'edit_profile.html', context)
