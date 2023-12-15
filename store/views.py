from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import JsonResponse
from .models import DATABASE
from logic.services import filtering_category


def products_view(request):
    if request.method == "GET":
        id = request.GET.get('id')
        list_prod = [product for product in DATABASE.keys()]
        if id:
            if id in list_prod:
                return JsonResponse(DATABASE[id], json_dumps_params={'ensure_ascii': False,
                                                                       'indent': 4})
            elif id not in list_prod:
                return HttpResponseNotFound("Данного продукта нет в базе данных")

            # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"):  # Если в параметрах есть 'ordering'
            if request.GET.get("reverse") in ('true', 'True'):  # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=True)
                # TODO Провести фильтрацию с параметрами
            else:
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=False)
                # TODO Провести фильтрацию с параметрами
        else:
            data = filtering_category(DATABASE, category_key)
            # TODO Провести фильтрацию с параметрами
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    with open(f'store/products/{page}.html', encoding="utf-8") as f:
                        page_product = f.read()
                    return HttpResponse(page_product)

        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as f:
                    page_product = f.read()
                return HttpResponse(page_product)

        return HttpResponse(status=404)
