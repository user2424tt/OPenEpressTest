<html>
    <head>
        <meta charset="UTF-8">
        <title>Создать опрос</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            form { max-width: 500px; }
            input, textarea { width: 100%; padding: 8px; margin: 5px 0; resize: none;}
            button { padding: 10px 20px; background: #481DBD; color: white; border: none; cursor: pointer; }
            .checkbox_input { width: auto !important;}
        </style>
    </head>
    <body>
        <h2>Создать новый опрос</h2>
        <form action="/api/create_task" method="post">
            <input type="text" name="theme" placeholder="Тема опроса" required><br>
            <input type="text" name="name" placeholder="Имя опроса" required><br>
            <textarea name="text" placeholder="Описание вопроса" rows="3" required></textarea><br>

            <div id="answers">

                <hr>
                <input type="text" name="answer_A" placeholder="Вариант ответа A..." required>
                <span>Правильный ответ: </span><input class="checkbox_input" type="checkbox" name="answer_A_correct">
                <hr>

            </div>

            <input type="number" name="number" placeholder="Номер вопроса:" required><br>
            <button type="submit">Создать опрос</button>
            <button type="button" onclick="window.location.href='/'">Вернуться обратно</button>
            <button type="button" onclick="AddNewAnswer()">Добавить ещё ответ...</button>
        </form>
    </body>
    <script>

        let letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        current_answer = 0;

        function AddNewAnswer() {

            if(letters[current_answer] == "z") {
                alert("Вы превысили максимальное число вариантов ответа не вопрос!");
                return;
            }

            current_answer++;

            let line = document.createElement("hr");

            let input_text = document.createElement("input");
            input_text.type = "text";
            input_text.name = `answer_${letters[current_answer]}`;
            input_text.placeholder = `Вариант ответа ${letters[current_answer]}...`;
            
            let input_checkbox_text = document.createElement("span");
            input_checkbox_text.innerHTML = "Правильный ответ: ";

            let input_checkbox = document.createElement("input");
            input_checkbox.type = "checkbox";
            input_checkbox.className = "checkbox_input";
            input_checkbox.name = `answer_${letters[current_answer]}_correct`;



            document.getElementById("answers").append(input_text);
            document.getElementById("answers").append(input_checkbox_text);
            document.getElementById("answers").append(input_checkbox);
            document.getElementById("answers").append(line);

        }
    </script>
</html>