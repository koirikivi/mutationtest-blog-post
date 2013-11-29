from django.db import models
from django.conf import settings


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    name = models.CharField(max_length=50)

    def get_description(self):
        if self.name == "blog":
            return "Definitely not a blog"
        return "A fancy blog called {} by {}".format(
                self.name, self.user.username)
