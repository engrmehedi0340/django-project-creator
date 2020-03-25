from django.shortcuts import render, redirect
from mainapp.forms import DjangoFieldForm
import os, sys, glob


base_html_format = """{% load static %}
<!DOCTYPE html>
<html lang='en'>
	<head>
		<meta charset='UTF-8'>
		<meta name='viewport' content='width=device-width, initial-scale=1'>
		<link rel='stylesheet' type='text/css' href="{% static 'css/bootstrap.min.css' %}">
		<title>{{title}}</title>
		<link rel="stylesheet" type='text/css' href="{% static 'css/user_styles.css' %}">
	</head>
	<body>
		<div class='container'>
		{% block content %}
			<!-- Code will be here -->
		{% endblock %}
		</div>
		<script src="{% static 'js/jquery.js' %}"></script>
		<script src="{% static 'js/bootstrap.min.js' %}"></script>
	</body>
</html>	
"""

index_html_format = """{% extends 'base.html' %}
 
 {% block content %}
 <p>This is default code</p>
 {% endblock %}
"""
urls_py_format = """from django.urls import path
from . import views

urlpatterns = [
 path('', views.home, name='home'),
 path('home', views.home, name='home'),
]

"""

views_py_format = """from django.shortcuts import render, redirect

def home(request):
	title = 'Home'
	template_name = 'index.html'
	return render(request, template_name, {'title':title})

#END
"""


def home(request):
	title = 'Home'
	template_name = 'index.html'
	dir_lists = os.listdir(os.getcwd())
	form = DjangoFieldForm()
	

	if glob.glob('manage.py'):
		request.session['is_project_dir'] = True
	else:
		request.session['is_project_dir'] = False

	return render(request, template_name, {'title':title, 'dir_lists':dir_lists, 'form':form})


def action(request):
	if request.method == 'POST':
		form = DjangoFieldForm(request.POST)
		if form.is_valid():
			# do action
			project_name = form.cleaned_data['project_name']
			app_name = form.cleaned_data['app_name']

			command = 'django-admin startproject ' + project_name
			try:
				os.system('cmd /c ' + command)
			except:
				pass
			project_dir = os.getcwd() + '\\' + project_name
			try:
				#Changing to project directory and create templates 
				os.chdir(project_dir) 
				os.system('cmd /c "mkdir templates"')
				template_path = project_dir + '\\templates'
				os.chdir(template_path)
				file = open('base.html', 'w+')
				file.write(base_html_format)
				file.close()
				file = open('index.html', 'w+')
				file.write(index_html_format)
				file.close()
			except:
				pass

			os.chdir(project_dir)
			command = 'python manage.py startapp ' + app_name 
			os.system('cmd /c ' + command) #Now creating the app
			app_dir = project_dir + '\\' + app_name
			os.chdir(app_dir)
			try:
				#Now create urls.py and rewrite views.py
				file = open('urls.py', 'w+')
				file.write(urls_py_format)
				file.close()
				file = open('views.py', 'w+')
				file.write(views_py_format)
				file.close()
			except:
				pass
			#At last current directory status took place in
			#current project directory
			try:
				os.chdir(project_dir)
			except:
				pass

			request.session['is_success'] = True
			return redirect('/home')
	else:
		form = DjangoFieldForm()
	return redirect('/home')


def run_server(request): #work is in progress
	command = 'python manage.py runserver'
	os.system('cmd /k ' + command)
	request.session['is_server_running'] = True
	return redirect('/home')

#END
