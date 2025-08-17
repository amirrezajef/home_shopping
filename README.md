# خانه خرید - سیستم مدیریت خرید خانه

این پروژه یک سیستم مدیریت خرید خانه است که از React برای فرانت‌اند و Flask برای API استفاده می‌کند.

## ساختار پروژه

```
home_shopping/
├── api/                    # Flask API Backend
│   ├── app.py             # Flask application
│   └── requirements.txt   # Python dependencies
├── frontend/              # React Frontend
│   ├── src/               # React source code
│   ├── public/            # Public assets
│   └── package.json       # Node.js dependencies
├── templates/             # Legacy Flask templates (can be removed)
└── README.md
```

## ویژگی‌ها

- **مدیریت آیتم‌ها**: افزودن، ویرایش و حذف آیتم‌های خرید
- **دسته‌بندی**: سازماندهی آیتم‌ها بر اساس دسته‌بندی و زیردسته
- **گزینه‌های خرید**: مدیریت گزینه‌های مختلف برای هر آیتم
- **داشبورد**: نمایش آمار و وضعیت کلی پروژه
- **رابط کاربری مدرن**: طراحی زیبا و کاربرپسند با React

## نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8+
- Node.js 16+
- npm یا yarn

### راه‌اندازی Backend (Flask API)

1. به پوشه `api` بروید:
```bash
cd api
```

2. محیط مجازی Python ایجاد کنید:
```bash
python -m venv venv
```

3. محیط مجازی را فعال کنید:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. وابستگی‌ها را نصب کنید:
```bash
pip install -r requirements.txt
```

5. دیتابیس را راه‌اندازی کنید:
```bash
curl -X POST http://localhost:5000/api/init-db
```

6. سرور Flask را اجرا کنید:
```bash
python app.py
```

سرور API روی پورت 5000 اجرا می‌شود.

### راه‌اندازی Frontend (React)

1. به پوشه `frontend` بروید:
```bash
cd frontend
```

2. وابستگی‌ها را نصب کنید:
```bash
npm install
```

3. اپلیکیشن React را اجرا کنید:
```bash
npm start
```

اپلیکیشن React روی پورت 3000 اجرا می‌شود و به API Flask متصل می‌شود.

## API Endpoints

### آیتم‌ها
- `GET /api/items` - دریافت لیست همه آیتم‌ها
- `POST /api/items` - ایجاد آیتم جدید
- `GET /api/items/{id}` - دریافت جزئیات آیتم
- `PUT /api/items/{id}` - ویرایش آیتم
- `DELETE /api/items/{id}` - حذف آیتم

### گزینه‌ها
- `POST /api/options` - افزودن گزینه جدید
- `PUT /api/options/{id}/select` - انتخاب گزینه
- `PUT /api/options/{id}/unselect` - لغو انتخاب گزینه
- `DELETE /api/options/{id}` - حذف گزینه

### داشبورد
- `GET /api/dashboard` - دریافت اطلاعات داشبورد
- `POST /api/init-db` - راه‌اندازی دیتابیس

### دسته‌بندی‌ها
- `GET /api/subcategories/{category_id}` - دریافت زیردسته‌های یک دسته

## استفاده

1. ابتدا سرور Flask را اجرا کنید
2. سپس اپلیکیشن React را اجرا کنید
3. در مرورگر به `http://localhost:3000` بروید
4. دیتابیس را راه‌اندازی کنید (از طریق API یا دکمه در UI)
5. شروع به افزودن آیتم‌ها و گزینه‌ها کنید

## تکنولوژی‌های استفاده شده

### Backend
- **Flask**: فریم‌ورک وب Python
- **SQLAlchemy**: ORM برای دیتابیس
- **Flask-CORS**: پشتیبانی از CORS
- **SQLite**: دیتابیس

### Frontend
- **React**: کتابخانه UI
- **React Router**: مسیریابی
- **Axios**: HTTP client
- **CSS Grid/Flexbox**: طراحی ریسپانسیو

## توسعه

### اضافه کردن ویژگی‌های جدید
1. API endpoint جدید در Flask اضافه کنید
2. کامپوننت React مربوطه ایجاد کنید
3. مسیریابی مناسب اضافه کنید

### تغییرات دیتابیس
1. مدل‌های SQLAlchemy را تغییر دهید
2. migration script ایجاد کنید
3. API endpoints را به‌روزرسانی کنید

## عیب‌یابی

### مشکلات رایج
- **CORS Error**: مطمئن شوید که Flask-CORS نصب شده و فعال است
- **Database Error**: دیتابیس را مجدداً راه‌اندازی کنید
- **Port Conflicts**: پورت‌های 3000 و 5000 را بررسی کنید

### لاگ‌ها
- Flask logs در ترمینال backend
- React logs در ترمینال frontend
- Browser console برای خطاهای JavaScript

## مشارکت

برای مشارکت در پروژه:
1. Fork کنید
2. Branch جدید ایجاد کنید
3. تغییرات را commit کنید
4. Pull Request ارسال کنید

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.
