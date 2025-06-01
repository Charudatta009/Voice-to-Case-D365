let recognition;
let isRecording = false;
let transcriptText = '';

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const status = document.getElementById("status");
const transcriptDiv = document.getElementById("transcript");

function initRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recog = new SpeechRecognition();
  recog.lang = 'en-US';
  recog.continuous = true;
  recog.interimResults = false;

  recog.onresult = (event) => {
    for (let i = event.resultIndex; i < event.results.length; i++) {
      if (event.results[i].isFinal) {
        transcriptText += event.results[i][0].transcript + '\n';
      }
    }
    transcriptDiv.innerHTML = `<span class="transcript-label">You said:</span><br>${transcriptText}`;
    
    // Add typing animation effect
    transcriptDiv.classList.add("typing");
    setTimeout(() => {
      transcriptDiv.classList.remove("typing");
    }, 500);
  };

  recog.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    status.innerHTML = `<i class="fas fa-exclamation-circle"></i> Error: ${event.error}`;
    status.parentElement.style.background = "rgba(214, 48, 49, 0.1)";
  };

  recog.onend = () => {
    if (isRecording) {
      console.log("Recognition ended. Restarting...");
      recog.start(); // Restart automatically if still recording
    }
  };

  return recog;
}

startBtn.onclick = () => {
  transcriptText = '';
  transcriptDiv.innerHTML = "";
  status.innerHTML = `<i class="fas fa-circle-notch fa-spin"></i> Status: Listening...`;
  status.parentElement.style.background = "rgba(74, 107, 255, 0.1)";
  startBtn.disabled = true;
  stopBtn.disabled = false;
  isRecording = true;

  // Add recording animation
  document.querySelector('.header i').classList.add('pulse');
  
  recognition = initRecognition();
  recognition.start();
};

stopBtn.onclick = () => {
  isRecording = false;
  recognition.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
  status.innerHTML = `<i class="fas fa-circle-notch fa-spin"></i> Status: Processing...`;
  status.parentElement.style.background = "rgba(253, 203, 110, 0.1)";

  // Remove recording animation
  document.querySelector('.header i').classList.remove('pulse');

  setTimeout(() => {
    transcriptDiv.innerHTML = `<span class="transcript-label">You said:</span><br>${transcriptText}`;

    if (!transcriptText.trim()) {
      status.innerHTML = `<i class="fas fa-exclamation-circle"></i> No speech detected.`;
      status.parentElement.style.background = "rgba(214, 48, 49, 0.1)";
      return;
    }

    sendToBackend(transcriptText);
  }, 1000);
};

async function sendToBackend(text) {
  try {
    console.log("Sending transcript:", text);
    status.innerHTML = `<i class="fas fa-circle-notch fa-spin"></i> Status: Creating case...`;
    
    const response = await fetch("https://voice-to-case-d365.onrender.com/transcribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript: text })
    });

    const result = await response.json();
    console.log("Backend response:", result);

    if (response.ok) {
      status.innerHTML = `<i class="fas fa-check-circle"></i> Case created! Sentiment: ${result.sentiment}, Priority: ${result.priority}`;
      status.parentElement.style.background = "rgba(0, 184, 148, 0.1)";
      
      // Add success animation
      status.parentElement.classList.add("success-pulse");
      setTimeout(() => {
        status.parentElement.classList.remove("success-pulse");
      }, 2000);
    } else {
      status.innerHTML = `<i class="fas fa-times-circle"></i> Failed: ${result.error}`;
      status.parentElement.style.background = "rgba(214, 48, 49, 0.1)";
    }
  } catch (error) {
    status.innerHTML = `<i class="fas fa-times-circle"></i> Error: ${error.message}`;
    status.parentElement.style.background = "rgba(214, 48, 49, 0.1)";
  }
}
