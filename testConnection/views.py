from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

#from django.http import Http404

#from django.template import loader


#import from models
from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
	template_name = 'testConnection/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		#return last 5 published questions
		return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'testConnection/detail.html'


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'testConnection/results.html'



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
	'''
	response = "The result of question %s."
	return HttpResponse(response % question_id)
	'''
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'testConnection/results.html', {'question': question})

def vote(request, question_id):
	#return HttpResponse("Voting on question %s" %question_id)
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#redisplay the question voting form
		return render(request, 'testConnection/detail.html', {
			'question': question,
			'error_message': "Haven't select a choice",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#always return an HttpResponseRedirect after successfully dealing with POST data
		return HttpResponseRedirect(reverse('testConnection:results', args=(question_id,)))


