from deep_translator import GoogleTranslator
from langdetect import detect


# ==========================================
# DETECT LANGUAGE
# ==========================================

def detect_language(text):

    try:

        text = str(text).strip()

        # ======================================
        # HINGLISH DETECTION
        # ======================================
        #
        # IMPORTANT:
        # Common English words like:
        # account, bank, otp, link, verify,
        # message, offer, kyc etc. are NOT used
        # for Hinglish detection.
        #
        # This prevents normal English messages
        # from being detected as Hinglish.
        #
        # ======================================

        hinglish_words = [

            "aap",
            "apka",
            "apki",
            "apke",

            "hai",
            "hain",
            "ho",

            "tha",
            "thi",
            "the",

            "kya",
            "kyu",
            "kyun",
            "kaise",

            "mujhe",
            "mera",
            "meri",
            "mere",

            "hum",
            "ham",

            "aapko",
            "apko",

            "tum",
            "tumhe",
            "tumhara",

            "bhai",
            "yaar",

            "paise",
            "paisa",

            "bhejo",
            "bhej",

            "chahiye",
            "milega",

            "abhi",
            "turant",
            "jaldi",
            "warna",

            "nahi",
            "nahin",

            "mat",

            "karna",
            "karo",
            "kare",

            "krna",
            "kr"
        ]


        words = text.lower().split()

        count = 0


        for word in words:

            word = word.strip(
                ".,!?;:'\"()[]{}"
            )

            if word in hinglish_words:

                count += 1


        # ======================================
        # HINGLISH ONLY IF MULTIPLE
        # ROMAN HINDI WORDS ARE FOUND
        # ======================================

        if count >= 2:

            return "Hinglish"


        # ======================================
        # NORMAL LANGUAGE DETECTION
        # ======================================

        language = detect(text)


        if language == "en":

            return "English"

        elif language == "hi":

            return "Hindi"

        elif language == "mr":

            return "Marathi"

        else:

            return "Other"


    except:

        return "Unknown"


# ==========================================
# TRANSLATE TEXT
# ==========================================

