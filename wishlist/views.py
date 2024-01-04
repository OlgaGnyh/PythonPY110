from django.http import JsonResponse
from django.shortcuts import render, redirect
from store.models import DATABASE
from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound


@login_required(login_url='login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]
        # получить продукты из избранного для пользователя
        products = []
        # список словарей продуктов с их характеристиками
        for product_id in data['products']:
            product = DATABASE[product_id]

            products.append(product)
        return render(request, 'wishlist/wishlist.html',
                      # context={"products": DATABASE.values()},
                      context={"products": products})
        # отображение избранного. Путь до HTML - wishlist/wishlist.html


@login_required(login_url='login:login_view')
def wishlist_add_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)  # обработчик из services.py добавляющий продукт в избранное
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"},
                                json_dumps_params={'ensure_ascii': False})
            # JsonResponse с ключом "answer" и значением "Продукт успешно добавлен в избранное"

        return JsonResponse({"answer": "Неудачное добавление в избранное"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
        # JsonResponse с ключом "answer" и значением "Неудачное добавление в избранное" и параметром status=404


def wishlist_del_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        # обработчик из services.py удаляющий продукт из избранного
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из избранного"},
                                json_dumps_params={'ensure_ascii': False})
            # JsonResponse с ключом "answer" и значением "Продукт успешно удалён из избранного"
        return JsonResponse({"answer": "Неудачное удаление из избранного"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
        # JsonResponse с ключом "answer" и значением "Неудачное удаление из избранного" и параметром status=404


def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(request)[current_user]
        # данные о списке товаров в избранном у пользователя
        if data:
            return JsonResponse(data)  # JsonResponse c data
        return JsonResponse({"answer": "Пользователь не авторизирован"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
        # JsonResponse с ключом "answer" и значением "Пользователь не авторизирован" и параметром status=404


def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        if result:
            return redirect("wishlist:wishlist")

        return HttpResponseNotFound("Неудачное удаление из избранного")
