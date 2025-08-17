# راهنمای راه‌اندازی پروژه خانه خرید

## خلاصه تغییرات

پروژه شما از یک اپلیکیشن Flask ساده به یک معماری مدرن با React + Flask API تبدیل شده است:

### قبل از تغییرات:
- Flask با templates HTML
- همه چیز در یک فایل `app.py`
- رابط کاربری ساده

### بعد از تغییرات:
- **Backend**: Flask API در پوشه `api/`
- **Frontend**: React app در پوشه `frontend/`
- **جداسازی کامل**: فرانت‌اند و بک‌اند کاملاً جدا
- **رابط کاربری مدرن**: طراحی زیبا و ریسپانسیو

## ساختار جدید پروژه

```
home_shopping/
├── api/                    # Flask API Backend
│   ├── app.py             # Flask application با API endpoints
│   ├── requirements.txt   # Python dependencies
│   └── init_db.py         # Script راه‌اندازی دیتابیس
├── frontend/              # React Frontend
│   ├── src/               # React source code
│   │   ├── components/    # React components
│   │   ├── App.js         # Main app component
│   │   └── App.css        # Main styles
│   ├── public/            # Public assets
│   └── package.json       # Node.js dependencies
├── start.bat              # Windows startup script
├── start.sh               # Unix startup script
└── README.md              # Updated documentation
```

## مراحل راه‌اندازی

### مرحله 1: راه‌اندازی Backend (Flask API)

1. **به پوشه API بروید:**
   ```bash
   cd api
   ```

2. **محیط مجازی Python ایجاد کنید:**
   ```bash
   python -m venv venv
   ```

3. **محیط مجازی را فعال کنید:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **وابستگی‌ها را نصب کنید:**
   ```bash
   pip install -r requirements.txt
   ```

5. **سرور Flask را اجرا کنید:**
   ```bash
   python app.py
   ```

   سرور روی پورت 5000 اجرا می‌شود.

### مرحله 2: راه‌اندازی Frontend (React)

1. **در ترمینال جدید، به پوشه frontend بروید:**
   ```bash
   cd frontend
   ```

2. **وابستگی‌ها را نصب کنید:**
   ```bash
   npm install
   ```

3. **اپلیکیشن React را اجرا کنید:**
   ```bash
   npm start
   ```

   اپلیکیشن روی پورت 3000 اجرا می‌شود.

### مرحله 3: راه‌اندازی دیتابیس

1. **دیتابیس را راه‌اندازی کنید:**
   ```bash
   # در پوشه api
   python init_db.py
   ```

   یا از طریق API:
   ```bash
   curl -X POST http://localhost:5000/api/init-db
   ```

## استفاده از Script های راه‌اندازی

### Windows:
```bash
start.bat
```

### Linux/Mac:
```bash
./start.sh
```

## ویژگی‌های جدید

### Backend API:
- **RESTful API**: تمام endpoints با `/api/` شروع می‌شوند
- **CORS Support**: پشتیبانی کامل از React frontend
- **Error Handling**: مدیریت خطاهای بهتر
- **JSON Responses**: تمام responses در فرمت JSON

### Frontend React:
- **Modern UI**: طراحی زیبا و ریسپانسیو
- **Component-based**: کامپوننت‌های قابل استفاده مجدد
- **State Management**: مدیریت state با React hooks
- **Routing**: مسیریابی با React Router
- **API Integration**: ارتباط با Flask API با Axios

## کامپوننت‌های React

1. **Header**: نوار ناوبری
2. **Dashboard**: صفحه اصلی با آمار و آیتم‌ها
3. **NewItem**: فرم افزودن آیتم جدید
4. **ItemDetail**: نمایش جزئیات آیتم و گزینه‌ها

## API Endpoints

- `GET /api/dashboard` - اطلاعات داشبورد
- `GET /api/items` - لیست آیتم‌ها
- `POST /api/items` - ایجاد آیتم جدید
- `GET /api/items/{id}` - جزئیات آیتم
- `POST /api/options` - افزودن گزینه
- `PUT /api/options/{id}/select` - انتخاب گزینه

## عیب‌یابی

### مشکلات رایج:

1. **CORS Error**: مطمئن شوید که Flask-CORS نصب شده
2. **Port Conflicts**: پورت‌های 3000 و 5000 را بررسی کنید
3. **Database Error**: دیتابیس را مجدداً راه‌اندازی کنید

### لاگ‌ها:
- Flask logs در ترمینال backend
- React logs در ترمینال frontend
- Browser console برای خطاهای JavaScript

## مزایای معماری جدید

1. **جداسازی مسئولیت‌ها**: Backend و Frontend کاملاً جدا
2. **قابلیت توسعه**: تیم‌های مختلف می‌توانند همزمان کار کنند
3. **مقیاس‌پذیری**: امکان اضافه کردن mobile app یا desktop app
4. **تکنولوژی مدرن**: استفاده از آخرین تکنولوژی‌های web
5. **Maintainability**: کد تمیزتر و قابل نگهداری‌تر

## مراحل بعدی

1. **تست کامل**: تمام functionality را تست کنید
2. **UI/UX بهبود**: طراحی را بهتر کنید
3. **Authentication**: سیستم احراز هویت اضافه کنید
4. **Database Migration**: از SQLite به PostgreSQL یا MySQL
5. **Deployment**: نصب روی سرور تولید

## سوالات متداول

**Q: آیا می‌توانم از templates قدیمی استفاده کنم؟**
A: خیر، templates قدیمی با React جایگزین شده‌اند.

**Q: آیا دیتابیس تغییر کرده؟**
A: خیر، ساختار دیتابیس همان است، فقط API endpoints تغییر کرده‌اند.

**Q: آیا می‌توانم فقط Flask یا فقط React را اجرا کنم؟**
A: خیر، هر دو باید اجرا شوند چون React به Flask API متصل است.

**Q: آیا داده‌های قبلی حفظ می‌شوند؟**
A: بله، اگر فایل `shopping.db` را حفظ کنید.

## پشتیبانی

برای سوالات و مشکلات:
1. README.md را مطالعه کنید
2. Console logs را بررسی کنید
3. API endpoints را تست کنید
4. از browser developer tools استفاده کنید

موفق باشید! 🚀 