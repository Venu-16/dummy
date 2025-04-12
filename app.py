import streamlit as st
import speech_recognition as sr
import time

def recognize_speech():
    r = sr.Recognizer()
    audio_data = []

    with sr.Microphone() as source:
        st.info("Speak now... (3-second pause max, 15 sec total)")
        r.adjust_for_ambient_noise(source)
        end_time = time.time() + 15
        last_audio_time = time.time()

        while time.time() < end_time:
            try:
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                audio_data.append(audio)
                last_audio_time = time.time()
            except sr.WaitTimeoutError:
                if time.time() - last_audio_time > 3:
                    st.warning("Paused too long. Stopping.")
                    break
                else:
                    continue

        st.success("Recording done!")

    # Combine audio
    combined_audio = sr.AudioData(
        b''.join([a.get_raw_data() for a in audio_data]),
        audio_data[0].sample_rate if audio_data else 16000,
        audio_data[0].sample_width if audio_data else 2
    )

    # Speech recognition
    try:
        text = r.recognize_google(combined_audio)
        return text
    except sr.UnknownValueError:
        st.error("Could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"API Error: {e}")

    return ""

# --- Streamlit UI ---

st.title("🎤 Speech to Text Field")
st.write("Click below to record your voice and convert it to text.")

if st.button("🎙 Start Recording"):
    transcript = recognize_speech()
    if transcript:
        st.text_input("Your Speech as Text:", value=transcript, key="speech_input")