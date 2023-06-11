from django.shortcuts import render, redirect, reverse

from utils.trie_dictionary import trie_dict


def search_word_view(request):
    if request.method == 'POST':
        word = request.POST['word']
        print(word)
    return redirect(reverse('home'))


def add_word_view(request):
    if request.method == 'POST':
        word = request.POST['word']
        print(word)
    return redirect(reverse('home'))


def home_page_view(request):
    return render(request, 'main/home.html')
