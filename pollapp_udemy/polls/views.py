from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django.template import loader, RequestContext
from .models import Question

# Create your views here.


def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]

    # output = ", ".join(q.question_text for q in latest_questions)
    # template = loader.get_template('polls/index.html')
    # context = RequestContext(request, {'latest_questions': latest_questions, })  --> this is django 1.9
    context = {'latest_questions': latest_questions}
    # context = RequestContext(request)         -> error in 1.11, should use 1.10
    # context.push({"latest_questions":"bar"})
    print(context)
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    # return HttpResponse('These are the results of the question: %s' % question_id)


def vote(request, question_id):
    # return HttpResponse('Vote on question: %s' % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except:
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "Please select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
