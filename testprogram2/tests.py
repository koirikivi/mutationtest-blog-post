from unittest import TestCase
from .program import Blog


class BlogTests(TestCase):
    def test_create_blog(self):
        blog = Blog(name="In Wonderland")
        self.assertEqual("A fancy blog called In Wonderland by Alice",
                         blog.get_description())

    def test_create_blog_named_blog(self):
        blog = Blog(name="blog")
        self.assertEqual("Definitely not a blog", blog.get_description())
