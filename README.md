# Yapılacaklar Listesi Uygulaması

Bu uygulama, Flask backend API'si ve JavaScript frontend kullanarak oluşturulmuş tam kapsamlı bir yapılacaklar listesi uygulamasıdır.

## Özellikler

- Görev ekleme, düzenleme, silme ve tamamlandı işaretleme
- Frontend ve Backend mimari
- Sunucu tarafında veri depolama (JSON dosyası)
- Kullanıcı dostu arayüz ve animasyonlar
- Hata işleme ve kullanıcı geri bildirimleri
- Yükleme durumu göstergeleri
- XSS koruması
- Duplike görev kontrolü
- Responsive tasarım

## Teknolojiler

### Frontend
- HTML5, CSS3, JavaScript
- Fetch API ile asenkron istekler

### Backend
- Python Flask API
- CORS desteği
- Dosya tabanlı JSON veri depolama
- RESTful API tasarımı

## Kurulum

### Backend Kurulumu
1. Python 3.6 veya daha yeni bir sürüm yüklü olmalıdır
2. Gereken paketleri yükleyin:
   ```
   pip install flask flask-cors
   ```
3. Backend klasörüne gidin ve sunucuyu başlatın:
   ```
   cd backend
   python app.py
   ```
   
### Frontend Başlatma
1. `index.html` dosyasını herhangi bir tarayıcıda açın
2. Veya bir yerel sunucu kullanabilirsiniz:
   ```
   python -m http.server
   ```

## API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/` | GET | API ana sayfası |
| `/todos` | GET | Tüm görevleri listeler |
| `/todos` | POST | Yeni görev ekler |
| `/todos/:id` | PUT | Bir görevi günceller |
| `/todos/:id` | DELETE | Bir görevi siler |

## Nasıl Kullanılır

1. Backend sunucusunu başlatın (`python app.py`)
2. Frontend sayfasını tarayıcıda açın
3. Yeni bir görev eklemek için giriş alanına yazın ve "Ekle" butonuna tıklayın
4. Bir görevi tamamlandı olarak işaretlemek için görev metnine tıklayın
5. Bir görevi düzenlemek için "Düzenle" butonuna tıklayın
6. Bir görevi silmek için "Sil" butonuna tıklayın

## Geliştirme Notları

- Backend, `todos.json` dosyasında görevleri depolar
- Sunucu başlatıldığında bu dosya yoksa, otomatik olarak oluşturulur
- Tüm API istekleri hata durumlarını ele alır ve anlamlı yanıtlar döndürür 