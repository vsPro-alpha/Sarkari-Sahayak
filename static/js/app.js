/**
 * Sarkari Sahayak & Grievance Drafter Application Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // State
  let currentAudio = null;
  let activeTab = "voice-tab";

  // Elements
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabPanels = document.querySelectorAll(".tab-panel");
  const statusBadge = document.getElementById("api-status-badge");
  const statusText = document.getElementById("api-status-text");
  const statusDot = document.getElementById("status-dot");

  // Settings Modal
  const settingsModal = document.getElementById("settings-modal");
  const btnSettings = document.getElementById("btn-settings");
  const btnCloseSettings = document.getElementById("btn-close-settings");
  const btnSaveSettings = document.getElementById("btn-save-settings");
  const inputApiKey = document.getElementById("sarvam-api-key-input");

  // Voice Tab Elements
  const btnRecordVoice = document.getElementById("btn-record-voice");
  const voiceTimer = document.getElementById("voice-timer");
  const voiceStatusText = document.getElementById("voice-status-text");
  const voiceInputText = document.getElementById("voice-input-text");
  const voiceLangSelect = document.getElementById("voice-language-select");
  const btnAnalyzeVoice = document.getElementById("btn-analyze-voice");
  const voiceResultsArea = document.getElementById("voice-results-area");

  // Grievance Tab Elements
  const grievanceTextInput = document.getElementById("grievance-text-input");
  const citizenNameInput = document.getElementById("citizen-name");
  const citizenLocationInput = document.getElementById("citizen-location");
  const citizenPhoneInput = document.getElementById("citizen-phone");
  const btnDraftGrievance = document.getElementById("btn-draft-grievance");
  const grievanceResultCard = document.getElementById("grievance-result-card");
  const petitionViewerEn = document.getElementById("petition-viewer-en");
  const petitionViewerHi = document.getElementById("petition-viewer-hi");
  const refBadge = document.getElementById("ref-badge");
  const ministryBadge = document.getElementById("ministry-badge");
  const timeframeBadge = document.getElementById("timeframe-badge");
  const btnCopyEn = document.getElementById("btn-copy-en");
  const btnCopyHi = document.getElementById("btn-copy-hi");
  const btnCopyCpgrams = document.getElementById("btn-copy-cpgrams");
  const btnPrintPetition = document.getElementById("btn-print-petition");

  // Document Scanner Elements
  const fileInputDoc = document.getElementById("doc-file-input");
  const btnUploadDoc = document.getElementById("btn-upload-doc");
  const docScanResult = document.getElementById("doc-scan-result");

  // Schemes Tab Elements
  const profileForm = document.getElementById("profile-form");
  const schemesContainer = document.getElementById("schemes-container");

  // 1. Initialize Health & Check API Status
  async function checkHealth() {
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      if (data.sarvam_api_connected) {
        statusDot.className = "status-dot";
        statusText.innerText = "Sarvam AI Live";
        statusBadge.title = `STT: ${data.models.stt} | TTS: ${data.models.tts}`;
      } else {
        statusDot.className = "status-dot inactive";
        statusText.innerText = "Simulation Mode (Add Key)";
        statusBadge.title = "Click Settings to add SARVAM_API_KEY for live models";
      }
    } catch (err) {
      console.warn("Health check failed:", err);
      statusDot.className = "status-dot inactive";
      statusText.innerText = "Offline";
    }
  }
  checkHealth();

  // 2. Tab Navigation
  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-tab");
      tabBtns.forEach((b) => b.classList.remove("active"));
      tabPanels.forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(target).classList.add("active");
      activeTab = target;

      if (target === "directory-tab") {
        loadSchemesDirectory();
      }
    });
  });

  // 3. Audio Recorder Setup
  const recorder = new AudioVoiceRecorder({
    onStart: () => {
      btnRecordVoice.classList.add("recording");
      voiceStatusText.innerText = "Listening... Speak your issue in Hindi or your native tongue";
      voiceTimer.style.display = "inline-block";
    },
    onTick: (secs) => {
      voiceTimer.innerText = `00:${secs < 10 ? '0' : ''}${secs}`;
    },
    onStop: async (audioBlob) => {
      btnRecordVoice.classList.remove("recording");
      voiceStatusText.innerText = "Processing audio with Sarvam Saaras v4...";
      voiceTimer.style.display = "none";
      await uploadVoiceForTranscription(audioBlob);
    },
    onError: (err) => {
      btnRecordVoice.classList.remove("recording");
      voiceStatusText.innerText = "Microphone error: " + err;
    }
  });

  btnRecordVoice.addEventListener("click", () => {
    if (recorder.isRecording) {
      recorder.stop();
    } else {
      recorder.start();
    }
  });

  async function uploadVoiceForTranscription(audioBlob) {
    const formData = new FormData();
    formData.append("file", audioBlob, "citizen_voice.webm");
    formData.append("language_code", voiceLangSelect.value);

    try {
      const res = await fetch("/api/voice/transcribe", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      if (data.success && data.transcript) {
        voiceInputText.value = data.transcript;
        voiceStatusText.innerText = data.simulated 
          ? "Transcribed (Simulated Saaras):" 
          : "Transcribed via Sarvam Saaras v4:";
      } else {
        voiceStatusText.innerText = "Could not transcribe audio. Please type below.";
      }
    } catch (err) {
      voiceStatusText.innerText = "Transcription failed: " + err.message;
    }
  }

  // Sample Chips Click Handler
  document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const sampleText = chip.getAttribute("data-sample");
      if (voiceInputText) voiceInputText.value = sampleText;
      if (grievanceTextInput) grievanceTextInput.value = sampleText;
    });
  });

  // Audio Player Helper
  function playAudioBase64(base64Data) {
    if (!base64Data) return;
    if (currentAudio) {
      currentAudio.pause();
    }
    const audioUrl = `data:audio/wav;base64,${base64Data}`;
    currentAudio = new Audio(audioUrl);
    currentAudio.play().catch(e => console.warn("Audio play prevented:", e));
  }

  // 4. Voice Tab Analysis Button
  btnAnalyzeVoice.addEventListener("click", async () => {
    const text = voiceInputText.value.trim();
    if (!text) {
      alert("Please speak or enter your issue first.");
      return;
    }

    voiceResultsArea.innerHTML = `<div style="text-align:center; padding: 2rem;">Analyzing with Sarvam Indic Reasoning...</div>`;

    // Detect if this is grievance or scheme inquiry
    const isGrievanceKeywords = ["nahi mila", "band ho gaya", "jal gaya", "shikayat", "bhrashtachar", "pareshan", "roka", "kharab", "sewer", "kotedar", "broken", "complaint"];
    const isGrievance = isGrievanceKeywords.some(k => text.toLowerCase().includes(k));

    if (isGrievance) {
      // Draft Grievance
      try {
        const res = await fetch("/api/grievance/draft", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            raw_text: text,
            citizen_name: citizenNameInput ? citizenNameInput.value : "Citizen",
            location: citizenLocationInput ? citizenLocationInput.value : "Rural District",
            language_code: voiceLangSelect.value,
            generate_audio: true
          })
        });
        const draft = await res.json();
        renderGrievanceCard(draft, voiceResultsArea);
        if (draft.spoken_audio) {
          playAudioBase64(draft.spoken_audio);
        }
      } catch (e) {
        voiceResultsArea.innerHTML = `<div style="color:red;">Error: ${e.message}</div>`;
      }
    } else {
      // Match Schemes
      try {
        const res = await fetch("/api/schemes/match", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            age: 35,
            occupation: text.includes("kisan") ? "farmer" : "artisan",
            language_code: voiceLangSelect.value
          })
        });
        const schemeRes = await res.json();
        renderSchemesResults(schemeRes, voiceResultsArea);
        if (schemeRes.spoken_audio) {
          playAudioBase64(schemeRes.spoken_audio);
        }
      } catch (e) {
        voiceResultsArea.innerHTML = `<div style="color:red;">Error: ${e.message}</div>`;
      }
    }
  });

  // Render Grievance Card
  function renderGrievanceCard(draft, container) {
    container.innerHTML = `
      <div class="card" style="border-left: 4px solid var(--saffron);">
        <div class="card-header">
          <div class="card-title">⚖️ CPGRAMS Grievance Petition Generated</div>
          <span class="status-badge" style="background:#eff6ff; color:#1e3a8a;">Ref: ${draft.reference_id}</span>
        </div>
        <p style="margin-bottom: 0.5rem;"><strong>Target Ministry:</strong> ${draft.ministry}</p>
        <p style="margin-bottom: 0.5rem;"><strong>Legal Citation:</strong> <span style="color:#0369a1;">${draft.act_citation}</span></p>
        <p style="margin-bottom: 1rem;"><strong>Resolution Timeframe:</strong> <span style="color:#b45309; font-weight:700;">${draft.stipulated_timeframe}</span></p>

        <div style="display:flex; gap:0.5rem; margin-bottom:1rem; flex-wrap:wrap;">
          <button class="btn-outline" id="play-draft-audio">🔊 Listen (Bulbul Voice)</button>
          <button class="btn-outline" id="view-in-drafter-tab">📄 Open Full Dual-Language Drafter</button>
        </div>

        <div class="petition-box">${escapeHtml(draft.petition_hindi)}</div>
      </div>
    `;

    document.getElementById("play-draft-audio")?.addEventListener("click", () => {
      if (draft.spoken_audio) playAudioBase64(draft.spoken_audio);
    });

    document.getElementById("view-in-drafter-tab")?.addEventListener("click", () => {
      document.querySelector('[data-tab="grievance-tab"]').click();
      populateGrievanceTab(draft);
    });
  }

  // Populate Grievance Tab Directly
  function populateGrievanceTab(draft) {
    grievanceResultCard.style.display = "block";
    refBadge.innerText = `Ref: ${draft.reference_id}`;
    ministryBadge.innerText = draft.ministry;
    timeframeBadge.innerText = `Timeframe: ${draft.stipulated_timeframe}`;
    petitionViewerEn.textContent = draft.petition_english;
    petitionViewerHi.textContent = draft.petition_hindi;

    // Attach copy actions
    btnCopyEn.onclick = () => copyText(draft.petition_english, "English Petition Copied!");
    btnCopyHi.onclick = () => copyText(draft.petition_hindi, "Hindi Petition Copied!");
    btnCopyCpgrams.onclick = () => copyText(draft.cpgrams_compact, "CPGRAMS Portal Text Copied!");
    btnPrintPetition.onclick = () => window.print();
  }

  // 5. Grievance Tab Form Submission
  btnDraftGrievance.addEventListener("click", async () => {
    const rawText = grievanceTextInput.value.trim();
    if (!rawText) {
      alert("Please enter the grievance narrative.");
      return;
    }

    btnDraftGrievance.innerText = "Drafting with Legal Acts...";
    try {
      const res = await fetch("/api/grievance/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          raw_text: rawText,
          citizen_name: citizenNameInput.value || "Aggrieved Citizen",
          location: citizenLocationInput.value || "India",
          contact_phone: citizenPhoneInput.value || "+91 98765 43210",
          generate_audio: true
        })
      });
      const draft = await res.json();
      populateGrievanceTab(draft);
      if (draft.spoken_audio) {
        playAudioBase64(draft.spoken_audio);
      }
    } catch (e) {
      alert("Drafting failed: " + e.message);
    } finally {
      btnDraftGrievance.innerText = "Generate Formal CPGRAMS Petition";
    }
  });

  // 6. Schemes Profile Form Matching
  profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      age: parseInt(document.getElementById("prof-age").value) || 30,
      gender: document.getElementById("prof-gender").value,
      occupation: document.getElementById("prof-occupation").value,
      annual_income_lakhs: parseFloat(document.getElementById("prof-income").value) || 1.5,
      has_land: document.getElementById("prof-land").checked,
      is_rural: document.getElementById("prof-rural").checked,
      is_taxpayer: document.getElementById("prof-taxpayer").checked,
      language_code: "hi-IN"
    };

    schemesContainer.innerHTML = `<div style="text-align:center; padding:2rem;">Matching against Central & State schemes database...</div>`;

    try {
      const res = await fetch("/api/schemes/match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      renderSchemesResults(data, schemesContainer);
      if (data.spoken_audio) {
        playAudioBase64(data.spoken_audio);
      }
    } catch (e) {
      schemesContainer.innerHTML = `<div style="color:red;">Error: ${e.message}</div>`;
    }
  });

  function renderSchemesResults(data, container) {
    let html = `
      <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:1rem; margin-bottom:1.5rem;">
        <h4 style="color:#1e3a8a; margin-bottom:0.25rem;">🎙️ AI Sahayak Spoken Guidance</h4>
        <p style="color:#1e293b; font-size:0.95rem;">${data.hindi_summary}</p>
      </div>
      <h3 style="margin-bottom:1rem; color:#0f172a;">Matched Welfare Schemes (${data.total_matched || 0})</h3>
      <div class="grid-2">
    `;

    const allSchemes = [...(data.eligible_schemes || []), ...(data.potential_schemes || [])];
    if (allSchemes.length === 0) {
      html += `<p>No matching schemes found for this criteria. Try adjusting income or occupation.</p>`;
    } else {
      allSchemes.forEach((s) => {
        const isEligible = s.status === "ELIGIBLE";
        html += `
          <div class="scheme-card">
            <div>
              <span class="scheme-badge ${isEligible ? 'badge-eligible' : 'badge-partial'}">
                ${isEligible ? '✓ Fully Eligible (पात्र)' : '⚠️ Check Requirements'}
              </span>
              <h4 style="color:#1e3a8a; margin-bottom:0.25rem;">${s.hindi_name}</h4>
              <p style="font-size:0.8rem; color:#64748b; margin-bottom:0.5rem;">${s.name} • ${s.ministry}</p>
              <p style="font-size:0.88rem; margin-bottom:0.75rem;">${s.hindi_benefit}</p>
              
              <div style="font-size:0.8rem; background:#f8fafc; padding:0.5rem; border-radius:6px; margin-bottom:0.75rem;">
                <strong>Required Documents:</strong>
                <ul style="margin-left:1.2rem; margin-top:0.25rem;">
                  ${(s.documents || []).map(d => `<li>${d}</li>`).join('')}
                </ul>
              </div>
            </div>
            <a href="${s.official_url}" target="_blank" class="btn-outline" style="text-align:center; justify-content:center; text-decoration:none;">
              Apply on Official Portal ↗
            </a>
          </div>
        `;
      });
    }
    html += `</div>`;
    container.innerHTML = html;
  }

  // 7. Document Scanner
  btnUploadDoc.addEventListener("click", async () => {
    const file = fileInputDoc.files[0];
    if (!file) {
      alert("Please select a photo or document file first.");
      return;
    }

    docScanResult.innerHTML = `<div style="text-align:center; padding:2rem;">Scanning with Sarvam Document Intelligence...</div>`;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("auto_match_schemes", "true");

    try {
      const res = await fetch("/api/document/parse", {
        method: "POST",
        body: formData
      });
      const result = await res.json();
      
      const p = result.extracted_profile;
      docScanResult.innerHTML = `
        <div class="card" style="border-left: 4px solid var(--green);">
          <div class="card-header">
            <div class="card-title">🪪 Document Extracted: ${result.document_type}</div>
            <span class="status-badge" style="background:#dcfce7; color:#166534;">Verified</span>
          </div>
          <p style="margin-bottom:1rem; color:#475569;">${result.extracted_summary}</p>
          
          <div class="grid-3" style="margin-bottom:1.25rem; font-size:0.9rem;">
            <div><strong>Name:</strong> ${p.name}</div>
            <div><strong>Age:</strong> ${p.age} years</div>
            <div><strong>Gender:</strong> ${p.gender}</div>
            <div><strong>Location:</strong> ${p.district}, ${p.state}</div>
            <div><strong>Landholding:</strong> ${p.land_area}</div>
            <div><strong>Est. Income:</strong> ₹${p.annual_income_lakhs} Lakhs/yr</div>
          </div>

          <button class="btn-saffron" id="btn-use-profile">Apply Profile to Scheme Matcher</button>
        </div>
      `;

      document.getElementById("btn-use-profile")?.addEventListener("click", () => {
        document.querySelector('[data-tab="schemes-tab"]').click();
        document.getElementById("prof-age").value = p.age;
        document.getElementById("prof-income").value = p.annual_income_lakhs;
        document.getElementById("prof-land").checked = p.has_land;
        document.getElementById("profile-form").dispatchEvent(new Event("submit"));
      });
    } catch (e) {
      docScanResult.innerHTML = `<div style="color:red;">Scan failed: ${e.message}</div>`;
    }
  });

  // 8. Schemes Directory Loader
  async function loadSchemesDirectory() {
    const dirContainer = document.getElementById("directory-container");
    if (!dirContainer) return;
    dirContainer.innerHTML = "Loading schemes catalog...";
    try {
      const res = await fetch("/api/schemes/list");
      const data = await res.json();
      let html = `<div class="grid-2">`;
      data.schemes.forEach((s) => {
        html += `
          <div class="scheme-card">
            <div>
              <span class="scheme-badge" style="background:#e0e7ff; color:#3730a3;">${s.category}</span>
              <h4 style="color:#1e3a8a; margin-bottom:0.25rem;">${s.hindi_name}</h4>
              <p style="font-size:0.8rem; color:#64748b; margin-bottom:0.5rem;">${s.name} • ${s.ministry}</p>
              <p style="font-size:0.88rem; margin-bottom:0.75rem;">${s.hindi_benefit}</p>
              <div style="font-size:0.8rem; margin-bottom:0.5rem; color:#475569;">
                <strong>Application Steps:</strong>
                <ol style="margin-left:1.2rem; margin-top:0.25rem;">
                  ${(s.application_steps || []).map(step => `<li>${step}</li>`).join('')}
                </ol>
              </div>
            </div>
            <a href="${s.official_url}" target="_blank" class="btn-outline" style="text-align:center; justify-content:center; text-decoration:none;">
              Portal Link ↗
            </a>
          </div>
        `;
      });
      html += `</div>`;
      dirContainer.innerHTML = html;
    } catch (e) {
      dirContainer.innerHTML = `<div style="color:red;">Error loading directory: ${e.message}</div>`;
    }
  }

  // Settings Modal Controls
  btnSettings.addEventListener("click", () => settingsModal.classList.add("active"));
  btnCloseSettings.addEventListener("click", () => settingsModal.classList.remove("active"));
  btnSaveSettings.addEventListener("click", async () => {
    const key = inputApiKey.value.trim();
    try {
      const res = await fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: key })
      });
      const data = await res.json();
      alert(data.message);
      settingsModal.classList.remove("active");
      checkHealth();
    } catch (e) {
      alert("Error updating key: " + e.message);
    }
  });

  // Utilities
  function copyText(text, alertMsg) {
    navigator.clipboard.writeText(text).then(() => {
      alert(alertMsg || "Copied to clipboard!");
    });
  }

  function escapeHtml(string) {
    const div = document.createElement('div');
    div.innerText = string;
    return div.innerHTML;
  }
});
