from django.core import mail


def send_mail(to_email, confirmation_code):
    subject = 'Регистрация на YaMDB.'
    message = (
        'Привет! Это администрация YaMDB!\n'
        'Спасибо за регистрацию на нашем сайте!\n'
        'Аутентификация на сайте происходит с помощью JWT-токена.\n'
        'Для получения токена отправьте запрос на '
        'http://127.0.0.1:8000/api/v1/auth/token/ с данными email и confirmation_code.\n'
        f'Ваш confirmation_code: {confirmation_code}. Никому не сообщайте этот код!'
    )
    mail.send_mail(
        subject=subject,
        message=message,
        from_email='admin@yamdb.ru',
        recipient_list=(to_email,),
    )
