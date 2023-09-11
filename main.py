from flask import Flask, request, render_template
import face_recognition
import mysql.connector

app = Flask(__name__)

# Подключение к базе данных MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="abbos2002",
    database="rk6_schema"
)

# Создание курсора для выполнения SQL-запросов
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def detect_face():
    if request.method == 'POST':
        # Загрузите изображение с лицом, которое вы хотите идентифицировать
        uploaded_image = request.files['file']
        if uploaded_image:
            unknown_image = face_recognition.load_image_file(uploaded_image)
            # Получение кодировки лица на загруженном изображении
            unknown_face_encodings = face_recognition.face_encodings(unknown_image)
            if unknown_face_encodings:
                unknown_face_encoding = unknown_face_encodings[0]
                # Выполните SQL-запрос, чтобы получить информацию о человеке, чье лицо совпадает
                sql = "SELECT first_name, last_name FROM people WHERE face_encoding = %s"
                cursor.execute(sql, (unknown_face_encoding.tobytes(),))
                # Получение результатов запроса
                result = cursor.fetchone()
                if result:
                    # Информация о человеке найдена
                    first_name, last_name = result
                    return render_template('index.html', message=f"Имя: {first_name}, Фамилия: {last_name}")
                else:
                    return render_template('index.html', message="Лицо не идентифицировано в базе данных")
            else:
                return render_template('index.html', message="На загруженном изображении не найдено лицо")

    return render_template('index.html', message=None)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
