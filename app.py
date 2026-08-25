from flask import Flask, render_template, request, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

from detect import detect_scam
from link_detector import detect_links
from database import create_table, save_report
from ocr import extract_text

from translator import (
    translate_text,
    detect_language,
    translate_analysis
)

# ==========================================================
# AUDIO IMPORTS
# ==========================================================

import whisper
from gtts import gTTS


app = Flask(__name__)


# ==========================================================
# SCAM ALERT SOUND
# ==========================================================
# Put siren.mpeg inside:
#
# TrustLensAI/static/siren.mpeg
#
# The sound will be sent to result.html ONLY when
# a scam is detected.

ALERT_SOUND = "siren.mpeg"


# ==========================================================
# WHISPER AUDIO MODEL
# ==========================================================
# CHANGED:
# base -> medium for better speech recognition accuracy
# Whisper will automatically detect English / Hindi /
# Marathi / Hinglish / mixed speech.

whisper_model = whisper.load_model("medium")


# ==========================================================
# UPLOAD SETTINGS
# ==========================================================

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",

    # Audio formats
    "wav",
    "mp3",
    "m4a",
    "webm",
    "ogg",
    "flac",
    "aac",
    "wma",
    "mp4",
    "mpeg",
    "mpga"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================================================
# GENERATED AUDIO SETTINGS
# ==========================================================

AUDIO_OUTPUT_FOLDER = "generated_audio"

os.makedirs(
    AUDIO_OUTPUT_FOLDER,
    exist_ok=True
)


# ==========================================================
# DASHBOARD STATISTICS
# ==========================================================

DASHBOARD_FILE = "dashboard_stats.json"


# ==========================================================
# DEFAULT DASHBOARD DATA
# ==========================================================

def get_default_dashboard_data():

    return {

        "messages_checked": 0,

        "links_checked": 0,

        "reports": 0,

        "translations": 0,

        "safe_messages": 0,

        "scam_messages": 0,

        "high_risk": 0,

        "medium_risk": 0,

        "low_risk": 0,

        "languages": {

            "English": 0,

            "Hindi": 0,

            "Marathi": 0,

            "Hinglish": 0,

            "Other": 0

        },

        "scam_categories": {

            "Bank / UPI": 0,

            "Job / Internship": 0,

            "Lottery / Prize": 0,

            "KYC / Account": 0,

            "Phishing": 0,

            "Investment": 0,

            "Shopping / Delivery": 0,

            "Social Media": 0,

            "Other": 0

        },

        "report_categories": {

            "Bank / UPI": 0,

            "Job / Internship": 0,

            "Lottery / Prize": 0,

            "KYC / Account": 0,

            "Phishing": 0,

            "Investment": 0,

            "Shopping / Delivery": 0,

            "Social Media": 0,

            "Other": 0

        },

        "alerts": 0,

        "activity": [],

        "daily_activity": {}

    }


# ==========================================================
# CREATE DASHBOARD FILE
# ==========================================================

def create_dashboard_file():

    if not os.path.exists(DASHBOARD_FILE):

        data = get_default_dashboard_data()

        with open(
            DASHBOARD_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )


create_dashboard_file()


# ==========================================================
# LOAD DASHBOARD DATA
# ==========================================================

