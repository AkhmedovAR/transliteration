from flask import Flask, render_template, request
from transliterate import translit
from langdetect import detect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def translator():
    if request.method == 'POST':
        text = request.form['text']

        # Для определения языка
        language = detect(text)

        # Если текст на русском, то выводится ошибка, иначе выведится результат
        if language == 'ru':
            result = "Ошибка! Введен текст на кириллице. Пожалуйста, введите текст на латинском."
        else:
            latin_text = translit(text, 'ru')
            result = "Результат: " + latin_text

        return render_template('index.html', result=result)

    return render_template('index.html', result=None)


if __name__ == "__main__":
    app.run(debug=True, port=5001)