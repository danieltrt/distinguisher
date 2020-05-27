from django.http import HttpResponse
from .src.logger import *
from .src.program import *
from .src.checker import *
from .src.interpreter import *
from .src.solver import *
from .src.model import *
from .src.distinguisher import *
from json import load
from os import listdir
import sys
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.edit import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *


logger = get_logger("polls")
logger.setLevel("DEBUG")


def load_dst():
    with open("./polls/example/instance1.json") as f:
        data = load(f)
    # UnchartIt specific
    logger.debug("Loading programs.")
    programs = []
    programs_paths = [data['programs'] + f for f in listdir(data['programs'])]
    for program_path in programs_paths:
        programs += [UnchartItProgram(program_path)]

    logger.debug("Loading CBMC template.")
    template = UnchartItTemplate(data["cbmc_template"], data['input_constraints'])
    interpreter = UnchartItInterpreter(data['input_constraints'])

    # Generic
    model_checker = CBMC(template)
    solver = Solver("open-wbo")
    interaction_model = YesNoInteractionModel(model_checker, solver, interpreter)

    return Distinguisher(interaction_model, programs)


dst = load_dst()


def index(request):
    inpt, output = dst.distinguish()

    question = Question(id=None, question_text=inpt)
    question.save()

    for out in output:
        choice = Choice(id=None, question_text=question, choice_text=out)
        choice.save()

    return render(request, 'yesno.html', {
        'question': question, "header": inpt.get_header(), "rows": inpt.get_active_rows()
    })


def options(request):
    inpt, output = dst.distinguish()

    question = Question(id=None, question_text=inpt)
    question.save()

    for out in output:
        choice = Choice(id=None, question_text=question, choice_text=out)
        choice.save()

    return render(request, 'yesno.html', {
        'question': question, "header": ["lol", "lol2"], "rows": [[1,2],[3,2]]
    })



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'options.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:index'))


