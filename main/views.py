from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from utils.trie_dictionary import trie_dict


def search_word_view(request):
    if request.method == 'POST':
        word = request.POST['word'].strip()
        result = trie_dict.search_word(word)
        return render(request, 'main/search_result.html', context={'word': word, 'result': result})
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
