/**
 * Sarkari Sahayak Audio Recorder
 * Records voice from browser microphone and uploads to Sarvam STT (Saaras v4)
 */

class AudioVoiceRecorder {
  constructor(options = {}) {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.isRecording = false;
    this.stream = null;
    this.timerInterval = null;
    this.secondsRecorded = 0;

    this.onStart = options.onStart || (() => {});
    this.onStop = options.onStop || (() => {});
    this.onTick = options.onTick || (() => {});
    this.onError = options.onError || ((err) => alert("Microphone Error: " + err));
  }

  async start() {
    if (this.isRecording) return;

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true
        } 
      });

      // Select mimeType supported by browser
      let mimeType = 'audio/webm';
      if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
        mimeType = 'audio/webm;codecs=opus';
      } else if (MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) {
        mimeType = 'audio/ogg;codecs=opus';
      } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
        mimeType = 'audio/mp4';
      }

      this.mediaRecorder = new MediaRecorder(this.stream, { mimeType });
      this.audioChunks = [];

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { type: mimeType });
        this.onStop(audioBlob);
        this.cleanup();
      };

      this.mediaRecorder.start(250); // collect 250ms chunks
      this.isRecording = true;
      this.secondsRecorded = 0;
      this.timerInterval = setInterval(() => {
        this.secondsRecorded++;
        this.onTick(this.secondsRecorded);
      }, 1000);

      this.onStart();
    } catch (err) {
      console.error("Microphone access error:", err);
      this.onError(err.message || "Microphone access denied or not available.");
      this.cleanup();
    }
  }

  stop() {
    if (!this.isRecording || !this.mediaRecorder) return;
    try {
      this.mediaRecorder.stop();
    } catch (e) {
      console.warn("Stop error:", e);
    }
    this.isRecording = false;
    clearInterval(this.timerInterval);
  }

  cleanup() {
    if (this.stream) {
      this.stream.getTracks().forEach((track) => track.stop());
      this.stream = null;
    }
    clearInterval(this.timerInterval);
    this.isRecording = false;
  }
}

window.AudioVoiceRecorder = AudioVoiceRecorder;
