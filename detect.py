# ==========================================
# TrustLens AI
# AI-Based Multilingual Scam Detection
# English + Hindi + Marathi + Hinglish
# ==========================================

import joblib
from langdetect import detect


# ==========================================
# LOAD MULTILINGUAL MODELS
# ==========================================

models = joblib.load(
    "model/multilingual_models.pkl"
)


# ==========================================
# SCAM DETECTION FUNCTION
# ==========================================

def detect_scam(message, selected_language=None):

    # --------------------------------------
    # CLEAN MESSAGE
    # --------------------------------------

    message = str(message).strip()


    # --------------------------------------
    # LANGUAGE DETECTION
    # --------------------------------------

    try:

        if len(message) < 10:

            language_code = "unknown"

        else:

            language_code = detect(message)

    except:

        language_code = "unknown"


    # --------------------------------------
    # CONVERT LANGUAGE CODE
    # --------------------------------------

    # If user manually selects a language,
    # use that language.

    if selected_language == "en":

        language = "English"
        model_language = "en"


    elif selected_language == "hi":

        language = "Hindi"
        model_language = "hi"


    elif selected_language == "mr":

        language = "Marathi"
        model_language = "mr"


    elif selected_language == "hinglish":

        language = "Hinglish"
        model_language = "hinglish"


    # --------------------------------------
    # OTHERWISE AUTOMATIC DETECTION
    # --------------------------------------

    elif language_code == "en":

        # ----------------------------------
        # IMPORTANT:
        # Roman/Hinglish messages are
        # usually detected as English by
        # langdetect.
        #
        # We keep English as default here.
        # Manual Hinglish selection from
        # the website will override this.
        # ----------------------------------

        language = "English"
        model_language = "en"


    elif language_code == "hi":

        language = "Hindi"
        model_language = "hi"


    elif language_code == "mr":

        language = "Marathi"
        model_language = "mr"


    else:

        # For unsupported languages,
        # use English model as fallback.

        language = language_code
        model_language = "en"


    # --------------------------------------
    # SELECT CORRECT AI MODEL
    # --------------------------------------

    model = models[model_language]


    # --------------------------------------
    # AI PREDICTION
    # --------------------------------------

    prediction = model.predict(
        [message]
    )[0]

    prediction = str(
        prediction
    ).lower()


    # --------------------------------------
    # GET SCAM PROBABILITY
    # --------------------------------------

    probability_values = model.predict_proba(
        [message]
    )[0]

    classes = model.classes_


    spam_probability = 0


    for i in range(len(classes)):

        if str(
            classes[i]
        ).lower() == "spam":

            spam_probability = (
                probability_values[i] * 100
            )


    probability = round(
        spam_probability,
        2
    )


    # --------------------------------------
    # STATUS
    # --------------------------------------

    if prediction == "spam":

        status = "Scam"

    else:

        status = "Safe"


    # --------------------------------------
    # RISK LEVEL
    # --------------------------------------

    if probability >= 80:

        risk = "High"

    elif probability >= 50:

        risk = "Medium"

    else:

        risk = "Low"


    # ======================================
    # DETECTION REASONS
    # ======================================

    reasons = []


    # English suspicious words

    suspicious_words_en = [

        "click",
        "prize",
        "winner",
        "otp",
        "password",
        "bank",
        "urgent",
        "money",
        "offer",
        "free",
        "link",
        "reward",
        "verify",
        "verification",
        "kyc",
        "upi",
        "refund",
        "blocked",
        "suspended",
        "account"

    ]


    # Hindi suspicious words

    suspicious_words_hi = [

        "बैंक",
        "खाता",
        "ओटीपी",
        "otp",
        "पासवर्ड",
        "इनाम",
        "पुरस्कार",
        "लिंक",
        "सत्यापित",
        "सत्यापन",
        "केवाईसी",
        "kyc",
        "यूपीआई",
        "upi",
        "रिफंड",
        "ब्लॉक",
        "बंद",
        "तुरंत",
        "कैशबैक"

    ]


    # Marathi suspicious words

    suspicious_words_mr = [

        "बँक",
        "खाते",
        "ओटीपी",
        "otp",
        "पासवर्ड",
        "बक्षीस",
        "इनाम",
        "लिंक",
        "सत्यापित",
        "सत्यापन",
        "केवायसी",
        "kyc",
        "यूपीआय",
        "upi",
        "परतावा",
        "ब्लॉक",
        "बंद",
        "त्वरित",
        "कॅशबॅक"

    ]


    # Hinglish suspicious words

    suspicious_words_hinglish = [

        "bank",
        "account",
        "otp",
        "password",
        "prize",
        "reward",
        "winner",
        "click",
        "link",
        "verify",
        "verification",
        "kyc",
        "upi",
        "refund",
        "cashback",
        "blocked",
        "suspend",
        "suspended",
        "urgent",
        "immediately",
        "abhi",
        "turant",
        "inaam",
        "bakhshish",
        "paise",
        "paisa",
        "details",
        "claim",
        "update",
        "open",
        "send",
        "share",
        "karo",
        "karna",
        "krna",
        "hai",
        "ho",
        "aap",
        "apka",
        "apne",
        "mera",
        "mere",
        "mujhe",
        "please",
        "jaldi",
        "band",
        "bandh",
        "khata",
        "khaata",
        "batao",
        "bhejo",
        "bhej",
        "verify karo",
        "click karo",
        "link kholo",
        "otp bhejo"

    ]


    # --------------------------------------
    # SELECT SUSPICIOUS WORDS
    # --------------------------------------

    if model_language == "hi":

        suspicious_words = (
            suspicious_words_hi
        )

    elif model_language == "mr":

        suspicious_words = (
            suspicious_words_mr
        )

    elif model_language == "hinglish":

        suspicious_words = (
            suspicious_words_hinglish
        )

    else:

        suspicious_words = (
            suspicious_words_en
        )


    # --------------------------------------
    # CHECK SUSPICIOUS WORDS
    # --------------------------------------

    for word in suspicious_words:

        if word.lower() in message.lower():

            reasons.append(

                "Suspicious word detected: "
                + word

            )


    # --------------------------------------
    # AI REASON
    # --------------------------------------

    if prediction == "spam":

        reasons.append(

            "AI model identified patterns "
            "similar to spam/scam messages."

        )


    # --------------------------------------
    # NO REASON FOUND
    # --------------------------------------

    if len(reasons) == 0:

        reasons.append(

            "No suspicious pattern detected."

        )


    # ======================================
    # SCAM TYPE DETECTION
    # ======================================

    # --------------------------------------
    # Convert message to lowercase
    # for category matching
    # --------------------------------------

    message_lower = message.lower()


    # ======================================
    # BANKING / KYC
    # ======================================

    banking_keywords = [

        # English
        "bank",
        "bank account",
        "account",
        "kyc",
        "verify kyc",
        "update kyc",
        "bank verification",
        "account blocked",
        "account suspended",
        "debit card",
        "credit card",
        "atm",
        "net banking",
        "banking",

        # Hindi
        "बैंक",
        "बैंक खाता",
        "खाता",
        "केवाईसी",
        "बैंक सत्यापन",
        "खाता बंद",
        "खाता ब्लॉक",

        # Marathi
        "बँक",
        "बँक खाते",
        "खाते",
        "केवायसी",
        "बँक सत्यापन",
        "खाते बंद"

    ]


    # ======================================
    # JOB / INTERNSHIP
    # ======================================

    job_keywords = [

        # English
        "job",
        "jobs",
        "job offer",
        "job opportunity",
        "employment",
        "work from home",
        "work from home job",
        "part time job",
        "full time job",
        "internship",
        "intern",
        "career",
        "salary",
        "hiring",
        "recruitment",
        "vacancy",
        "registration fee",
        "joining fee",
        "processing fee",

        # Hindi
        "नौकरी",
        "जॉब",
        "इंटर्नशिप",
        "वेतन",
        "भर्ती",
        "काम",
        "घर से काम",

        # Marathi
        "नोकरी",
        "जॉब",
        "इंटर्नशिप",
        "पगार",
        "भरती",
        "काम"
    ]


    # ======================================
    # LOTTERY / PRIZE
    # ======================================

    lottery_keywords = [

        # English
        "lottery",
        "lottery winner",
        "prize",
        "prize money",
        "winner",
        "you won",
        "won a prize",
        "reward",
        "cash prize",
        "lucky winner",
        "lucky draw",
        "contest winner",
        "congratulations",
        "claim your prize",
        "claim reward",

        # Hindi
        "लॉटरी",
        "इनाम",
        "पुरस्कार",
        "विजेता",
        "आप जीत गए",
        "बधाई",
        "इनामी राशि",
        "भाग्यशाली",

        # Marathi
        "लॉटरी",
        "बक्षीस",
        "इनाम",
        "पुरस्कार",
        "विजेता",
        "तुम्ही जिंकलात",
        "अभिनंदन"
    ]


    # ======================================
    # UPI / PAYMENT
    # ======================================

    payment_keywords = [

        # English
        "upi",
        "upi payment",
        "payment",
        "payment failed",
        "payment pending",
        "payment refund",
        "refund",
        "cashback",
        "transaction",
        "transaction failed",
        "send money",
        "receive money",
        "money transfer",
        "pay",
        "payment link",
        "qr code",
        "scan qr",

        # Hindi
        "यूपीआई",
        "भुगतान",
        "पैसे भेजें",
        "पैसे प्राप्त",
        "लेनदेन",
        "कैशबैक",
        "रिफंड",
        "क्यूआर कोड",

        # Marathi
        "यूपीआय",
        "पेमेंट",
        "पैसे पाठवा",
        "पैसे मिळवा",
        "व्यवहार",
        "कॅशबॅक",
        "परतावा",
        "क्यूआर कोड"
    ]


    # ======================================
    # SOCIAL MEDIA
    # ======================================

    social_media_keywords = [

        # English
        "instagram",
        "facebook",
        "whatsapp",
        "telegram",
        "social media",
        "social account",
        "account verification",
        "followers",
        "blue tick",
        "verified badge",
        "telegram group",
        "whatsapp group",

        # Hindi
        "इंस्टाग्राम",
        "फेसबुक",
        "व्हाट्सएप",
        "टेलीग्राम",
        "सोशल मीडिया",

        # Marathi
        "इन्स्टाग्राम",
        "फेसबुक",
        "व्हॉट्सअॅप",
        "टेलिग्राम",
        "सोशल मीडिया"
    ]


    # ======================================
    # SHOPPING / DELIVERY
    # ======================================

    shopping_keywords = [

        # English
        "amazon",
        "flipkart",
        "shopping",
        "order",
        "delivery",
        "parcel",
        "package",
        "courier",
        "delivery failed",
        "delivery address",
        "order cancelled",
        "refund order",
        "product",
        "online shopping",

        # Hindi
        "ऑर्डर",
        "डिलीवरी",
        "पार्सल",
        "कूरियर",
        "सामान",
        "ऑनलाइन खरीदारी",

        # Marathi
        "ऑर्डर",
        "डिलिव्हरी",
        "पार्सल",
        "कुरिअर",
        "ऑनलाइन खरेदी"
    ]


    # ======================================
    # INVESTMENT / LOAN
    # ======================================

    investment_keywords = [

        # English
        "investment",
        "invest",
        "stock",
        "trading",
        "crypto",
        "cryptocurrency",
        "bitcoin",
        "profit",
        "guaranteed profit",
        "double your money",
        "loan",
        "instant loan",
        "personal loan",
        "loan approval",
        "loan processing fee",
        "interest rate",

        # Hindi
        "निवेश",
        "शेयर",
        "ट्रेडिंग",
        "क्रिप्टो",
        "मुनाफा",
        "गारंटीड मुनाफा",
        "लोन",
        "ऋण",

        # Marathi
        "गुंतवणूक",
        "शेअर",
        "ट्रेडिंग",
        "क्रिप्टो",
        "नफा",
        "कर्ज",
        "लोन"
    ]


    # ======================================
    # SCAM TYPE DETECTION LOGIC
    # ======================================

    scam_type = "Other / General Scam"


    # We check the more specific categories
    # first.

    if any(
        keyword in message_lower
        for keyword in banking_keywords
    ):

        scam_type = "Banking / KYC"


    elif any(
        keyword in message_lower
        for keyword in job_keywords
    ):

        scam_type = "Job / Internship"


    elif any(
        keyword in message_lower
        for keyword in lottery_keywords
    ):

        scam_type = "Lottery / Prize"


    elif any(
        keyword in message_lower
        for keyword in payment_keywords
    ):

        scam_type = "UPI / Payment"


    elif any(
        keyword in message_lower
        for keyword in social_media_keywords
    ):

        scam_type = "Social Media"


    elif any(
        keyword in message_lower
        for keyword in shopping_keywords
    ):

        scam_type = "Shopping / Delivery"


    elif any(
        keyword in message_lower
        for keyword in investment_keywords
    ):

        scam_type = "Investment / Loan"


    # ======================================
    # SAFETY TIPS
    # ======================================

    tips = []


    if status == "Scam":

        tips.append(

            "Never share OTPs, passwords "
            "or banking details."

        )

        tips.append(

            "Do not click unknown or "
            "suspicious links."

        )

        tips.append(

            "Verify the sender before "
            "taking any action."

        )

        tips.append(

            "Report suspicious messages "
            "to the appropriate authority."

        )

    else:

        tips.append(

            "Message appears relatively safe "
            "based on the AI analysis."

        )

        tips.append(

            "Stay alert when dealing with "
            "unknown contacts."

        )

        tips.append(

            "Never share sensitive information "
            "through messages."

        )


    # ======================================
    # RETURN RESULT
    # ======================================

    return {

        "language": language,

        "probability": probability,

        "risk": risk,

        "status": status,

        "scam_type": scam_type,

        "reasons": reasons,

        "tips": tips

    }


# ==========================================
# TESTING SECTION
# ==========================================

if __name__ == "__main__":

    message = input(
        "Enter message: "
    )


    result = detect_scam(
        message
    )


    print(
        "\n----- TrustLens AI Result -----"
    )


    print(
        "Language:",
        result["language"]
    )


    print(
        "Scam Probability:",
        result["probability"],
        "%"
    )


    print(
        "Risk Level:",
        result["risk"]
    )


    print(
        "Status:",
        result["status"]
    )


    print(
        "Scam Type:",
        result["scam_type"]
    )


    print("\nReasons:")


    for reason in result["reasons"]:

        print(
            "-",
            reason
        )


    print("\nSafety Tips:")


    for tip in result["tips"]:

        print(
            "-",
            tip
        )