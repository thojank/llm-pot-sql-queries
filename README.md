# 🧠 Program-of-Thought SQL Generator  
**Powered by Gemini 2.5 + Streamlit + PostgreSQL**

Dieses Projekt demonstriert, wie du mithilfe von Google Gemini ein natürlichsprachliches Interface für SQL-Abfragen bauen kannst – inklusive Prompt-Engineering, automatischer SQL-Erzeugung und Live-Ausführung in einer echten Datenbank.

---

## 🚀 Features

- Prompt mit **Chain-of-Thought Reasoning**
- Nutzung von **Gemini 2.5 Flash (preview 05-20)**
- SQL-Ausgabe in PostgreSQL-kompatibler Syntax
- Live-Execution gegen Supabase/PostgreSQL
- Leichtgewichtig über **Streamlit UI**

---

## 🔧 Setup

```bash
git clone https://github.com/dein-username/llm-pot-sql-agent.git
cd llm-pot-sql-agent
pip install -r requirements.txt
cp .env.example .env
```

Dann `.env` mit deinen echten Zugangsdaten befüllen (siehe unten).

---

## 🗂️ .env Beispiel

```env
# Gemini / Google Generative AI
GOOGLE_CLOUD_API_KEY=your_google_cloud_api_key_here

# PostgreSQL / Supabase
DB_HOST=your-db-host.supabase.co
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_user
DB_PASSWORD=your_password
```

Oder alternativ mit `DATABASE_URL`:

```env
DATABASE_URL=postgresql://your_user:your_password@your-db-host.supabase.co:5432/your_database_name
```

---

## ▶️ Start

```bash
streamlit run main.py
```

---

## 💬 Beispiel-Fragen

```text
Gibt es Thorsten Jankowski?
Wie viele Urlaubstage hat Max noch?
Welche Mitarbeitenden haben weniger als 5 Tage Urlaub übrig?
```

---

## 📷 Screenshots

> siehe `/screenshots` oder Projektbeschreibung auf GitHub

---

## 🙏 CREDITS

> **Dieses Projekt basiert auf einem wunderbaren Prototypen von [@bunte-giraffe](https://github.com/bunte-giraffe)** – danke Zoryana für die Inspiration, Struktur und Klarheit beim Denken mit Code. 🦒💡

---

## 📄 Lizenz

MIT – free to use, improve & share.
