<html>
    <head>
        <title>Мои результаты</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #481DBD; color: white; }
            .correct { color: green; }
            .incorrect { color: red; }
            button { padding: 10px 20px; background: #481DBD; color: white; border: none; cursor: pointer; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h2>Мои результаты</h2>
        <table>
            <tr>
                <th>Опрос</th>
                <th>Тема</th>
                <th>Результат</th>
                <th>Мои ответы</th>
            </tr>
    
            % for result in results:
                % result_class = 'correct' if result['result'] == 'Correct' else 'incorrect'
                <tr>
                    <td>{{result['task_name']}}</td>
                    <td>{{result['theme']}}</td>
                    <td class="{{result_class}}">{{result['result']}}</td>
                    <td>{{result['answers']}}</td>
                </tr>
            % end

        </table>
        <button onclick="window.location.href='/'">На главную страницу</button>
    </body>
</html>