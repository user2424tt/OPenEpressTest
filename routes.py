import sqlite3
from bottle import route, static_file, request, response, template
import json

import database

# Названия маршрутов
reg_page_route = "/reg_page"
auth_page_route = "/enter_page"
create_page_route = "/create"

@route('/', method='GET')
def index():
    tasks = database.db.get_tasks()
    themes = []
    for task in tasks:
        if themes.count(task["theme"]) == 0:
            themes.append(task["theme"])

    return template('templates/pages/main_page', root='.', reg_page_route=reg_page_route, auth_page_route=auth_page_route, create_page_route=create_page_route, surveys=tasks, themes=themes)

@route(reg_page_route, method='GET')
def reg_page():
    return template('templates/pages/reg_page', root='.')

@route('/register', method='POST')
def register():
    name = request.forms.getunicode('name')
    group = request.forms.getunicode('group')
    password = request.forms.getunicode('password')
    
    # User registration
    result = database.db.register_user(name, password, group)
    
    if result['success']:
        return template('templates/redirect', root='.', text="Регистрация успешна!", url=auth_page_route)
    else:
        return template('templates/redirect', root='.', text=f'''Произошла ошибка регистрации: {result['error']}''', url=reg_page_route)


@route(auth_page_route, method='GET')
def enter_page():
    return template('templates/pages/enter_page', root='.')

@route('/enter', method='POST')
def enter():
    login = request.forms.getunicode('login')
    group = request.forms.getunicode('group')
    password = request.forms.getunicode('password')
    
    # Authentication
    jwt_token = database.db.authenticate_user(login, password, group)
    
    if jwt_token:
        response.set_cookie('jwt', jwt_token)
        return template('templates/redirect', root='.', text="Вы успешно авторизовались!", url="/")
    else:
        return template('templates/redirect', root='.', text="Неверный логин/пароль!", url=auth_page_route)

@route(create_page_route, method='GET')
def create_page():
    return template('templates/pages/create_page', root='.')

@route('/api/create_task', method='POST')
def create_task():

    conn = sqlite3.connect('OprosDataBase.db')

    try:
        theme = request.forms.getunicode('theme')
        name = request.forms.getunicode('name')
        text = request.forms.getunicode('text')

        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        answers = []

        for letter in letters:
            answer_text = request.forms.getunicode('answer_' + letter)
            if answer_text:
                answers.append({"letter": letter, "text": answer_text, "correct": request.forms.getunicode('answer_' + letter + '_correct')})
            else:
                break
        number = request.forms.getunicode('number')
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT INTO Tasks (task_theme, task_name, task_text, task_number) 
               VALUES (?, ?, ?, ?) RETURNING id''',
            (theme, name, text, int(number))
        )

        id = cursor.fetchone()[0]

        for answer in answers:
            correct = 0
            if(answer["correct"] == "on"):
                correct = 1
            cursor.execute(
                '''INSERT INTO Options (task_id, option_letter, option_text, is_correct) 
                VALUES (?, ?, ?, ?)''',
                (id, answer["letter"], answer["text"], correct)
            )
        
        conn.commit()
        conn.close()

        return template('templates/redirect', root='.', text="Опрос успешно создан!", url="/")
    except Exception as e:
        conn.close()
        return template('templates/redirect', root='.', text=f'''Не удалось создать опрос: {str(e)}''', url=create_page_route)

@route('/survey/<id>', method=['GET'])
def survey(id):
    task = database.db.get_task_by_id(id)
    if task:
        # Create dynamic HTML page for the test
        
        current_user = database.db.check_jwt_token(request.cookies.get('jwt'))

        if not current_user:
            return template('templates/redirect', root='.', text="Вы не авторизованы!", url=auth_page_route)

        answers = database.db.get_answers_by_task(task["id"])
        
        return template('templates/pages/survey_page', root='.', task=task, answers=answers)
    else:
        return template('templates/error', root='.')

@route('/my_results')
def my_results():

    current_user = database.db.check_jwt_token(request.cookies.get('jwt'))
    if not current_user:
        return template('templates/redirect', root='.', text="Вы не авторизованы!", url=auth_page_route)
    
    results = database.db.get_user_results(current_user['id'])
    
    return template('templates/pages/my_results', root='.', results=results)

@route('/api/submit_test', method='POST')
def submit_test():
    try:
        data = request.json

        current_user = database.db.check_jwt_token(request.cookies.get('jwt'))
        if not current_user:
            return json.dumps({'success': False, 'error': 'Вы не авторизованы!'})

        user_id = current_user["id"]
        task_id = data.get('task_id')
        user_answers = data.get('answers', [])
        
        if not task_id:
            return json.dumps({'success': False, 'error': 'Отсутствует информация!'})
        
        # Get correct answers
        answers = database.db.get_answers_by_task(task_id)
        if not answers:
            return json.dumps({'success': False, 'error': 'Ответы не найдены!'})
        
        correct_answers = []
        for answer in answers:
            if answer["is_correct"]:
                correct_answers.append(answer)

        for answer in answers:
            if answer["is_correct"] and user_answers.count(answer["option_letter"] == 0):
                database.db.save_test_result(
                    user_id, 
                    task_id, 
                    ','.join(user_answers), 
                    False
                )
                return json.dumps({
                    'success': True,
                    'correct': False,
                    'correct_answers': correct_answers
                })
            elif not answer["is_correct"] and user_answers.count(answer["option_letter"] == 1):
                database.db.save_test_result(
                    user_id, 
                    task_id, 
                    ','.join(user_answers), 
                    False
                )
                return json.dumps({
                    'success': True,
                    'correct': False,
                    'correct_answers': correct_answers
                })
            
        database.db.save_test_result(
            user_id, 
            task_id, 
            ','.join(user_answers), 
            True
        )
        
        return json.dumps({
            'success': True,
            'correct': True,
            'correct_answers': correct_answers
        })
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})

# Catch-all for other static files
@route('/<filename:path>')
def serve_static(filename):
    return static_file("public/" + filename, root='.')