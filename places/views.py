from django.shortcuts import render


def show_index(request):
    print('Кто-то зашёл на главную!')
    return render(request, "index.html")
