<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>ЭКСПРЕСС ТЕСТ</title>
    <script>

        function goToPage() {
            var select=document.getElementById("pageSelector");
            var selected=select.value;
            if (selected) {
                window.location.href=selected;
            }
        }

    </script>
</head>

<body>
    <div class="head">
        <form action={{auth_page_route}}>
            <button>Вход в аккаунт</button>
        </form>
        <form action="{{reg_page_route}}">
            <button>Регистрация</button>
        </form>
        <form action="{{create_page_route}}">
            <button>Создать опрос</button>
        </form>

    </div>
    <div class="dropdown_background2" id="dropdown_background_fix2">
        <div class="dropdown2" id="dropdown_fix2">
    <select class="dropdown_button2" id="pageSelector" onchange="goToPage()">
        <option value="">Выберите опрос</option>
        % for survey in surveys:
            <option class="surveys" data-theme="{{survey["theme"]}}" value="/survey/{{survey["id"]}}">{{survey["name"]}}</option>
        % end
    </select>
    </div>
    </div>
    <div class="dropdown_background">
        <div class="dropdown">
            <input type="checkbox" id="toggle" />
            <label for="toggle" class="dropdown_button">Выбрать тему опроса</label>
            <ul class="checklist" id="themes_list">

                % for theme in themes:
                    <li>
                        <label class="checkbox-container">
                            <input type="checkbox" class="choise" data-theme="{{theme}}">{{theme}}
                            <span class="checkmark"></span>
                        </label>
                    </li>
                % end

            </ul>
        </div>
    </div>
    <div class="content">
        <header>
            <div class="site-title">
                <h2>Добро пожаловать на ЭКСПРЕСС ТЕСТ!</h2>
                <p>ЭКСПРЕСС ТЕСТ – это ваша платформа для быстрого и эффективного создания, проведения и анализа опросов
                    и тестов. Независимо от того, хотите ли вы узнать мнение вашей аудитории, проверить знания или
                    собрать ценные данные, наш сервис предлагает интуитивно понятные инструменты для достижения ваших
                    целей.</p>
            </div>
        </header>
    </div>
    <script>

        current_themes = [];

        document.getElementById("themes_list").addEventListener("click", (event) => {

            if(event.target.classList.contains("choise")) {

                theme = event.target.dataset.theme;
                surveys = document.querySelectorAll('.surveys');

                index = current_themes.indexOf(theme);

                if(index == -1) {
                    current_themes.push(theme)
                } else {
                    current_themes.splice(index, 1);
                }

                if(current_themes.length > 0) {
                    surveys.forEach(function(survey) {
                        if(current_themes.indexOf(survey.dataset.theme) != -1) {
                            survey.style.display = "flex";
                        } else {
                            survey.style.display = "none";
                        }
                    });
                } else {
                    surveys.forEach(function(survey) {
                        survey.style.display = "";
                    });
                }

            }

        });

    </script>
</body>

</html>