def load_dashboard_data():

    try:

        with open(
            DASHBOARD_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        defaults = get_default_dashboard_data()

        for key, value in defaults.items():

            if key not in data:

                data[key] = value

        for language in defaults["languages"]:

            data["languages"].setdefault(
                language,
                0
            )

        for category in defaults["scam_categories"]:

            data["scam_categories"].setdefault(
                category,
                0
            )

        for category in defaults["report_categories"]:

            data["report_categories"].setdefault(
                category,
                0
            )

        return data

    except Exception:

        return get_default_dashboard_data()


# ==========================================================
# SAVE DASHBOARD DATA
# ==========================================================

def save_dashboard_data(data):

    with open(
        DASHBOARD_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# DETECT SCAM CATEGORY
# ==========================================================

def detect_scam_category(message):

    text = str(message).lower()

    bank_words = [
        "bank",
        "upi",
        "account",
        "debit",
        "credit",
        "transaction",
        "atm",
        "payment",
        "refund",
        "banking",
        "वेतन",
        "बँक",
        "upi"
    ]

    if any(word in text for word in bank_words):

        return "Bank / UPI"

    job_words = [
        "job",
        "jobs",
        "career",
        "internship",
        "intern",
        "work from home",
        "work-from-home",
        "salary",
        "vacancy",
        "hiring",
        "recruitment",
        "employment",
        "नोकरी",
        "जॉब",
        "इंटर्नशिप",
        "भरती"
    ]

    if any(word in text for word in job_words):

        return "Job / Internship"

    lottery_words = [
        "lottery",
        "prize",
        "winner",
        "won",
        "reward",
        "lucky draw",
        "cash prize",
        "gift",
        "jackpot",
        "लॉटरी",
        "बक्षीस",
        "इनाम",
        "विजेता"
    ]

    if any(word in text for word in lottery_words):

        return "Lottery / Prize"

    kyc_words = [
        "kyc",
        "verify account",
        "verification",
        "aadhaar",
        "aadhar",
        "pan card",
        "pan",
        "update kyc",
        "account blocked",
        "account suspended",
        "खाता",
        "केवायसी",
        "आधार",
        "पॅन"
    ]

    if any(word in text for word in kyc_words):

        return "KYC / Account"

    phishing_words = [
        "click here",
        "verify now",
        "login",
        "password",
        "username",
        "credentials",
        "reset password",
        "secure your account",
        "click the link",
        "link",
        "http://",
        "https://"
    ]

    if any(word in text for word in phishing_words):

        return "Phishing"

    investment_words = [
        "investment",
        "invest",
        "trading",
        "crypto",
        "bitcoin",
        "profit",
        "returns",
        "stock",
        "double your money",
        "guaranteed return",
        "investment plan",
        "निवेश",
        "गुंतवणूक"
    ]

    if any(word in text for word in investment_words):

        return "Investment"

    shopping_words = [
        "amazon",
        "flipkart",
        "delivery",
        "courier",
        "parcel",
        "order",
        "shopping",
        "package",
        "delivery failed",
        "delivery charge",
        "ऑर्डर",
        "पार्सल",
        "डिलिव्हरी"
    ]

    if any(word in text for word in shopping_words):

        return "Shopping / Delivery"

    social_words = [
        "instagram",
        "facebook",
        "whatsapp",
        "telegram",
        "social media",
        "account hacked",
        "followers",
        "verification badge"
    ]

    if any(word in text for word in social_words):

        return "Social Media"

    return "Other"


# ==========================================================
# ADD DAILY ACTIVITY
# ==========================================================

def add_daily_activity(data):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    if "daily_activity" not in data:

        data["daily_activity"] = {}

    if today not in data["daily_activity"]:

        data["daily_activity"][today] = 0

    data["daily_activity"][today] += 1

    sorted_dates = sorted(
        data["daily_activity"].keys()
    )

    if len(sorted_dates) > 14:

        old_dates = sorted_dates[:-14]

        for old_date in old_dates:

            del data["daily_activity"][old_date]


# ==========================================================
# ADD DASHBOARD ACTIVITY
# ==========================================================

def add_dashboard_activity(
    activity_type,
    alert=False
):

    data = load_dashboard_data()

    activity = data.get(
        "activity",
        []
    )

    activity.append({

        "type": activity_type,

        "time": datetime.now().strftime(
            "%d %b %Y, %I:%M %p"
        )

    })

    data["activity"] = activity[-20:]

    add_daily_activity(data)

    if alert:

        data["alerts"] = (
            data.get("alerts", 0) + 1
        )

    save_dashboard_data(data)


# ==========================================================
# UPDATE MESSAGE ANALYTICS
# ==========================================================

def update_message_analytics(
    result,
    original_language,
    message
):

    data = load_dashboard_data()

    data["messages_checked"] = (
        data.get(
            "messages_checked",
            0
        ) + 1
    )

    status = str(
        result.get(
            "status",
            ""
        )
    ).lower()

    is_scam = (
        status in [
            "spam",
            "scam",
            "unsafe",
            "suspicious"
        ]
        or
        "scam" in status
        or
        "spam" in status
    )

    if is_scam:

        data["scam_messages"] = (
            data.get(
                "scam_messages",
                0
            ) + 1
        )

    else:

        data["safe_messages"] = (
            data.get(
                "safe_messages",
                0
            ) + 1
        )

    risk = str(
        result.get(
            "risk",
            ""
        )
    ).lower()

    if "high" in risk:

        data["high_risk"] = (
            data.get(
                "high_risk",
                0
            ) + 1
        )

    elif "medium" in risk:

        data["medium_risk"] = (
            data.get(
                "medium_risk",
                0
            ) + 1
        )

    else:

        data["low_risk"] = (
            data.get(
                "low_risk",
                0
            ) + 1
        )

    if original_language in [
        "English",
        "Hindi",
        "Marathi",
        "Hinglish"
    ]:

        language = original_language

    else:

        language = "Other"

    if "languages" not in data:

        data["languages"] = {}

    data["languages"].setdefault(
        language,
        0
    )

    data["languages"][language] = (
        data["languages"].get(
            language,
            0
        ) + 1
    )

    category = detect_scam_category(
        message
    )

    if "scam_categories" not in data:

        data["scam_categories"] = {}

    data["scam_categories"].setdefault(
        category,
        0
    )

    if is_scam:

        data["scam_categories"][category] = (
            data["scam_categories"].get(
                category,
                0
            ) + 1
        )

    add_daily_activity(data)

    save_dashboard_data(data)

    return is_scam


# ==========================================================
# DASHBOARD API
# ==========================================================

@app.route("/dashboard-data")
def dashboard_data():

    data = load_dashboard_data()

    return jsonify(data)


# ==========================================================
# RESET DASHBOARD
# OPTIONAL
# ==========================================================

@app.route("/reset-dashboard")
def reset_dashboard():

    data = get_default_dashboard_data()

    save_dashboard_data(data)

    return jsonify({

        "success": True,

        "message": "Dashboard reset successfully"

    })


# ==========================================================
# FILE VALIDATION
# ==========================================================

def allowed_file(filename):

    return (
        "."
        in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================================
# AUDIO TO TEXT USING WHISPER
# ==========================================================

def audio_to_text(audio_path):

    try:

        print("================================")
        print("AUDIO PROCESSING")
        print("Audio:", audio_path)
        print("================================")

        print(
            "Converting speech to text..."
        )

        result = whisper_model.transcribe(

            audio_path,

            task="transcribe",

            language=None,

            fp16=False,

            condition_on_previous_text=False,

            verbose=False

        )

        text = result.get(
            "text",
            ""
        ).strip()

        detected_language = result.get(
            "language",
            "unknown"
        )

        print(
            "Recognized Audio Text:"
        )

        print(text)

        print(
            "Detected Audio Language:"
        )

        print(detected_language)

        segments = result.get(
            "segments",
            []
        )

        if segments:

            print(
                "\n===== AUDIO SEGMENTS ====="
            )

            for segment in segments:

                start = segment.get(
                    "start",
                    0
                )

                end = segment.get(
                    "end",
                    0
                )

                segment_text = segment.get(
                    "text",
                    ""
                ).strip()

                print(
                    f"[{start:.2f}s - {end:.2f}s] {segment_text}"
                )

        print("================================")

        return text

    except Exception as e:

        print(
            "AUDIO ERROR:",
            e
        )

        return ""


# ==========================================================
# LANGUAGE NAME CONVERTER
# ==========================================================

def get_language_name(language):

    language_map = {

        "en": "English",

        "hi": "Hindi",

        "mr": "Marathi",

        "hinglish": "Hinglish",

        "English": "English",

        "Hindi": "Hindi",

        "Marathi": "Marathi",

        "Hinglish": "Hinglish"

    }

    return language_map.get(
        language,
        language
    )


# ==========================================================
# TEXT TO AUDIO
# ==========================================================

def text_to_audio(
    text,
    language
):

    language_codes = {

        "English": "en",

        "Hindi": "hi",

        "Marathi": "mr",

        "Hinglish": "en"

    }

    language_code = language_codes.get(
        language,
        "en"
    )

    filename = "trustlens_result.mp3"

    output_path = os.path.join(
        AUDIO_OUTPUT_FOLDER,
        filename
    )

    tts = gTTS(
        text=text,
        lang=language_code
    )

    tts.save(
        output_path
    )

    return filename


# ==========================================================
# SERVE GENERATED AUDIO
# ==========================================================

@app.route("/audio/<filename>")
def serve_audio(filename):

    return send_from_directory(
        AUDIO_OUTPUT_FOLDER,
        filename
    )


# ==========================================================
# CREATE DATABASE TABLE
# ==========================================================

create_table()


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
@app.route("/home")
@app.route("/home.html")
def home():

    return render_template(
        "home.html"
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
@app.route("/dashboard.html")
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ==========================================================
# CHECK SCAM MESSAGE
# ==========================================================

@app.route(
    "/check",
    methods=["POST"]
)
def check():

    message = request.form.get(
        "message",
        ""
    ).strip()

    target_language = request.form.get(
        "target_language",
        ""
    ).strip()

    audio_file = request.files.get(
        "audio"
    )

    output_format = request.form.get(
        "output_format",
        "text"
    ).strip()

    screenshot = request.files.get(
        "screenshot"
    )

    # ======================================================
    # AUDIO TO TEXT
    # ======================================================

    if audio_file and audio_file.filename:

        if not allowed_file(
            audio_file.filename
        ):

            return """
            <h1>Invalid audio file</h1>

            <p>
                Please upload WAV, MP3, M4A, WEBM, OGG,
                FLAC, AAC, WMA or supported audio.
            </p>

            <br>

            <a href="/">
                Go Back
            </a>
            """

        try:

            filename = secure_filename(
                audio_file.filename
            )

            audio_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            audio_file.save(
                audio_path
            )

            print("================================")
            print("AUDIO SCAM DETECTION")
            print("Audio:", filename)
            print("================================")

            extracted_audio_text = audio_to_text(
                audio_path
            )

            try:

                os.remove(
                    audio_path
                )

            except:

                pass

            if not extracted_audio_text:

                return """
                <h1>Could not understand audio</h1>

                <p>
                    Please upload a clear audio recording
                    and try again.
                </p>

                <br>

                <a href="/">
                    Go Back
                </a>
                """

            message = extracted_audio_text

            print("AUDIO TEXT:")
            print(message)

            print("================================")

        except Exception as e:

            print(
                "AUDIO PROCESSING ERROR:",
                e
            )

            return f"""
            <h1>Audio Error</h1>

            <p>{e}</p>

            <br>

            <a href="/">
                Go Back
            </a>
            """

    # ======================================================
    # OCR FROM SCREENSHOT
    # ======================================================

    if screenshot and screenshot.filename:

        if not allowed_file(
            screenshot.filename
        ):

            return """
            <h1>Invalid file</h1>

            <p>
                Please upload a PNG, JPG, JPEG or WEBP image.
            </p>

            <br>

            <a href="/">
                Go Back
            </a>
            """

        try:

            filename = secure_filename(
                screenshot.filename
            )

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            screenshot.save(
                image_path
            )

            print("================================")
            print("OCR SCREENSHOT DETECTION")
            print("Image:", filename)
            print("================================")

            extracted_text = extract_text(
                image_path
            ).strip()

            print("OCR TEXT:")
            print(extracted_text)

            print("================================")

            try:

                os.remove(
                    image_path
                )

            except:

                pass

            if not extracted_text:

                return """
                <h1>No text detected</h1>

                <p>
                    We could not read any text from
                    the uploaded screenshot.
                </p>

                <br>

                <a href="/">
                    Go Back
                </a>
                """

            message = extracted_text

        except Exception as e:

            print(
                "OCR ERROR:",
                e
            )

            return f"""
            <h1>OCR Error</h1>

            <p>{e}</p>

            <br>

            <a href="/">
                Go Back
            </a>
            """

    # ======================================================
    # EMPTY MESSAGE
    # ======================================================

    if not message:

        return redirect("/")

    # ======================================================
    # SCAM DETECTION
    # ======================================================

    print("================================")
    print("SCAM MESSAGE DETECTION")
    print("Message:", message)

    print(
        "Selected Target Language:",
        target_language
    )

    print("================================")

    try:

        try:

            original_language = detect_language(
                message
            )

        except Exception as e:

            print(
                "LANGUAGE DETECTION ERROR:",
                e
            )

            original_language = "Unknown"

        print(
            "Original Message Language:",
            original_language
        )

        selected_language = None

        if original_language == "English":

            selected_language = "en"

        elif original_language == "Hindi":

            selected_language = "hi"

        elif original_language == "Marathi":

            selected_language = "mr"

        elif original_language == "Hinglish":

            selected_language = "hinglish"

        print(
            "Language sent to scam model:",
            selected_language
        )

        result = detect_scam(
            message,
            selected_language
        )

        print(
            "Detection result:",
            result
        )

        is_scam = update_message_analytics(
            result,
            original_language,
            message
        )

        scam_category = detect_scam_category(
            message
        )

        print(
            "Detected Scam Category:",
            scam_category
        )

        add_dashboard_activity(
            "🔍 Message checked",
            alert=is_scam
        )

        try:

            translated = translate_analysis(
                result,
                target_language
            )

        except Exception as e:

            print(
                "ANALYSIS TRANSLATION ERROR:",
                e
            )

            translated = result.copy()

        if not translated.get("risk"):

            translated["risk"] = result["risk"]

        if not translated.get("status"):

            translated["status"] = result["status"]

        if not translated.get("language"):

            translated["language"] = result["language"]

        if not translated.get("reasons"):

            translated["reasons"] = result["reasons"]

        if not translated.get("tips"):

            translated["tips"] = result["tips"]

        if "probability" not in translated:

            translated["probability"] = result["probability"]

        print(
            "Translated analysis:",
            translated
        )

        # ==================================================
        # OPTIONAL AUDIO RESULT
        # ==================================================

        audio_result = None

        if output_format == "audio":

            try:

                audio_text = (
                    f"{translated['status']}. "
                    f"{translated['risk']}. "
                    f"Scam probability "
                    f"{translated['probability']}. "
                )

                if isinstance(
                    translated["reasons"],
                    list
                ):

                    audio_text += " ".join(
                        translated["reasons"]
                    )

                else:

                    audio_text += str(
                        translated["reasons"]
                    )

                audio_text += " Safety tips. "

                if isinstance(
                    translated["tips"],
                    list
                ):

                    audio_text += " ".join(
                        translated["tips"]
                    )

                else:

                    audio_text += str(
                        translated["tips"]
                    )

                audio_result = text_to_audio(
                    audio_text,
                    target_language
                )

                print(
                    "Audio language:",
                    target_language
                )

                print(
                    "Audio result created:",
                    audio_result
                )

            except Exception as e:

                print(
                    "AUDIO OUTPUT ERROR:",
                    e
                )

                audio_result = None

        # ==================================================
        # FINAL LANGUAGE VALUES
        # ==================================================

        try:

            original_language = detect_language(
                message
            )

        except Exception as e:

            print(
                "FINAL LANGUAGE DETECTION ERROR:",
                e
            )

            original_language = "Unknown"

        result_language = (
            target_language
            if target_language
            else "English"
        )

        print("================================")
        print("FINAL LANGUAGE INFORMATION")

        print(
            "Original Message Language:",
            original_language
        )

        print(
            "Result Language:",
            result_language
        )

        print(
            "Scam Type:",
            scam_category
        )

        print(
            "Scam Alert:",
            is_scam
        )

        print("================================")

        # ==================================================
        # SCAM ALERT SOUND
        # ==================================================
        # Only send the siren filename when a scam is detected.
        #
        # Safe result:
        #     alert_sound = None
        #
        # Scam result:
        #     alert_sound = "siren.mpeg"

        alert_sound = (
            ALERT_SOUND
            if is_scam
            else None
        )

        return render_template(

            "result.html",

            message=message,

            probability=result["probability"],

            risk=translated["risk"],

            language=original_language,

            status=translated["status"],

            reasons=translated["reasons"],

            tips=translated["tips"],

            translated_probability=translated["probability"],

            translated_risk=translated["risk"],

            translated_language=result_language,

            translated_status=translated["status"],

            translated_reasons=translated["reasons"],

            translated_tips=translated["tips"],

            target_language=result_language,

            audio_result=audio_result,

            output_format=output_format,

            scam_category=scam_category,

            # ==================================================
            # SCAM STATUS
            # ==================================================

            is_scam=is_scam,

            # ==================================================
            # SCAM ALERT SOUND
            # ONLY PRESENT FOR SCAM
            # ==================================================

            alert_sound=alert_sound

        )

    except Exception as e:

        print(
            "ERROR:",
            e
        )

        return f"""
        <h1>Something went wrong</h1>

        <p>{e}</p>

        <br>

        <a href="/">
            Go Back
        </a>
        """


# ==========================================================
# FAKE LINK DETECTION
# ==========================================================

@app.route(
    "/link-check",
    methods=["GET", "POST"]
)
@app.route(
    "/link_check.html",
    methods=["GET", "POST"]
)
def link_check():

    result = None
    category = ""
    source = ""
    link = ""

    if request.method == "POST":

        link = request.form.get(
            "link",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        source = request.form.get(
            "source",
            ""
        ).strip()

        print("================================")
        print("FAKE LINK DETECTION")
        print("Link:", link)
        print("Category:", category)
        print("Source:", source)
        print("================================")

        if not link:

            return render_template(

                "link_check.html",

                result=None,

                category=category,

                source=source,

                link=link

            )

        try:

            result = detect_links(
                link
            )

            print(
                "Link detection result:",
                result
            )

            dashboard = load_dashboard_data()

            dashboard["links_checked"] = (
                dashboard.get(
                    "links_checked",
                    0
                ) + 1
            )

            add_daily_activity(
                dashboard
            )

            save_dashboard_data(
                dashboard
            )

            link_alert = False

            if isinstance(result, dict):

                status_text = str(
                    result.get(
                        "status",
                        ""
                    )
                ).lower()

                link_alert = (
                    "unsafe" in status_text
                    or
                    "suspicious" in status_text
                    or
                    "danger" in status_text
                    or
                    "scam" in status_text
                )

            add_dashboard_activity(
                "🔗 Link checked",
                alert=link_alert
            )

        except Exception as e:

            print(
                "LINK ERROR:",
                e
            )

            return f"""
            <h1>Something went wrong</h1>

            <p>{e}</p>

            <br>

            <a href="/link-check">
                Go Back
            </a>
            """

    return render_template(

        "link_check.html",

        result=result,

        category=category,

        source=source,

        link=link

    )


# ==========================================================
# ABOUT
# ==========================================================

@app.route("/about")
@app.route("/about.html")
def about():

    return render_template(
        "about.html"
    )


# ==========================================================
# SCAM AWARENESS
# ==========================================================

@app.route("/awareness")
@app.route("/awareness.html")
def awareness():

    return render_template(
        "awareness.html"
    )


# ==========================================================
# CONTACT
# ==========================================================

@app.route("/contact")
@app.route("/contact.html")
def contact():

    return render_template(
        "contact.html"
    )


# ==========================================================
# PRIVACY
# ==========================================================

@app.route("/privacy")
@app.route("/privacy.html")
def privacy():

    return render_template(
        "privacy.html"
    )


# ==========================================================
# REPORT SCAM
# ==========================================================

@app.route(
    "/report",
    methods=["GET", "POST"]
)
@app.route(
    "/report.html",
    methods=["GET", "POST"]
)
def report():

    if request.method == "POST":

        message = request.form.get(
            "message",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        source = request.form.get(
            "source",
            ""
        ).strip()

        print("================================")
        print("SCAM REPORT")
        print("Message:", message)
        print("Category:", category)
        print("Source:", source)
        print("================================")

        if not message:

            return redirect(
                "/report"
            )

        try:

            save_report(
                message,
                category
            )

            print(
                "Report saved successfully!"
            )

            dashboard = load_dashboard_data()

            dashboard["reports"] = (
                dashboard.get(
                    "reports",
                    0
                ) + 1
            )

            if not category:

                detected_category = detect_scam_category(
                    message
                )

            else:

                detected_category = category

            if detected_category not in dashboard[
                "report_categories"
            ]:

                detected_category = "Other"

            dashboard[
                "report_categories"
            ][detected_category] = (
                dashboard[
                    "report_categories"
                ].get(
                    detected_category,
                    0
                ) + 1
            )

            add_daily_activity(
                dashboard
            )

            save_dashboard_data(
                dashboard
            )

            add_dashboard_activity(
                "🚩 Scam reported",
                alert=True
            )

            return redirect(
                "/thankyou"
            )

        except Exception as e:

            print(
                "DATABASE ERROR:",
                e
            )

            return f"""
            <h1>Could not submit report</h1>

            <p>{e}</p>

            <br>

            <a href="/report">
                Go Back
            </a>
            """

    return render_template(
        "report.html"
    )


# ==========================================================
# THANK YOU / SUCCESS PAGE
# ==========================================================

@app.route("/thankyou")
@app.route("/success.html")
def thankyou():

    return render_template(
        "success.html"
    )


# ==========================================================
# TRANSLATOR
# ==========================================================

@app.route(
    "/translator",
    methods=["GET", "POST"]
)
@app.route(
    "/translator.html",
    methods=["GET", "POST"]
)
def translator_page():

    text = ""
    detected_language = ""
    target_language = ""
    translated_text = ""
    analysis = None

    analysis_labels = {

        "scam_probability":
            "Scam Probability",

        "risk_level":
            "Risk Level",

        "status":
            "Status",

        "reasons":
            "Reasons",

        "safety_tips":
            "Safety Tips"

    }

    if request.method == "POST":

        text = request.form.get(
            "text",
            ""
        ).strip()

        target_language = request.form.get(
            "target_language",
            ""
        ).strip()

        if not text:

            return render_template(

                "translator.html",

                text="",

                detected_language="",

                target_language=target_language,

                translated_text="",

                analysis=None,

                analysis_labels=analysis_labels

            )

        detected_language = detect_language(
            text
        )

        print("================================")
        print("TRANSLATOR")
        print("Original Text:", text)

        print(
            "Detected Language:",
            detected_language
        )

        print(
            "Target Language:",
            target_language
        )

        print("================================")

        translated_text = translate_text(
            text,
            target_language
        )

        dashboard = load_dashboard_data()

        dashboard["translations"] = (
            dashboard.get(
                "translations",
                0
            ) + 1
        )

        add_daily_activity(
            dashboard
        )

        save_dashboard_data(
            dashboard
        )

        add_dashboard_activity(
            "🌐 Translation completed",
            alert=False
        )

        try:

            try:

                original_text_language = detect_language(
                    text
                )

            except Exception as e:

                print(
                    "LANGUAGE DETECTION ERROR:",
                    e
                )

                original_text_language = "Unknown"

            print(
                "Original Text Language:",
                original_text_language
            )

            selected_language = None

            if original_text_language == "English":

                selected_language = "en"

            elif original_text_language == "Hindi":

                selected_language = "hi"

            elif original_text_language == "Marathi":

                selected_language = "mr"

            elif original_text_language == "Hinglish":

                selected_language = "hinglish"

            print(
                "Language sent to scam model:",
                selected_language
            )

            result = detect_scam(
                text,
                selected_language
            )

            print(
                "Scam Analysis:",
                result
            )

            try:

                analysis = translate_analysis(
                    result,
                    target_language
                )

            except Exception as e:

                print(
                    "ANALYSIS TRANSLATION ERROR:",
                    e
                )

                analysis = result.copy()

            analysis["probability"] = result[
                "probability"
            ]

            if not analysis.get("risk"):

                analysis["risk"] = result["risk"]

            if not analysis.get("status"):

                analysis["status"] = result["status"]

            if not analysis.get("language"):

                analysis["language"] = result["language"]

            if not analysis.get("reasons"):

                analysis["reasons"] = result["reasons"]

            if not analysis.get("tips"):

                analysis["tips"] = result["tips"]

            if target_language == "Hindi":

                analysis_labels = {

                    "scam_probability":
                        "स्कैम संभावना",

                    "risk_level":
                        "जोखिम स्तर",

                    "status":
                        "स्थिति",

                    "reasons":
                        "कारण",

                    "safety_tips":
                        "सुरक्षा सुझाव"

                }

            elif target_language == "Marathi":

                analysis_labels = {

                    "scam_probability":
                        "स्कॅम संभाव्यता",

                    "risk_level":
                        "जोखीम पातळी",

                    "status":
                        "स्थिती",

                    "reasons":
                        "कारणे",

                    "safety_tips":
                        "सुरक्षा टिप्स"

                }

            print("================================")

            print(
                "Translation completed"
            )

            print(
                "Translated Text:",
                translated_text
            )

            print(
                "Translated Analysis:",
                analysis
            )

            print("================================")

        except Exception as e:

            print(
                "TRANSLATOR ERROR:",
                e
            )

            analysis = None

    return render_template(

        "translator.html",

        text=text,

        detected_language=detected_language,

        target_language=target_language,

        translated_text=translated_text,

        analysis=analysis,

        analysis_labels=analysis_labels

    )


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )