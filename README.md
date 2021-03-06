## Welltory - test case

Test case tech requirements: https://docs.google.com/document/d/1eOqpUsl8Fi99IARAkI6BKYkVt93Y-vuSQFfx6IZ3aGk/edit#

------------------------------------------

Before we begin:

Поскольку job application form не предложила написать что-то от себя (а-ля cover letter), сделаю это здесь.
Я, конечно, никакой не Senior, более того, не имел опыта с fastapi и (что предсказуемо оказалось сложнее) c асинхронной обработкой - синхронную версию задания сделал очень быстро. Тем не менее предложение выполнить тестовое задание было вызовом, который, надеюсь, даст мне возможность продемонстрировать некоторую смелость и способность быстро осваивать новые технологии и предметные области. 

Страшно интересна ваша предметная область и продукт - самостоятельно тренирую себя как соревнующегося велосипедиста (любителя), используя данные (ЧСС, HRV, мощность итп.), поэтому темы well-being, здоровья и HRV очень близки и я очень хотел бы получить шанс присоединиться к команде чтобы участвовать в разработке Welltory. 

Разрабатываю собственный opensource проект HARDIO – инструмент для анализа вело- (и, в будущем, беговых) тренировок с возможностью выявления позитивных метаболических изменений в организме на основе фактических данных собранных с датчиков мощности, скорости, ЧСС, итд. Проект в стадии разработки, но заметная часть бизнес логики завершена. 
Стек: Python, Flask, SQLAlchemy (PostgreSQL), Plotly/Dash
Развернутое приложение https://hardio.herokuapp.com/application/activity/5827372037 
GitHub: https://github.com/Zepp333333/HARDIO 

Уверен, что смогу максимально влиться в команду и процессы, перенять лучшие практики от опытных разработчиков и начать приносить пользу реальным проектам.

Поработав в большой корпорации, я бы хотел присоединиться к компании с культурой стартапа, где можно быстро принимать решения, отвечать за них и видеть результат своей работы. 

С уважением,
Сергей




------------------------------------------
### 1. Running test case in venv:
- git clone
- pip install -r requirements.txt
- uvicorn app.runner:run --reload
- kick services with: 
  
  <code>curl 'http://localhost:8000/a/' --header 'Content-Type: application/json' --data '{"name": "payload", "d;5Digits": [], "avg": null, "max": null, "min": null}'</code>

### 2. Running as docker image:
- docker build -t ping_pong .
- docker run -d --name pp -p 8000:8000 ping_pong
- kick services with: 
  
  <code>curl 'http://localhost:8000/a/' --header 'Content-Type: application/json' --data '{"name": "payload", "d;5Digits": [], "avg": null, "max": null, "min": null}'</code>

### 3. Краткое описание 
- Сервисы A и B взаимодействуют по http, адреса endpoints: http://localhost:8000/a/ and http://localhost:8000/b/ (hardcoded)
- Насколько я понял тех. требования, "примитивные" сервисы stateless и поэтому (в моей реализации) состояние содержится только в 
  самом json, который валидируют, обрабатывают и которым обмениваются сервисы. Это, безусловно, усложняет задачу отладки.
- Для иллюстрации работы сервисов, я сохранил в коде выводы в stdout содержимого payload при каждой его обработке обоими сервисами.

  
### 4. Отладка без доступа к коду (QA) - цель: понять в какой момент прервался pipeline и state на этот момент
Поскольку сервисы "общаются" только между собой и состояние содержится в payload, тестирование endpoints
с помощью Postman/Curl etc позволит только убедиться в работоспособности самих endpoints, их способности корректно
валидировать json на соответствие схеме, а также факт рандомной "отрицательной" валидации с ошибкой 400.

Для достижения цели отладки, я бы использовал сниффер между endpoints (либо пытался реализовать proxy/man-in-the-middle 
сценарий, в случае использования SSL) для понимания с каким кодом был остановлен пайплайн и в каком состоянии 
находится payload (из него также можно понять на какой итерации).

### 5. Отладка с доступом к коду (dev) - цель: понять в какой момент прервался pipeline и state на этот момент
- Сервисам отчаянно не хватает журналирования событий. Реализовал бы с использованием модуля logging
- добавил бы в схему json поле sequence в котором хранил бы словарь 
  {порядковый_номер_итерации : последний_сервис_обработавший_payload} - в сочетании с логгингом это
  дало бы мне возможность изолировать итерацию и сервис на которых пайплайн обрывается, для 
  дальнейшего исследования причин
- В зависимости от бизнес-потребностей, возможно имеет смысл реализовать stateful-сервисы, которые 
  сохраняли бы результаты своей обработки как минимум в in-memory database

