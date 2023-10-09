@login_required
def Delete_account(request):

	if request.user == request.user:
		delete_user = User.objects.get(username=request.user)
		delete_user.delete()
		return redirect('signup')
	else:
		return redirect('signup')
