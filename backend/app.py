# # Gerekli kütüphaneleri yüklüyoruz
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import json
# import os
# import time
#
# # Flask uygulamamızı başlatıyoruz
# app = Flask(__name__)
# # CORS'u etkinleştir
# CORS(app)
#
# # Dosya yolu tanımlama
# DATA_FILE = os.path.join(os.path.dirname(__file__), 'todos.json')
#
# # Görevleri dosyadan yükleme
# def load_todos():
#     if os.path.exists(DATA_FILE):
#         try:
#             with open(DATA_FILE, 'r', encoding='utf-8') as file:
#                 return json.load(file)
#         except (json.JSONDecodeError, IOError) as e:
#             app.logger.error(f"Dosya okuma hatası: {e}")
#             return []
#     return []
#
# # Görevleri dosyaya kaydetme
# def save_todos(todos):
#     try:
#         with open(DATA_FILE, 'w', encoding='utf-8') as file:
#             json.dump(todos, file, ensure_ascii=False, indent=2)
#         return True
#     except IOError as e:
#         app.logger.error(f"Dosya yazma hatası: {e}")
#         return False
#
# # Görevler listemizi yükleyelim
# todos = load_todos()
#
# # Say Welcome
# @app.route('/')
# def home():
#     return "Yapılacaklar API'sine hoş geldiniz"
#
# # GET: Tüm görevleri göster
# @app.route('/todos', methods=['GET'])
# def get_todos():
#     return jsonify(todos)
#
# # POST: Yeni bir görev ekle
# @app.route('/todos', methods=['POST'])
# def add_todo():
#     try:
#         data = request.json
#
#         # Gerekli alanların kontrolü
#         if not data or 'text' not in data or not data['text'].strip():
#             return jsonify({'error': 'Görev metni boş olamaz'}), 400
#
#         # Duplicate kontrolü
#         if any(todo['text'].lower() == data['text'].lower().strip() for todo in todos):
#             return jsonify({'error': 'Bu görev zaten mevcut'}), 400
#
#         # ID yoksa ekleyelim
#         if 'id' not in data:
#             data['id'] = int(time.time() * 1000)
#
#         # Completed değeri yoksa false yapalım
#         if 'completed' not in data:
#             data['completed'] = False
#
#         # Texti temizleyelim
#         data['text'] = data['text'].strip()
#
#         todos.append(data)
#         if save_todos(todos):
#             return jsonify({'message': 'Görev başarıyla eklendi', 'todo': data}), 201
#         else:
#             return jsonify({'error': 'Görev kaydedilemedi'}), 500
#     except Exception as e:
#         app.logger.error(f"Görev eklerken hata: {e}")
#         return jsonify({'error': 'Bir hata oluştu'}), 500
#
# # PUT: Görev güncelle
# @app.route('/todos/<int:todo_id>', methods=['PUT'])
# def update_todo(todo_id):
#     try:
#         data = request.json
#         if not data:
#             return jsonify({'error': 'Geçersiz veri'}), 400
#
#         # Metin güncellenmişse ve boşsa
#         if 'text' in data and not data['text'].strip():
#             return jsonify({'error': 'Görev metni boş olamaz'}), 400
#
#         # Metin güncellenmişse ve zaten varsa
#         if 'text' in data and data['text'].strip():
#             # Başka bir görevle aynı metni girmeye çalışıyorsa
#             is_duplicate = any(todo['id'] != todo_id and todo['text'].lower() == data['text'].lower().strip() for todo in todos)
#             if is_duplicate:
#                 return jsonify({'error': 'Bu görev zaten mevcut'}), 400
#
#         for i, todo in enumerate(todos):
#             if todo['id'] == todo_id:
#                 # Textse temizle
#                 if 'text' in data:
#                     data['text'] = data['text'].strip()
#
#                 todos[i].update(data)
#                 if save_todos(todos):
#                     return jsonify({'message': 'Görev güncellendi', 'todo': todos[i]})
#                 else:
#                     return jsonify({'error': 'Görev kaydedilemedi'}), 500
#
#         return jsonify({'error': 'Görev bulunamadı'}), 404
#     except Exception as e:
#         app.logger.error(f"Görev güncellerken hata: {e}")
#         return jsonify({'error': 'Bir hata oluştu'}), 500
#
# # DELETE: Görevi sil
# @app.route('/todos/<int:todo_id>', methods=['DELETE'])
# def delete_todo(todo_id):
#     try:
#         global todos
#         original_len = len(todos)
#         todos = [todo for todo in todos if todo['id'] != todo_id]
#
#         if len(todos) == original_len:
#             return jsonify({'error': 'Görev bulunamadı'}), 404
#
#         if save_todos(todos):
#             return jsonify({'message': 'Görev silindi'})
#         else:
#             return jsonify({'error': 'Görev silinemedi'}), 500
#     except Exception as e:
#         app.logger.error(f"Görev silerken hata: {e}")
#         return jsonify({'error': 'Bir hata oluştu'}), 500
#
# # Sunucuyu çalıştır
# if __name__ == '__main__':
#
#     app.run(debug=True)
#
from flask import Flask, request, jsonify
from flask_cors import CORS
from db_handler import (
    init_db, init_user_table,
    get_all_todos, add_todo, update_todo, delete_todo,
    register_user, verify_user
)

app = Flask(__name__)
CORS(app)

# 🟢 GET: Sadece giriş yapan kullanıcının görevlerini getir
@app.route('/todos', methods=['GET'])
def get_todos_route():
    user_data = request.args.get('user_id')
    if not user_data:
        return jsonify({"error": "Kullanıcı ID'si gerekli"}), 400
    todos = get_all_todos(int(user_data))
    return jsonify(todos)

# 🟡 POST: Yeni görev ekle (user_id zorunlu!)
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    if not data.get("text") or not data.get("user_id"):
        return jsonify({"error": "Veri eksik"}), 400
    try:
        add_todo(data)
        return jsonify({"message": "Görev eklendi"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔵 PUT: Görev güncelle
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo_route(todo_id):
    data = request.json
    update_todo(todo_id, data)
    return jsonify({'message': 'Görev güncellendi'}), 200

# 🔴 DELETE: Görevi sil
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo_route(todo_id):
    delete_todo(todo_id)
    return jsonify({'message': 'Görev silindi'}), 200

# 🔐 KAYIT
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Kullanıcı adı ve şifre gerekli"}), 400

    if register_user(username, password):
        return jsonify({"message": "Kayıt başarılı"}), 201
    else:
        return jsonify({"error": "Kullanıcı zaten mevcut"}), 409

# 🔐 GİRİŞ
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Kullanıcı adı ve şifre gerekli"}), 400

    from db_handler import connect_db
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result and verify_user(username, password):
        return jsonify({
            "message": "Giriş başarılı",
            "username": username,
            "user_id": result[0]
        }), 200
    else:
        return jsonify({"error": "Geçersiz kullanıcı adı veya şifre"}), 401

# Sunucuyu başlat
if __name__ == '__main__':
    init_db()
    init_user_table()
    app.run(debug=True)
