from member.models import Member


def check_username_exists(username):
    return Member.objects.filter(username=username).exists()


def check_nickname_exists(nickname):
    return Member.objects.filter(nickname=nickname).exists()


def check_email_exists(email):
    return Member.objects.filter(email=email).exists()
