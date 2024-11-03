from flask import Flask, render_template, request, jsonify
from dwh_assistant import natural_language_to_sql, build_dbml_schema, execute_sql_query
from config import Config

app = Flask(__name__)

schema_data = build_dbml_schema(Config.TABLE_NAMES)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message']

    response = natural_language_to_sql(user_message, schema_data)

    if response.get('error_description'):
        bot_message = response['error_description']
        sql_query = ''
    else:
        sql_query = response['sql']
        result = execute_sql_query(sql_query)
        if result['error']:
            bot_message = f"Ошибка выполнения SQL-запроса: {result['error']}"
        else:
            df = result['result']
            if df.empty:
                bot_message = "Запрос выполнен успешно, но результатов нет."
            else:
                bot_message = df.to_html(classes='table table-striped', index=False)

    return jsonify({'message': bot_message, 'sql_query': sql_query})

if __name__ == '__main__':
    app.run(debug=False)
