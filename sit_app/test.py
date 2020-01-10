def make_bold(fn):
    def bold():
        return "<b>" + fn() + "</b>"

    return bold


def make_italic(fn):
    def italic():
        return "<i>" + fn() + "</i>"

    return italic


@make_bold
@make_italic
def hello():
    return "hello world"


helloHTML = hello()
print(helloHTML)
