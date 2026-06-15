<!DOCTYPE html>
<html lang="ru">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>ЭКСПРЕСС ТЕСТ - Аутентификация</title>
</head>

<body>
    <div id="card">
    <form action="/enter" method="post" class="card_form_1">
        <div>
            <p>Пользователь : </p><input name='login' class="input_login_password">
        </div>
        <div>
            <p>Группа : </p><input name='group' class="input_login_password">
        </div>
        <div>
            <p>Пароль : </p><input type='password' name='password' class="input_login_password">
        </div>

        <button class="button_login_registration">Вход в аккаунт</button>
        </form>
        <form action="/" class="card_form_2">
            <button class="button_login_registration">Назад</button>
        </form>
    </div>
</body>

</html>
