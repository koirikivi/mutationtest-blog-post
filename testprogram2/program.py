class Blog:
    def __init__(self, name):
        self.name = name
        self.user = lambda: None
        self.user.username = "Alice"

    def get_description(self):
        if self.name == "blog":
            return "Definitely not a blog"
        return "A fancy blog called {} by {}".format(
                self.name, self.user.username)
