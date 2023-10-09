
def DeleteNotification(request, noti_id):
	user = request.user
	Notification.objects.filter(id=noti_id, user=user).delete()
	return redirect('index')

