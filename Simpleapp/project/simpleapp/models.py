from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    cat_name = models.CharField(max_length=255, unique=True)
    cat_subscribers = models.ManyToManyField(User,through='Catsubs')

    def __str__(self):
        return self.cat_name


class Author(models.Model):
    name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)

    author_to_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self, post_ratings, mycom_ratings, allcom_ratings):
        i = 0
        new_rating = 0
        for i in range(len(post_ratings)):
            new_rating += post_ratings[i]['post_rating']
            i += 1
        self.rating = 3 * new_rating
        i = 0
        new_rating = 0
        for i in range(len(mycom_ratings)):
            new_rating += mycom_ratings[i]['com_rating']
            i += 1
        self.rating += new_rating
        i = 0
        new_rating = 0
        for i in range(len(allcom_ratings)):
            new_rating += allcom_ratings[i]['com_rating']
            i += 1
        self.rating += new_rating
        self.save()

    def __str__(self):
        return self.name





class Catsubs(models.Model):
    amount = models.IntegerField(default=1)
    catsubs_to_subs = models.ForeignKey(User, on_delete=models.CASCADE)
    catsubs_to_cat = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    POST_TYPES = [('ART', 'Статья'),
                  ('POST', 'Новость')]
    post_name = models.CharField(max_length=255)
    post_text = models.TextField()
    post_datetime = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(choices=POST_TYPES, max_length=255, default='ART')
    post_rating = models.IntegerField(default=0)
    post_to_author = models.ForeignKey(Author, on_delete=models.CASCADE) #мини-костыль - если автора нет, то пост приписывается Unnamed Author
    post_to_postcat = models.ManyToManyField(Category, through='Postcat')

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/posts/{self.id}'

    def like(self):
        self.post_rating += 1
        self.save(update_fields=['post_rating'])

    def dislike(self):
        self.post_rating -= 1
        self.save(update_fields=['post_rating'])

    def preview(self):
        length = 50
        i = 0
        post_text = ''
        while i <= length and i < len(str(self.post_text)):
            post_text += str(self.post_text)[i]
            i += 1
        post_text += '...'
        return post_text

    #def __str__(self):
    #    return self.post_name


class Postcat(models.Model):
    amount = models.IntegerField(default=1)
    postcat_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    postcat_to_cat = models.ForeignKey(Category, on_delete=models.CASCADE)

    #def __str__(self):
    #    return self.postcat_to_cat


class Comment(models.Model):
    com_text = models.CharField(max_length=255)
    com_datetime = models.DateTimeField(auto_now_add=1)
    com_rating = models.IntegerField(default=0)

    com_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    com_to_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.com_rating += 1
        self.save(update_fields=['com_rating'])

    def dislike(self):
        self.com_rating -= 1
        self.save(update_fields=['com_rating'])

# Create your models here.
