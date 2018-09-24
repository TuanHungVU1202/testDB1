from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404

#from django.template import loader


#import from models
from .models import Question

# Create your views here.
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	
	'''import loader to use the following
	template = loader.get_template('testConnection/index.html')
	'''

	context = {
		'latest_question_list': latest_question_list,
	}
	#return HttpResponse(template.render(context, request))
	return render(request, 'testConnection/index.html', context)


def detail(request, question_id):
	''' Not using get_object_or_404 shortcut
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404('Question not exist')
	return render(request, 'testConnection/detail.html', {'question': question})
	'''
	#return HttpResponse("This is the question %s." %question_id)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'testConnection/detail.html', {'question': question})


def results(request, question_id):
	response = "The result of question %s."
	return HttpResponse(response % question_id)


def vote(request, question_id):
	return HttpResponse("Voting on question %s" %question_id)


