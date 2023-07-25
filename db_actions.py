# >>> from db_actions import acts
# >>> acts()
# a = Author.objects.get(author_name='author2')
# a.update_rating()
# Author.objects.get(author_name='author2').update_rating()

from datetime import datetime
from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment


def init():
    print(f'DB initialization started...')

    print(f' Очистка объектов...')
    PostCategory.objects.all().delete()
    print(f'  PostCategories = {PostCategory.objects.count()}')
    Category.objects.all().delete()
    print(f'  Categories = {Category.objects.count()}')
    Author.objects.all().delete()
    print(f'  Authors = {Author.objects.count()}')
    User.objects.all().delete()
    print(f'  Users = {User.objects.count()}')
    print(f' Очистка объектов завершена')

    print(f' Ввод новых данных...')
    print(f'  Создание пользователей и авторов...')
    User(username="user1").save()
    User(username="user2").save()
    User(username="comment_user1").save()
    User(username="comment_user2").save()

    Author(user=User.objects.get(username="user1"), author_name="author1").save()
    Author(user=User.objects.get(username="user2"), author_name="author2").save()
    print(f'  Пользователи и авторы созданы')
    print(f'   пользователей: {User.objects.count()}')
    print(f'   авторов: {Author.objects.count()}')

    print(f'  Создание категорий...')
    c1 = Category(name="cat1")
    c1.save()
    c2 = Category(name="cat2")
    c2.save()
    c3 = Category(name="cat3")
    c3.save()
    c4 = Category(name="cat4")
    c4.save()
    print(f'  Категории созданы: {Category.objects.count()}')

    print(f'  Создание постов и новостей...')
    p = Post(post_type='1', author=Author.objects.get(author_name='author1'), post_header='NewsHeader1',
             # input_date_time=datetime.strptime('2021-06-01 10:30', '%Y-%m-%d %H:%M'),
             post_body="""Слово1 слово2 плохое_слово1 плохое_слово2
плохое_слово3 слово3
1234567890
1234567890
1234567890
1234567890
1234567890
""", rating=1)
    p.save()
    p.input_date_time = datetime.strptime('2021-06-01 10:30', '%Y-%m-%d %H:%M')
    p.save()
    a = Author.objects.get(author_name='author2')
    p = Post(post_type='1', author=a, post_header='NewsHeader2',
             post_body="""Слово1 слово2 плохое_слово1 плохое_слово2
    плохое_слово3 плохое_слово4""", rating=2)
    # создать запись с явным указанием input_date_time
    p.save()
    p.input_date_time = datetime.strptime('2021-06-06 04:21', '%Y-%m-%d %H:%M')
    p.save()
    PostCategory(post=p, category=c1).save()
    PostCategory(post=p, category=c2).save()
    p = Post(post_type='0', author=a, post_header='PostHeader1', post_body='post_body1', rating=4)
    p.save()
    PostCategory(post=p, category=c3).save()
    p.input_date_time = datetime.strptime('2021-05-01 09:00', '%Y-%m-%d %H:%M')
    p.save()
    p = Post(post_type='0', author=a, post_header='PostHeader2', post_body='post_body2', rating=5)
    p.save()
    PostCategory(post=p, category=c4).save()
    p.input_date_time = datetime.strptime('2021-06-01 12:30', '%Y-%m-%d %H:%M')
    p.save()
    print(f'  Посты и новости созданы')
    print(f'   постов: {Post.objects.filter(post_type="0").count()}')
    print(f'   новостей: {Post.objects.filter(post_type="1").count()}')

    print(f'  Создание комментов...')
    p1 = Post.objects.get(post_header='NewsHeader1')
    p2 = Post.objects.get(post_header='PostHeader2')
    u1 = User.objects.get(username='comment_user1')
    Comment(post=p1, user=u1, comment_text='Комментарий №1. Текст комментария', rating=1).save()
    u2 = User.objects.get(username='comment_user2')
    Comment(post=p1, user=u2, comment_text='Комментарий №2. Грамотно излагаешь! Уважаю!', rating=2).save()

    Comment(post=p2, user=u1, comment_text='Комментарий №3. Текст комментария', rating=1).save()
    p2 = Post.objects.get(post_header='NewsHeader2')
    Comment(post=p2, user=u1, comment_text='Комментарий №4. 1 Комментарий к новости', rating=1).save()
    Comment(post=p2, user=u2, comment_text='Комментарий №5. 2 Комментарий к новости', rating=2).save()
    print(f'   Comments = {Comment.objects.count()}')
    print(f'  Комментарии созданы')

    print(f' Ввод новых данных завершён')
    print(f'DB initialization complete')


def acts():
    init()

    # 1. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
    print('1. Ставим лайки и дизлайки...')
    p1 = Post.objects.get(post_header='PostHeader1')
    p1.like()
    p1.dislike()
    p1.dislike()

    # 2. Обновить рейтинги пользователей.
    print('2. Рейтинги пользователей')
    print(' Обновление рейтингов пользователей...')
    for a in Author.objects.all():
        a.update_rating()
    # print(Author.objects.all().values('author_name', 'rating'))
    print(' Обновление рейтингов пользователей завершено')

    # 3. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
    a = Author.objects.all().order_by('-rating')[:1][0]
    print(f"3. Лучший пользователь (по версии Forbes):")
    print(f' Имя: {a.user.username}')
    print(f' Рейтинг: {a.rating}')

    # 4. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на
    #    лайках/дислайках к этой статье.
    # лучший пост - аналог SELECT TOP 1 ... ORDER BY rating DESC
    print('4. Лучшая статья:')
    p = Post.objects.all().order_by('-rating')[:1][0]
    print(f' Дата добавления статьи: {p.input_date_time.strftime("%d.%m.%Y %H:%M:%S")}')
    print(f' Автор: {p.author.author_name}')
    print(f' Рейтинг автора: {p.author.rating}')
    print(f' Заголовок статьи: "{p.post_header}"')
    print(f' Preview статьи: "{p.preview()}"')

    # 5. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
    cs = Comment.objects.filter(post=p)
    print(f'5. Комментарии к статье: {cs.count()}')
    n = 1
    for c in cs:
        print(f' Комментарий №{n}')
        print(f'  Дата комментария: {c.input_date_time.strftime("%d.%m.%Y %H:%M:%S")}')
        print(f'  Пользователь: {c.user.username}')
        print(f'  Рейтинг комментария: {c.rating}')
        print(f'  Текст комментария: {c.comment_text}')
        n += 1
