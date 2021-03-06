from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import datetime

from .models import Choice, Question
from .forms import ContactForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:15]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    cookie_name = "vote"+str(question_id)
    if request.method.lower() == 'post' and cookie_name not in request.COOKIES:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            response = HttpResponseRedirect(reverse('results', args=(question.id,)))
            response.set_cookie("vote"+str(question_id), 1,
                                expires=datetime.datetime.utcnow() + datetime.timedelta(days=1))
            return response
        except Choice.DoesNotExist:
            pass

    # Redisplay the question voting form.
    return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "You didn't select a choice.",
    })


def new_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'template.html')
    else:
        form = ContactForm()
    return render(request, 'template.html', {'form': form})
