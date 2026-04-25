# ☁️ Cloud Voting System

A secure, web-based voting platform built with **Flask** and **Firebase Firestore**. It uses fingerprint-based authentication to ensure that each registered student can cast exactly one vote, with live results displayed through a clean, pastel-themed UI.

---

## ✨ Features

- **Fingerprint-based Authentication** — Students register and log in using a unique fingerprint ID.
- **One-person, One-vote** — Server-side double-vote prevention ensures election integrity.
- **Live Results** — Real-time vote tallying with animated progress bars.
- **CSRF Protection** — All forms are protected against cross-site request forgery.
- **Cloud Database** — Firebase Firestore stores all user and vote data securely.

---

## 🛠️ Tech Stack

| Layer     | Technology             |
| --------- | ---------------------- |
| Backend   | Python 3, Flask        |
| Database  | Firebase Firestore     |
| Frontend  | HTML5, CSS3 (Jinja2)   |
| Auth      | Firebase Admin SDK     |
| Security  | Flask-WTF (CSRF)       |

---

## 📁 Project Structure

```
Voting-System/
├── app.py                  # Flask web application (main entry point)
├── main.py                 # CLI-based voting interface (for testing)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Files excluded from version control
├── static/
│   └── style.css           # Pastel-themed stylesheet
└── templates/
    ├── index.html           # Landing page
    ├── register.html        # User registration form
    ├── login.html           # Login form
    ├── vote.html            # Voting page
    └── results.html         # Live results dashboard
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- A **Firebase project** with Firestore enabled
- A Firebase Admin SDK service account key (JSON)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Voting-System.git
cd Voting-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy the example file
cp .env.example .env       # Linux / macOS
copy .env.example .env     # Windows
```

Open `.env` and fill in your values:

```env
FLASK_SECRET_KEY=<generate-a-long-random-string>
FLASK_DEBUG=False
FIREBASE_KEY_PATH=serviceAccountKey.json
```

> **Tip:** Generate a strong secret key with:
> ```python
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 5. Add your Firebase key

Place your Firebase Admin SDK service account JSON file in the project root and make sure the filename matches `FIREBASE_KEY_PATH` in your `.env`.

> ⚠️ **Never commit this file to Git.** It is already listed in `.gitignore`.

### 6. Run the application

```bash
python app.py
```

The app will open automatically at **http://127.0.0.1:5000**.

---

## 🔐 Security Notes

- The Flask secret key is loaded from `.env` — never hard-code secrets.
- `debug=True` is disabled by default in production; controlled via `FLASK_DEBUG`.
- CSRF protection is enabled on all POST forms via Flask-WTF.
- Firebase credentials are excluded from version control via `.gitignore`.

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork this repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request.

Please make sure your code follows the existing style and passes any checks before submitting.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Firebase Admin Python SDK](https://firebase.google.com/docs/admin/setup)
- [Flask-WTF](https://flask-wtf.readthedocs.io/)
