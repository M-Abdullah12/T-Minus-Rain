🌦️ Climate Forecasting with LSTM & NASA Giovanni Data

🛰️ Overview

This project uses NASA Giovanni climate datasets to forecast future climate trends such as temperature and precipitation through a Long Short-Term Memory (LSTM) deep learning model. It offers users an interactive, web-based platform to visualize historical data, explore seasonal context, and predict future values for specific dates or regions.

Developed as part of the NASA Space Apps Challenge, this project represents a fusion of climate science and AI to highlight the potential of open NASA data in understanding environmental changes.

⸻

⚙️ Features
	•	🌍 Interactive visualization of NASA Giovanni climate data
	•	🤖 AI-driven LSTM model for weather and climate forecasting
	•	🗓️ Seasonal context-based predictions
	•	📊 Dual-date comparison to observe change trends
	•	🧠 AI-assisted development for refinement and optimization

⸻

🧰 Tech Stack

Component	Technology Used
Frontend	React, TypeScript, Tailwind CSS
Backend	FastAPI (Python)
Model	TensorFlow / Keras (LSTM)
Data Source	NASA Giovanni
Deployment	Vercel / Localhost
AI Assistance	ChatGPT, DeepSeek, Cursor AI


⸻

👨‍💻 Developer Note

This project was developed solo by a 20-year-old self-taught developer currently pursuing a Bachelor’s in Artificial Intelligence.
It was their first time working with NASA data or AI modeling, which required continuous learning and iteration using AI tools to meet technical requirements and deadlines.
AI assistance was used responsibly for debugging, documentation, and refining model performance — all core decisions, design logic, and integrations were performed manually.

⸻

🚀 How to Run the Project

1. Clone the Repository

git clone <your-repo-url>
cd project

2. Backend Setup

cd backend
pip install -r requirements.txt

3. Run the Backend Server

For PowerShell (Windows):

cd backend; $env:PYTHONUNBUFFERED=1; uvicorn main:app --host 0.0.0.0 --port 8000 --reload

For Mac/Linux:

cd backend && PYTHONUNBUFFERED=1 uvicorn main:app --host 0.0.0.0 --port 8000 --reload

If successful, you should see:

✅ LSTM model and artifacts loaded
[(None, 720, 9), (None, 6)]

4. Frontend Setup

In a new terminal:

npm install
npm run dev

Then open your browser at:
👉 http://localhost:5173

⸻

🧠 AI Involvement Transparency

AI tools were used to:
	•	Assist with backend debugging and FastAPI setup
	•	Refine the LSTM model and training pipeline
	•	Format the frontend with React and Tailwind CSS
	•	Generate documentation and code explanations

