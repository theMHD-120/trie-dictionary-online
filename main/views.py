from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from utils.trie_dictionary import trie_dict


def search_word_view(request):
    if request.method == 'POST':
        word = request.POST['word'].strip()
        result = trie_dict.search_word(word)
        return render(request, 'main/home.html', context={'word': word, 'result': result, 'show_result': True})
    else:
        return redirect(reverse('home'))


def add_word_view(request):
    context = {}
    if request.method == 'POST':
        word = request.POST['word'].strip()
        result = trie_dict.add_new_word(word)
        if result:
            context['status'] = 'successful'
        else:
            context['status'] = 'already exists'

        return render(request, 'main/home.html', context=context)
    else:
        return redirect(reverse('home'))


def home_page_view(request):
    return render(request, 'main/home.html')
