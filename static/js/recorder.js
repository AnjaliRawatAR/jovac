let audioContext;
let recorder;
let audioChunks = [];
let isRecording = false;

document.getElementById('recordButton').addEventListener('click', () => {
    startRecording();
});

document.getElementById('stopButton').addEventListener('click', () => {
    stopRecording();
});

function startRecording() {
    if (isRecording) return;

    isRecording = true;
    audioChunks = [];
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            audioContext = new AudioContext();
            const input = audioContext.createMediaStreamSource(stream);
            recorder = new MediaRecorder(stream);

            recorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            recorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                document.getElementById('audioPlayback').src = audioUrl;

                // Send the audio to the server
                const formData = new FormData();
                formData.append('audio_data', audioBlob, 'recording.wav');

                fetch('/upload', {
                    method: 'POST',
                    body: formData
                }).then(response => response.blob())
                  .then(data => {
                      const processedAudioUrl = URL.createObjectURL(data);
                      document.getElementById('audioPlayback').src = processedAudioUrl;
                  });
            };

            recorder.start();
            document.getElementById('recordButton').disabled = true;
            document.getElementById('stopButton').disabled = false;
        });
}

function stopRecording() {
    if (!isRecording) return;

    isRecording = false;
    recorder.stop();
    document.getElementById('recordButton').disabled = false;
    document.getElementById('stopButton').disabled = true;
}
