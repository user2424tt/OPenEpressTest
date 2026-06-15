<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/style.css">
    <title>{{task['name']}}</title>
</head>
<body>
    <div id="card">
        <form id="testForm">
            <h1>{{task['name']}}</h1>
            <p style="color: gainsboro">{{task['text']}}</p>
            <ul class="checklist2">
                % for answer in answers:
                    <li>
                        <label class="checkbox-container2">
                            <input type="checkbox" class="checkmark2" name="answers" value="{{answer["option_letter"]}}">
                            <span class="checkmark2"></span>
                        </label>
                        {{answer["option_text"]}}
                    </li>
                % end
            </ul>
            <div>
                <button type="button" onclick="window.location.href='/'">Назад</button>
                <button type="button" onclick="submitTest()">Отправить результат</button>
            </div>
        </form>
    </div>
    <script>
        function submitTest() {{
            const checkboxes = document.querySelectorAll('input[name="answers"]:checked');
            const answers = Array.from(checkboxes).map(cb => cb.value);

            fetch('/api/submit_test', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    task_id: {{task['id']}},
                    answers: answers
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    if(data.correct) {
                        alert("Верно!");
                    } else {
                        alert("Неверно! Верные ответы: " + data.correct_answers.join(', '));
                    }
                    window.location.href = "/";
                } else {
                    alert("Ошибка: " + data.error);
                }
            });
            
            
        }}
    </script>
</body>
</html>