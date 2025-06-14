🎤 Voice-to-Case Generator for Microsoft Dynamics 365
A voice-based customer service automation tool that listens to a user's speech, analyzes the sentiment, and creates a Case in Dynamics 365. Built using JavaScript (frontend), Flask (backend), and integrated with Azure Cognitive Services, Dynamics 365 Web API and one importan flow to invoke HTTP request.

📌 Features
✅ Real-time voice recognition using Web Speech API

✅ Transcription display in browser

✅ Sentiment analysis using Azure Text Analytics API

✅ Intelligent Priority classification based on text content

✅ Case creation in Dynamics 365 Customer Service

✅ Authentication via Azure Active Directory (OAuth 2.0)

✅ Full-stack deployment (frontend + backend)

✅ Backend hosted on Render.com

✅ Designed for Power Platform extensibility (Power Automate, Power Pages)

📂 Tech Stack
🎧 Frontend: HTML5, JavaScript (Web Speech API)

🧠 Backend: Python (Flask)

☁️ AI Services: Azure Cognitive Services (Text Analytics)

💬 CRM: Microsoft Dynamics 365 Web API

🔐 Auth: Azure AD + App Registration

🚀 Deployment: Render.com (Flask API)

💻 Version Control: GitHub

📈 Use Case
 -This project is ideal for:

 -Contact center automation

 -Voice-based incident/ticket creation

 -Field agent or voice assistant integrations

 -Internal CRM tools

🚀 How It Works
 -User clicks Start Recording on the frontend.
 ![image](https://github.com/user-attachments/assets/d309345a-4dd5-49d7-a0aa-1d9639852a8f)



 -Browser listens to speech and displays the live transcript.
 ![Screenshot 2025-06-01 161054](https://github.com/user-attachments/assets/fc399be7-5c78-4a7b-a8d9-55a75e9681f6)


 -On stopping, transcript is sent to the backend to trigger the D365 flow.

 -Backend analyzes sentiment and derives priority.

 -Backend creates a Case record in D365 with the extracted details by triggering the flow.
 ![Screenshot 2025-06-01 161257](https://github.com/user-attachments/assets/d1e3872d-441c-40b9-a80b-6e46fcb1fcc0)


 -Success message is shown on the UI.