def translate_text(text, target_language):

    language_codes = {

        "English": "en",

        "Hindi": "hi",

        "Marathi": "mr"

        # Hinglish handled separately
    }


    # ======================================
    # BASIC VALIDATION
    # ======================================

    if not text:

        return text


    text = str(text).strip()


    if not text:

        return text


    # ======================================
    # HINGLISH TRANSLATION
    # ======================================
    #
    # Hinglish does NOT use GoogleTranslator.
    # Fixed translations are used instead.
    #
    # ======================================

    if target_language == "Hinglish":

        hinglish_translations = {

            # ==================================
            # RISK
            # ==================================

            "Low":
                "Low",

            "Medium":
                "Medium",

            "High":
                "High",


            # ==================================
            # STATUS
            # ==================================

            "Scam":
                "Scam",

            "Safe":
                "Safe",

            "Spam":
                "Spam",

            "Ham":
                "Safe",


            # ==================================
            # REASONS
            # ==================================

            "Suspicious word detected":
                "Suspicious word mila",

            "AI model identified patterns similar to spam/scam messages.":
                "AI model ne spam ya scam jaise patterns detect kiye.",

            "Message appears relatively safe based on the AI analysis.":
                "AI analysis ke according message relatively safe lagta hai.",

            "No suspicious pattern detected.":
                "Koi suspicious pattern nahi mila.",

            "No suspicious patterns detected.":
                "Koi suspicious pattern nahi mila.",

            "कोई संदिग्ध पैटर्न नहीं मिला.":
                "Koi suspicious pattern nahi mila.",

            "कोई संदिग्ध पैटर्न नहीं मिला।":
                "Koi suspicious pattern nahi mila.",


            # ==================================
            # SAFETY TIPS
            # ==================================

            "Never share OTPs, passwords or banking details.":
                "Kabhi bhi OTP, passwords ya banking details share na karein.",

            "Do not click unknown or suspicious links.":
                "Unknown ya suspicious links par click na karein.",

            "Verify the sender before taking any action.":
                "Koi bhi action lene se pehle sender ko verify karein.",

            "Report suspicious messages to the appropriate authority.":
                "Suspicious messages ko appropriate authority ko report karein.",

            "Stay alert when dealing with unknown contacts.":
                "Unknown contacts ke saath deal karte time alert rahein.",

            "Never share sensitive information through messages.":
                "Messages ke through sensitive information kabhi share na karein."
        }


        # ==================================
        # EXACT TRANSLATIONS
        # ==================================

        if text in hinglish_translations:

            return hinglish_translations[text]


        # ==================================
        # SUSPICIOUS WORD DETECTION
        # ==================================

        if text.startswith(
            "Suspicious word detected:"
        ):

            word = text.split(
                ":",
                1
            )[1].strip()

            return (
                f"Suspicious word mila: {word}"
            )


        # ==================================
        # AI SCAM REASON
        # ==================================

        if (
            "AI model identified patterns"
            in text
        ):

            return (
                "AI model ne spam ya scam "
                "jaise patterns detect kiye."
            )


        # ==================================
        # SAFE PATTERN
        # ==================================

        if (
            "No suspicious pattern"
            in text
        ):

            return (
                "Koi suspicious pattern nahi mila."
            )


        if (
            "कोई संदिग्ध पैटर्न"
            in text
        ):

            return (
                "Koi suspicious pattern nahi mila."
            )


        # ==================================
        # UNKNOWN HINGLISH TEXT
        # ==================================
        #
        # Do not call GoogleTranslator.
        # Return original text instead of
        # displaying an API error.
        #
        # ==================================

        return text


    # ======================================
    # NORMAL LANGUAGE TRANSLATION
    # ======================================

    target_code = language_codes.get(
        target_language
    )


    if not target_code:

        return text


    # ======================================
    # SIMPLE FIXED VALUES
    # ======================================

    simple_translations = {

        "Hindi": {

            "Low": "कम",

            "Medium": "मध्यम",

            "High": "उच्च",

            "Scam": "घोटाला",

            "Safe": "सुरक्षित",

            "Spam": "स्पैम",

            "Ham": "सुरक्षित"

        },


        "Marathi": {

            "Low": "कमी",

            "Medium": "मध्यम",

            "High": "उच्च",

            "Scam": "घोटाळा",

            "Safe": "सुरक्षित",

            "Spam": "स्पॅम",

            "Ham": "सुरक्षित"

        },


        "English": {

            "Low": "Low",

            "Medium": "Medium",

            "High": "High",

            "Scam": "Scam",

            "Safe": "Safe",

            "Spam": "Spam",

            "Ham": "Ham"

        }

    }


    if target_language in simple_translations:

        if text in simple_translations[
            target_language
        ]:

            return simple_translations[
                target_language
            ][text]


    # ======================================
    # HINDI FIXED REASONS
    # ======================================

    if target_language == "Hindi":

        # ----------------------------------
        # Suspicious word
        # ----------------------------------

        if text.startswith(
            "Suspicious word detected:"
        ):

            word = text.split(
                ":",
                1
            )[1].strip()

            return (
                f"संदिग्ध शब्द मिला: {word}"
            )


        # ----------------------------------
        # AI model reason
        # ----------------------------------

        if (
            text ==
            "AI model identified patterns similar to spam/scam messages."
        ):

            return (
                "AI मॉडल ने स्पैम/स्कैम संदेशों "
                "जैसे पैटर्न पहचाने।"
            )


        # ----------------------------------
        # Safe reason
        # ----------------------------------

        if (
            text ==
            "Message appears relatively safe based on the AI analysis."
        ):

            return (
                "AI विश्लेषण के अनुसार संदेश "
                "अपेक्षाकृत सुरक्षित लगता है।"
            )


        # ----------------------------------
        # No suspicious pattern
        # ----------------------------------

        if (
            text ==
            "No suspicious pattern detected."
        ):

            return (
                "कोई संदिग्ध पैटर्न नहीं मिला।"
            )


        if (
            text ==
            "No suspicious patterns detected."
        ):

            return (
                "कोई संदिग्ध पैटर्न नहीं मिला।"
            )


        if (
            "कोई संदिग्ध पैटर्न"
            in text
        ):

            return (
                "कोई संदिग्ध पैटर्न नहीं मिला।"
            )


        # ----------------------------------
        # Safety Tips
        # ----------------------------------

        if (
            text ==
            "Never share OTPs, passwords or banking details."
        ):

            return (
                "OTP, पासवर्ड या बैंकिंग विवरण "
                "कभी साझा न करें।"
            )


        if (
            text ==
            "Do not click unknown or suspicious links."
        ):

            return (
                "अज्ञात या संदिग्ध लिंक पर "
                "क्लिक न करें।"
            )


        if (
            text ==
            "Verify the sender before taking any action."
        ):

            return (
                "कोई भी कार्रवाई करने से पहले "
                "प्रेषक को सत्यापित करें।"
            )


        if (
            text ==
            "Report suspicious messages to the appropriate authority."
        ):

            return (
                "संदिग्ध संदेशों की रिपोर्ट "
                "उचित प्राधिकरण को करें।"
            )


        if (
            text ==
            "Stay alert when dealing with unknown contacts."
        ):

            return (
                "अज्ञात संपर्कों से बात करते समय "
                "सतर्क रहें।"
            )


        if (
            text ==
            "Never share sensitive information through messages."
        ):

            return (
                "संदेशों के माध्यम से संवेदनशील "
                "जानकारी कभी साझा न करें।"
            )


    # ======================================
    # MARATHI FIXED REASONS
    # ======================================

    if target_language == "Marathi":

        # ----------------------------------
        # Suspicious word
        # ----------------------------------

        if text.startswith(
            "Suspicious word detected:"
        ):

            word = text.split(
                ":",
                1
            )[1].strip()

            return (
                f"संशयास्पद शब्द आढळला: {word}"
            )


        # ----------------------------------
        # AI model reason
        # ----------------------------------

        if (
            text ==
            "AI model identified patterns similar to spam/scam messages."
        ):

            return (
                "AI मॉडेलने स्पॅम/स्कॅम "
                "संदेशांसारखे नमुने ओळखले."
            )


        # ----------------------------------
        # Safe reason
        # ----------------------------------

        if (
            text ==
            "Message appears relatively safe based on the AI analysis."
        ):

            return (
                "AI विश्लेषणानुसार हा संदेश "
                "तुलनेने सुरक्षित वाटतो."
            )


        # ----------------------------------
        # No suspicious pattern
        # ----------------------------------

        if (
            text ==
            "No suspicious pattern detected."
        ):

            return (
                "कोणताही संशयास्पद नमुना "
                "आढळला नाही."
            )


        if (
            text ==
            "No suspicious patterns detected."
        ):

            return (
                "कोणताही संशयास्पद नमुना "
                "आढळला नाही."
            )


        # ----------------------------------
        # Safety Tips
        # ----------------------------------

        if (
            text ==
            "Never share OTPs, passwords or banking details."
        ):

            return (
                "OTP, पासवर्ड किंवा बँकिंग तपशील "
                "कधीही शेअर करू नका."
            )


        if (
            text ==
            "Do not click unknown or suspicious links."
        ):

            return (
                "अज्ञात किंवा संशयास्पद लिंकवर "
                "क्लिक करू नका."
            )


        if (
            text ==
            "Verify the sender before taking any action."
        ):

            return (
                "कोणतीही कारवाई करण्यापूर्वी "
                "प्रेषकाची पडताळणी करा."
            )


        if (
            text ==
            "Report suspicious messages to the appropriate authority."
        ):

            return (
                "संशयास्पद संदेशांची योग्य "
                "प्राधिकरणाकडे तक्रार करा."
            )


        if (
            text ==
            "Stay alert when dealing with unknown contacts."
        ):

            return (
                "अज्ञात संपर्कांशी व्यवहार करताना "
                "सतर्क रहा."
            )


        if (
            text ==
            "Never share sensitive information through messages."
        ):

            return (
                "संदेशांद्वारे संवेदनशील माहिती "
                "कधीही शेअर करू नका."
            )


    # ======================================
    # GOOGLE TRANSLATION
    # ======================================
    #
    # Used only for English / Hindi /
    # Marathi when a fixed translation
    # is not available.
    #
    # ======================================

    try:

        translated = GoogleTranslator(

            source="auto",

            target=target_code

        ).translate(text)


        if not translated:

            return text


        translated = str(
            translated
        )


        # ==================================
        # NEVER DISPLAY API ERROR
        # ==================================

        error_words = [

            "Error 500",

            "Server Error",

            "That's an error",

            "There was an error",

            "Please try again later",

            "That's all we know",

            "1500.That’s an error",

            "1500.That's an error"

        ]


        for error_word in error_words:

            if (
                error_word.lower()
                in translated.lower()
            ):

                print(
                    "Invalid translation received."
                )

                return text


        return translated


    except Exception as e:

        print(
            "TRANSLATION ERROR:",
            e
        )

        return text


