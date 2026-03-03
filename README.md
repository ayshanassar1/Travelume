# ✈️ Travelume

> An AI-powered travel planning web application that helps users plan trips, manage travel journals, book accommodations, and interact with a smart travel coach chatbot.

---

## 🌟 Features

- 🤖 **AI Trip Planner** — Generate personalized itineraries powered by Google Gemini
- 📓 **Travel Journals** — Create, edit, and export travel journals with images and PDFs
- 💬 **Travel Coach Chatbot** — Real-time AI travel assistant with text-to-speech support
- 🔐 **Authentication** — Secure JWT-based user registration and login
- 🗺️ **Popular Destinations** — Curated destination cards with premium itinerary modals
- 📊 **Account Dashboard** — View saved trips, journals, and booking history

---

## 🏗️ Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| React + TypeScript | UI framework |
| Vite | Build tool & dev server |
| Redux Toolkit | State management |
| TailwindCSS | Styling |
| React Router | Client-side routing |
| Axios | API communication |

### Backend
| Technology | Purpose |
|---|---|
| FastAPI (Python) | REST API server |
| Uvicorn | ASGI server |
| Python-JOSE | JWT authentication |
| Passlib + bcrypt | Password hashing |
| Google Gemini API | AI itinerary & chat |
| ReportLab + Pillow | PDF & image generation |
| Pydantic | Data validation |

---

## 📁 Project Structure

```
Travelume/
├── backend/                  # FastAPI backend
│   ├── main.py               # App entry point & CORS setup
│   ├── models.py             # Pydantic data models
│   ├── requirements.txt      # Backend dependencies
│   └── routers/
│       ├── auth.py           # Login & signup endpoints
│       ├── chat.py           # Chatbot endpoints
│       ├── journals.py       # Journal CRUD endpoints
│       ├── planner.py        # AI itinerary endpoints
│       └── trips.py          # Trip management endpoints
│
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   │   ├── home/         # Hero, DestinationGrid, DestinationModal
│   │   │   ├── journal/      # JournalCreator, JournalPreview
│   │   │   ├── planner/      # Itinerary display & PDF export
│   │   │   ├── layout/       # Navbar, Footer, MainLayout
│   │   │   └── common/       # Chatbot, ErrorBoundary
│   │   ├── pages/            # Route-level page components
│   │   ├── store/            # Redux store & slices
│   │   ├── hooks/            # Custom hooks (usePlanner, etc.)
│   │   ├── api/              # Axios API client
│   │   ├── data/             # Predefined itineraries data
│   │   └── utils/            # PDF and journal generators
│   ├── public/images/        # Destination images
│   └── vite.config.js
│
├── modules/                  # Legacy Python modules
│   ├── ai_planner.py
│   ├── travel_coach.py
│   ├── journal.py
│   ├── tts_service.py
│   ├── hotel_booking.py
│   ├── flight_booking.py
│   └── ...
│
├── data/                     # Runtime data (gitignored)
├── .gitignore
├── requirements.txt          # Root Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.10+
- **Node.js** 18+
- **Git**
- A **Google Gemini API key**

---

### 1. Clone the Repository

```bash
git clone https://github.com/ayshanassar1/Travelume.git
cd Travelume
```

---

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_jwt_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 3. Set Up the Backend

```bash
# Install dependencies (if not already done)
pip install -r backend/requirements.txt

# Start the backend server from the project root
npm run dev:api
```

Backend runs at: `http://localhost:8001`  
API docs available at: `http://localhost:8001/docs`

---

### 4. Set Up the Frontend

```bash
# Start the frontend from the project root (in a new terminal)
npm run dev:frontend
```

Frontend runs at: `http://localhost:5173`

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/trips/` | Get all saved trips |
| POST | `/trips/` | Save a new trip |
| GET | `/journals/` | Get all travel journals |
| POST | `/journals/` | Create a new journal |
| POST | `/planner/generate` | Generate AI itinerary |
| POST | `/chat/message` | Send message to travel coach |

---

## 🛡️ Security Notes

- User passwords are hashed with **bcrypt**
- All protected routes require a **JWT Bearer token**
- Sensitive data files (`users.json`, `trips/`, `journals/`) are **gitignored** and never committed
- API keys are stored in `.env` (also gitignored)

---

## 📸 Screenshots

> _Coming soon_

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is for educational and personal use.

---

## 👩‍💻 Author

**Aysha Nassar** — [github.com/ayshanassar1](https://github.com/ayshanassar1)
