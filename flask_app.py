from flask import Flask
import quest
import logging

# создание FLASK приложения
app = Flask(__name__)

# влкючение уровня трассировки INFO
logging.basicConfig(level=logging.INFO)


# основной обработчик запросов от Алисы
@app.route('/quest', methods=['POST'])
def run_quest():
    return quest.main()


# запуск программы
if __name__ == '__main__':
    app.run()
