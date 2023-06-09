import smtplib

def send_email(query, product_name, discount, current_price, product_id, email):
    """
        Отправка электронного письма (email)
        """
    from_addr = "your-address@yandex.ru"
    to_addr = email
    encode = 'utf-8'
    subject = "Уведомление о снижении цены."
    text = f"По Вашему запросу {query} цена на товар {product_name} с артикулом - {product_id} снизилась на желаемые {discount} %  и составляет {current_price}"

    # оставшиеся настройки
    passwd = "**********"
    server = "smtp.yandex.ru"
    port = 587
    charset = f'Content-Type: text/plain; charset={encode}'
    mime = 'MIME-Version: 1.0'
    # формируем тело письма
    body = "\r\n".join((f"From: {from_addr}", f"To: {to_addr}",
                        f"Subject: {subject}", mime, charset, "", text))

    try:
        # подключаемся к почтовому сервису
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(from_addr, passwd)
        # пробуем послать письмо
        smtp.sendmail(from_addr, to_addr, body.encode(encode))
        smtp.quit()
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err


