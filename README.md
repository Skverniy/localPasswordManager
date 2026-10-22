# 🔐 Local Password Manager / Локальный менеджер паролей

[🇬🇧 English version below](#-english-version) | [🇷🇺 Русская версия ниже](#-русская-версия)

---

## 🇬🇧 English version

A secure, self-hosted, and fully local password manager. It runs entirely within Docker and stores all your data in a single SQLite file, encrypted with military-grade cryptography.

### ✨ Features
- **Zero-Knowledge Architecture**: Your master password and encryption keys are never stored on the disk. Keys live only in RAM.
- **Strong Cryptography**: Argon2id for key derivation (KDF) and AES-256-GCM for data encryption.
- **Dockerized**: Simple deployment with a single `docker-compose` command.
- **Modern UI**: Fast, responsive, vanilla JS frontend (no build step required).
- **Localhost Only**: By default, the app binds to `127.0.0.1`, ensuring it's not exposed to your local network.
- **Rate Limiting**: Protection against brute-force attacks on the login endpoint.

### 🛠 Tech Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy
- **Database**: SQLite (stored in `./data/vault.db`)
- **Frontend**: HTML5, Vanilla JavaScript, TailwindCSS (via CDN)
- **Security**: `cryptography` (AES-GCM), `argon2-cffi`, `python-jose` (JWT)

### 📂 Project Structure
Make sure your files are arranged exactly like this:
```text
password-manager/             <-- Project Root
│
├── .env                      <-- (Create manually, copy from .env.example)
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
│
├── data/                     <-- (Auto-created by Docker, contains vault.db)
│
└── app/                      <-- Main application folder
    ├── __init__.py
    ├── main.py
    ├── config.py
    ├── database.py
    ├── api/                  (__init__.py, auth.py, vault.py)
    ├── core/                 (__init__.py, crypto.py, deps.py, limiter.py, security.py)
    ├── models/               (__init__.py, user.py, vault_item.py)
    ├── schemas/              (__init__.py, auth.py, vault.py)
    └── static/               (index.html, app.js)# 🔐 Local Password Manager / Локальный менеджер паролей

[🇬🇧 English version below](#-english-version) | [🇷🇺 Русская версия ниже](#-русская-версия)

---

## 🇬🇧 English version

A secure, self-hosted, and fully local password manager. It runs entirely within Docker and stores all your data in a single SQLite file, encrypted with military-grade cryptography.

### ✨ Features
- **Zero-Knowledge Architecture**: Your master password and encryption keys are never stored on the disk. Keys live only in RAM.
- **Strong Cryptography**: Argon2id for key derivation (KDF) and AES-256-GCM for data encryption.
- **Dockerized**: Simple deployment with a single `docker-compose` command.
- **Modern UI**: Fast, responsive, vanilla JS frontend (no build step required).
- **Localhost Only**: By default, the app binds to `127.0.0.1`, ensuring it's not exposed to your local network.
- **Rate Limiting**: Protection against brute-force attacks on the login endpoint.

### 🛠 Tech Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy
- **Database**: SQLite (stored in `./data/vault.db`)
- **Frontend**: HTML5, Vanilla JavaScript, TailwindCSS (via CDN)
- **Security**: `cryptography` (AES-GCM), `argon2-cffi`, `python-jose` (JWT)

### 📂 Project Structure
Make sure your files are arranged exactly like this:
```text
password-manager/             <-- Project Root
│
├── .env                      <-- (Create manually, copy from .env.example)
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
│
├── data/                     <-- (Auto-created by Docker, contains vault.db)
│
└── app/                      <-- Main application folder
    ├── __init__.py
    ├── main.py
    ├── config.py
    ├── database.py
    ├── api/                  (__init__.py, auth.py, vault.py)
    ├── core/                 (__init__.py, crypto.py, deps.py, limiter.py, security.py)
    ├── models/               (__init__.py, user.py, vault_item.py)
    ├── schemas/              (__init__.py, auth.py, vault.py)
    └── static/               (index.html, app.js)

----------------------------------------------------------

# 🔐 Локальный менеджер паролей

Безопасный, полностью локальный менеджер паролей. Работает автономно внутри Docker-контейнера и хранит все данные в одном файле SQLite, зашифрованном стойкой криптографией.

### ✨ Особенности
- **Архитектура нулевого знания (Zero-Knowledge)**: Мастер-пароль и ключи шифрования никогда не сохраняются на диск. Ключи живут только в оперативной памяти.
- **Надежная криптография**: Argon2id для генерации ключа (KDF) и AES-256-GCM для шифрования данных.
- **Docker-контейнеризация**: Простое развертывание одной командой `docker compose`.
- **Современный интерфейс**: Быстрый и адаптивный фронтенд на чистом JS (без этапа сборки).
- **Только локальный доступ**: По умолчанию приложение доступно только на `127.0.0.1` и не торчит в локальную сеть.
- **Защита от брутфорса**: Ограничение количества попыток входа (Rate Limiting).

### 🛠 Стек технологий
- **Бэкенд**: Python 3.12, FastAPI, SQLAlchemy
- **База данных**: SQLite (файл `./data/vault.db`)
- **Фронтенд**: HTML5, Vanilla JavaScript, TailwindCSS (через CDN)
- **Безопасность**: `cryptography` (AES-GCM), `argon2-cffi`, `python-jose` (JWT)

### 📂 Структура проекта
Убедитесь, что ваши файлы разложены ровно по этой схеме (особенно важно, чтобы файлы Python лежали внутри папки `app`):
```text
password-manager/             <-- Корень проекта
│
├── .env                      <-- (Создать вручную, скопировав из .env.example)
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
│
├── data/                     <-- (Создастся автоматически, здесь будет vault.db)
│
└── app/                      <-- Главная папка приложения
    ├── __init__.py           (пустой файл)
    ├── main.py
    ├── config.py
    ├── database.py
    ├── api/                  (__init__.py, auth.py, vault.py)
    ├── core/                 (__init__.py, crypto.py, deps.py, limiter.py, security.py)
    ├── models/               (__init__.py, user.py, vault_item.py)
    ├── schemas/              (__init__.py, auth.py, vault.py)
    └── static/               (index.html, app.js)