# ==========================================
# TRANSLATE LIST
# ==========================================

def translate_list(
    items,
    target_language
):

    translated_items = []


    if not items:

        return translated_items


    for item in items:

        translated_items.append(

            translate_text(

                item,

                target_language

            )

        )


    return translated_items


# ==========================================
# TRANSLATE ANALYSIS RESULT
# ==========================================

def translate_analysis(
    result,
    target_language
):

    translated_result = result.copy()


    # ======================================
    # PROBABILITY
    # ======================================

    translated_result["probability"] = result[
        "probability"
    ]


    # ======================================
    # RISK
    # ======================================

    translated_result["risk"] = translate_text(

        result["risk"],

        target_language

    )


    # ======================================
    # STATUS
    # ======================================

    translated_result["status"] = translate_text(

        result["status"],

        target_language

    )


    # ======================================
    # DO NOT TRANSLATE DETECTED LANGUAGE
    # ======================================

    translated_result["language"] = result[
        "language"
    ]


    # ======================================
    # REASONS
    # ======================================

    translated_result["reasons"] = translate_list(

        result["reasons"],

        target_language

    )


    # ======================================
    # SAFETY TIPS
    # ======================================

    translated_result["tips"] = translate_list(

        result["tips"],

        target_language

    )


    return translated_result