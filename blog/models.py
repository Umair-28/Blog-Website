from django.db import models

# Create your models here.


class Tag(models.Model):

    caption = models.CharField(max_length=20)

    def __str__(self):
        return f" {self.caption}"


class Author(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()


    def __str__(self):
        return f"{self.first_name}{self.last_name}  "


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=150)
    image_name = models.ImageField(upload_to="posts", null = True)
    date = models.DateField(auto_now = True)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null = True, related_name="posts")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.title} "
    

class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_name} {self.text}"


