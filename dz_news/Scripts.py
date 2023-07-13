from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# Создание пользователей
user1 = User.objects.create_user(username='user1')
user2 = User.objects.create_user(username='user2')

# Создание объектов модели Author
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Создание категорий
category1 = Category.objects.create(name='Sport')
category2 = Category.objects.create(name='Politics')
category3 = Category.objects.create(name='Education')
category4 = Category.objects.create(name='Technology')

# Создание статей и новости
post1 = Post.objects.create(author=author1, post_type=Post.ARTICLE, title='Article 1', text='This is an article.')
post2 = Post.objects.create(author=author1, post_type=Post.NEWS, title='News 1', text='This is a news.')
post3 = Post.objects.create(author=author2, post_type=Post.ARTICLE, title='Article 2', text='This is another article.')

# Добавление категорий к статьям/новостям
post1.category.add(category1, category2)
post2.category.add(category3, category4)
post3.category.add(category2, category3, category4)

# Создание комментариев
comment1 = Comment.objects.create(post=post1, user=user1, text='Comment 1')
comment2 = Comment.objects.create(post=post1, user=user2, text='Comment 2')
comment3 = Comment.objects.create(post=post2, user=user1, text='Comment 3')
comment4 = Comment.objects.create(post=post3, user=user2, text='Comment 4')

# Увеличение/уменьшение рейтингов объектов
post1.like()
post2.like()
comment1.like()
comment2.dislike()

# Обновление рейтингов авторов
author1.update_rating()
author2.update_rating()

# Вывод информации о лучшем пользователе
best_author = Author.objects.order_by('-rating').values('user__username', 'rating').first()
print('Best Author:', best_author)

# Вывод информации о лучшей статье
best_post = Post.objects.order_by('-rating').values('created_at', 'author__user__username', 'rating', 'title').first()
print('Best Post:', best_post)

# Вывод всех комментариев к лучшей статье
comments = Comment.objects.filter(post=best_post).values('created_at', 'user__username', 'rating', 'text')
print('Comments:')
for comment in comments:
    print(comment)
