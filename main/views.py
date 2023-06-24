from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from .models import Word
from utils.trie_dictionary import trie_dict


def search_word_view(request):
    if request.method == 'POST':
        context = {}
        word = request.POST['word'].strip()
        result = trie_dict.search_word(word, trie_dict.root, True)
        context['word'] = word
        if result == True:
            context['result'] = result
            word_obj = Word.objects.get(word=word)
            word_obj.frequency += 1
            word_obj.save()
        else:
            word_objects = Word.objects.filter(word__in=result).order_by('-frequency')[:5]
            context['suggestions'] = word_objects
        return render(request, 'main/search_result.html', context=context)
    else:
        return redirect(reverse('home'))


def add_word_view(request):
    context = {}
    if request.method == 'POST':
        word = request.POST['word'].strip()
        context['word'] = word
        result = trie_dict.add_new_word(word)
        if result:
            context['result'] = True
        else:
            context['result'] = False

        return render(request, 'main/add_result.html', context=context)
    else:
        return redirect(reverse('home'))


def home_page_view(request):
    return render(request, 'main/home.html')
