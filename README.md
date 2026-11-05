# 🎯 Valoshop — Заявки на скины Valorant

Шуточный веб-сайт для друзей, где можно оставить «заявку» на получение желаемого скина в Valorant. 
Никаких реальных транзакций — только веселье, каталог скинов и админка для модерации заявок. 

## 🚀 Стек технологий
* **Backend:** Python 3.14, Django 6.1
* **База данных:** SQLite (для разработки)
* **Frontend:** HTML, Bootstrap 5 (через CDN)
* **Безопасность:** python-dotenv (секреты вынесены в `.env`)

## 🛠 Функционал (на данный момент)
* 📦 Каталог оружия и скинов (управляется через админку).
* 📝 Страница отдельного скина с информацией об оружии.
* ⚙️ Кастомная админка с кнопками массового «Одобрения» и «Отклонения» заявок.
* (В разработке) Форма отправки заявки без регистрации.

## 💻 Как запустить локально

Клонируйте репозиторий:
```bash
   git clone https://github.com/jaferkoi/valshop.git
   cd valoshop
```

🪟 Для Windows
1. Создайте виртуальное окружение:
```powershell
    py -m venv venv_val
```

2. Активируйте его:

Если вы используете PowerShell:

```powershell
    .\venv_val\Scripts\Activate.ps1
```
(Если появится ошибка не удается загрузить файл Activate.ps1, так как выполнение сценариев отключено, выполните в PowerShell от имени администратора: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned и ответьте Y).

Если вы используете CMD (командную строку):

```cmd
    venv_val\Scripts\activate.bat
```

3. Установите зависимости:

```powershell
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
```

4. Создайте файл .env в корне проекта (рядом с manage.py) и добавьте туда:

```env
    DJANGO_SECRET_KEY=ваш_секретный_ключ
    DJANGO_DEBUG=True
```

5. Примените миграции и создайте админа:

```powershell
    py manage.py migrate
    py manage.py createsuperuser
```
6. Запустите сервер:

```powershell
    py manage.py runserver
```


🐧 Для Linux / macOS
1. Создайте виртуальное окружение:

```bash
    python3 -m venv venv_val
```

2. Активируйте его:

```bash
    source venv_val/bin/activate
```

3. Установите зависимости:

```bash
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
```

4. Создайте файл .env в корне проекта и добавьте туда:

```env
    DJANGO_SECRET_KEY=ваш_секретный_ключ
    DJANGO_DEBUG=True
```
5. Примените миграции и создайте админа:

```bash
    python manage.py migrate
    python manage.py createsuperuser
```
6. Запустите сервер:

```bash
    python manage.py runserver
```