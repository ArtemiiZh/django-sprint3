from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

# Константы
POSTS_LIMIT = 5


def get_published_posts():
    """Вспомогательная функция для получения базового запроса постов.

    Отбирает только опубликованные посты с опубликованной категорией,
    дата публикации которых уже наступила, и оптимизирует запросы к БД.
    """
    return Post.objects.select_related('category', 'location').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    """Главная страница: выводит 5 последних опубликованных постов."""
    posts = get_published_posts().order_by('-pub_date')[:POSTS_LIMIT]

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
            'page_obj': posts,
            'post_list': posts,
        }
    )


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    post = get_object_or_404(get_published_posts(), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Страница категории: выводит все посты выбранной категории."""
    # Шаг 1: Проверяем саму категорию. Если она скрыта или её нет — 404
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    # Шаг 2: Извлекаем посты этой категории через вспомогательную функцию
    posts = (
        get_published_posts()
        .filter(category=category)
        .order_by('-pub_date')
    )

    # Шаг 3: Рендерим шаблон, передавая все варианты ключей
    return render(
        request,
        'blog/category.html',
        { 
            'category': category,
            'posts': posts,
            'page_obj': posts,
            'post_list': posts,
        }
    )
