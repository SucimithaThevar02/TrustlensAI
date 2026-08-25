import os
import whisper

from detect import detect_scam


# ==========================================
# AUDIO FILE
# ==========================================

audio_file = "audio/converted_audio.wav"


if not os.path.exists(audio_file):

    print("Audio file not found!")
    print("Looking for:", os.path.abspath(audio_file))
    exit()


# ==========================================
# WHISPER SPEECH RECOGNITION
# ==========================================

print("================================")
print("Processing audio...")
print("Please wait...")
print("Audio:", audio_file)
print("================================")


try:

    print("\nLoading Whisper model...")

    # Use a better model than "base" for improved recognition.
    # If your computer is slow, change this back to "base".
    model = whisper.load_model("small")


    print("Converting speech to text...")


    # ==========================================
    # WHISPER TRANSCRIPTION
    # ==========================================

    result = model.transcribe(

        audio_file,

        # Automatically detect the spoken language
        language=None,

        # Speech-to-text
        task="transcribe",

        # Better accuracy for real-world audio
        temperature=0,

        # Helps Whisper use previous context
        condition_on_previous_text=True,

        # Do not use FP16 on CPU
        fp16=False
    )


    # ==========================================
    # GET TRANSCRIPTION
    # ==========================================

    text = result["text"].strip()


    # ==========================================
    # GET DETECTED LANGUAGE
    # ==========================================

    detected_language = result.get(
        "language",
        "unknown"
    )


    # ==========================================
    # TRANSCRIPTION
    # ==========================================

    print("\n===== AUDIO TRANSCRIPTION =====")

    print("\nDetected Language:")
    print(detected_language)


    print("\nTranscription:")

    print(text)


    # ==========================================
    # CHECK EMPTY TRANSCRIPTION
    # ==========================================

    if not text:

        print("\nNo speech could be detected in the audio.")

        exit()


    # ==========================================
    # TRUSTLENS AI ANALYSIS
    # ==========================================

    print("\n===== TRUSTLENS AI ANALYSIS =====")


    result = detect_scam(text)


    print("\nLanguage:")

    print(result["language"])


    print("\nScam Probability:")

    print(str(result["probability"]) + "%")


    print("\nRisk Level:")

    print(result["risk"])


    print("\nStatus:")

    print(result["status"])


    print("\nReasons:")

    for reason in result["reasons"]:

        print("-", reason)


    print("\nSafety Tips:")

    for tip in result["tips"]:

        print("-", tip)


except Exception as e:

    print("\nError:")

    print(e)