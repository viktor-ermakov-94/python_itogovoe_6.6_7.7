# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
# from django.shortcuts import render
from .models import Author, Category, Post, PostCategory, Comment
from datetime import datetime


# Create your views here.
class AuthorsList(ListView):
    model = Author
    # указываем имя шаблона, в котором будет лежать HTML, в котором будут все
    # инструкции о том, как именно пользователю должны вывестись наши объекты
    template_name = 'authors.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    context_object_name = 'authors'

    def get_queryset(self):
        # return Author.objects.filter(author_name="author2")
        return Author.objects.all()

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре
    # context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом
    # обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context


class AuthorDetail(DetailView):
    model = Author
    # указываем имя шаблона, в котором будет лежать HTML, в котором будут все
    # инструкции о том, как именно пользователю должны вывестись наши объекты
    template_name = 'author.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    context_object_name = 'author'


class NewsList(ListView):
    model = Post
    template_name = 'newslist.html'
    context_object_name = 'newslist'

    def get_queryset(self):
        # показываем только новости в порядке убывания даты публикации
        return Post.objects.filter(post_type='1').order_by('-input_date_time')
        # return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_count'] = self.get_queryset().count()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_queryset(self):
        return Post.objects.filter(post_type='1')  # показываем только новости


