from django.urls import path
from .views import NewsList, NewsDetail, AuthorsList, AuthorDetail  # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('authors/', AuthorsList.as_view()),
    path('authors/<int:pk>', AuthorDetail.as_view()),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('news/', NewsList.as_view()),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
]