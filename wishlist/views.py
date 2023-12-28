
from django.shortcuts import render, redirect


def wishlist_view(request):
    if request.method == "GET":
        return render(request, 'wishlist/wishlist.html')
        # прописать отображение избранного. Путь до HTML - wishlist/wishlist.html
