from django.contrib.auth.models import User
user = User.objects.create_user('apina', 'kayttaja@asdfoparkopekpogh.aeropakop', 'gorilla')
user.save()
