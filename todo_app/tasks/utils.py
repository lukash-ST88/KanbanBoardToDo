from todo_app.config import SMTP_USER, SMTP_PASSWORD
from todo_app.auth.models import User
from email.message import EmailMessage


def get_email_template_expirated_tasks(user):
    email = EmailMessage()
    email['Subject'] = 'ToDo App'
    email['From'] = SMTP_USER
    email['To'] = 'lukash.andrei2012@yandex.ru'


    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {user}, а вот и ваш отчет. Зацените 😊</h1>'    
        '</div>',
        subtype='html'
    )
    return email
