from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class BlogTests(TestCase):
    def test_create_blog(self):
        from . import models
        user = User.objects.create(username="Alice")
        blog = models.Blog.objects.create(name="In Wonderland", user=user)
        self.assertEqual("A fancy blog called In Wonderland by Alice",
                         blog.get_description())

    def test_create_blog_named_blog(self):
        from . import models
        user = User.objects.create(username="Alice")
        blog = models.Blog.objects.create(name="blog", user=user)
        self.assertEqual("Definitely not a blog",
                         blog.get_description())
