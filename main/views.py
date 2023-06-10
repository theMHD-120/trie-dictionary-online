from django.shortcuts import render

from utils.trie_dictionary import trie_dict


def home_page_view(request):
    if request.method == 'POST':
        word = request.POST['word']
        print(word)
    return render(request, 'main/home.html')
