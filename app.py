from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

# Отримуємо повний шлях до файлів XML
data_folder = os.path.join(os.path.dirname(__file__), 'data')
users_xml_path = os.path.join(data_folder, 'users.xml')
posts_xml_path = os.path.join(data_folder, 'posts.xml')

# Функція для додавання нового користувача до файлу XML
def add_user_to_xml(username, password):
    tree = ET.parse(users_xml_path)
    root = tree.getroot()

    new_user = ET.SubElement(root, 'user')
    ET.SubElement(new_user, 'username').text = username
    ET.SubElement(new_user, 'password').text = password

    tree.write(users_xml_path)

# Функція для перевірки наявності користувача з вказаним ім'ям у файлі users.xml
def check_user(username):
    tree = ET.parse(users_xml_path)
    root = tree.getroot()

    for user in root.findall('user'):
        if user.find('username').text == username:
            return True

    return False

# Функція для додавання нового поста до файлу XML
def add_post_to_xml(topic, content, author):
    tree = ET.parse(posts_xml_path)
    root = tree.getroot()

    new_post = ET.SubElement(root, 'post')
    ET.SubElement(new_post, 'id').text = str(len(root) + 1)  # автоматичне надання id
    ET.SubElement(new_post, 'topic').text = topic
    ET.SubElement(new_post, 'content').text = content
    ET.SubElement(new_post, 'author').text = author

    tree.write(posts_xml_path)

# Маршрут для обробки реєстрації нового користувача
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    # Перевірка наявності користувача з таким ім'ям
    if check_user(username):
        return jsonify({'success': False, 'message': 'Username already exists'})

    # Додавання нового користувача до бази даних XML
    add_user_to_xml(username, password)

    return jsonify({'success': True, 'message': 'User registered successfully'})

# Маршрут для обробки створення нового поста
@app.route('/create_post', methods=['POST'])
def create_post():
    topic = request.form['topic']
    content = request.form['content']
    author = request.form['author']

    # Перевірка, чи існує користувач з вказаним ім'ям як автором поста
    if not check_user(author):
        return jsonify({'success': False, 'message': 'Author does not exist'})

    # Додавання нового поста до бази даних XML
    add_post_to_xml(topic, content, author)

    return jsonify({'success': True, 'message': 'Post created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
