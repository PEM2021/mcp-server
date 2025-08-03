# MCP Server – Model Context Protocol

A FastAPI server that:

- ✅ Chats about your CV by parsing a resume PDF
- ✅ Sends email notifications via SMTP (e.g. Mailtrap)
- ✅ Has a deployed live server with optional frontend

---

## 🚀 Live Demo

🔗 (https://mcp-server-92fy.onrender.com)

---

## 📁 Project Structure

```bash
mcp-server/
├── backend/
│   ├── main.py          # FastAPI entry point
│   ├── resume_parser.py # Extracts text from uploaded resumes
│   ├── email_sender.py  # SMTP email sending logic
│   └── .env.example     # Sample env file
├── frontend/ (optional)
│   └── Next.js client
├── requirements.txt
└── README.md
```
