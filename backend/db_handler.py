from werkzeug.security import generate_password_hash,check_password_hash
import psycopg2
# Veritabanına bağlantı kuran fonksiyon
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="todo_db",       # Veritabanı adın
        user="postgres",          # Kullanıcı adın
        password="123456"           # Şifren (bunu kendi şifrene göre değiştir!)
    )

# Uygulama ilk açıldığında tablo yoksa oluşturalım
def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id BIGINT PRIMARY KEY,
            text TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Tüm görevleri getir
def get_all_todos(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, text, completed FROM todos WHERE user_id = %s", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "text": r[1], "completed": r[2]} for r in rows]

# Yeni görev ekle
def add_todo(todo):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (id, text, completed, user_id) VALUES (%s, %s, %s, %s)",
                (todo["id"], todo["text"], todo["completed"], todo["user_id"]))
    conn.commit()
    cur.close()
    conn.close()

# Görev güncelle (tamamlandı veya metin değişikliği)
def update_todo(todo_id, updated_todo):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE todos SET text = %s, completed = %s WHERE id = %s",
                (updated_todo["text"], updated_todo["completed"], todo_id))
    conn.commit()
    cur.close()
    conn.close()

# Görev sil
def delete_todo(todo_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()

# Kullanıcılar için tablo oluşturma
def init_user_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Yeni kullanıcı kaydetme (şifre hash'lenir)
def register_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    password_hash = generate_password_hash(password)  # Güvenli şifreleme
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
        conn.commit()
        return True
    except psycopg2.Error as e:
        print("Kayıt hatası:", e)
        return False
    finally:
        cur.close()
        conn.close()

# Giriş yapan kullanıcıyı doğrulama
def verify_user(username,password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        return check_password_hash(result[0], password)
    return False