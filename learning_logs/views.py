from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.forms.forms import Form

# Create your views here.

def check_topic_owner(topic,request):
	"""Confere que usuario esta logado"""
	if topic.owner != request.user:
		raise Http404


def index(request):
    """A pagina inicial de ll"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
	"""Mostra todos os assuntos"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
	"""Mostra um unico assunto e todas as suas entradas"""
	topic = Topic.objects.get(id=topic_id)
	#Garante que o usuario eh dono do topico
	check_topic_owner(topic, request)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
	"""Adiciona um novo assunto"""
	if request.method != 'POST':
		#se for um GET ele cria um form em branco
		#o interessante eh justamente que se nao for POST
		#ele devolve em branco! Ou seja, mais seguro!
		form = TopicForm()
	else:
		#Dados de POST submetidos; processa os dados
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
	"""Acrescenta uma nova entrada para um assunto em particular"""
	topic = Topic.objects.get(id=topic_id)
	if request.method != 'POST':
		#Nenhum dado foi submetido;cria o form em branco
		form = EntryForm()
	else:
		#Dados de POST submetidos;processa os dados
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			check_topic_owner(topic, request)
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
	"""Edita uma entrada existente"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	check_topic_owner(topic, request)
	if request.method != 'POST':
		#Requisicao inicial; preenche previamente o form com a entrada atual
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(request, 'learning_logs:topic', args=[topic.id]))
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)
