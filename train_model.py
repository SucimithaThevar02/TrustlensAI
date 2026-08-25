# ==========================================
# TRUSTLENS AI
# Multilingual Scam Detection
# English + Hindi + Marathi + Hinglish
# ==========================================

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. LOAD DATASET
# ==========================================

print("\nLoading dataset...")

df = pd.read_csv(
    "dataset/combined_scam_dataset.csv"
)

print("Combined dataset:", len(df))

print("\nDataset columns:")
print(df.columns.tolist())

print("\nLanguage distribution:")
print(df["language"].value_counts())


# ==========================================
# 2. PREPARE DATA USING LANGUAGE COLUMN
# ==========================================

# Combined dataset contains:
#
# text
# labels
# language
#
# We separate the dataset using language.


# ==========================================
# 3. PREPARE ENGLISH DATA
# ==========================================

english = df[
    df["language"].astype(str).str.lower().str.strip() == "english"
][
    ["text", "labels"]
].copy()


# ==========================================
# 4. PREPARE HINDI DATA
# ==========================================

hindi = df[
    df["language"].astype(str).str.lower().str.strip() == "hindi"
][
    ["text", "labels"]
].copy()


# ==========================================
# 5. PREPARE MARATHI DATA
# ==========================================

marathi = df[
    df["language"].astype(str).str.lower().str.strip() == "marathi"
][
    ["text", "labels"]
].copy()


# ==========================================
# 6. PREPARE HINGLISH DATA
# ==========================================

hinglish = df[
    df["language"].astype(str).str.lower().str.strip() == "hinglish"
][
    ["text", "labels"]
].copy()


# ==========================================
# 7. CLEAN DATA
# ==========================================

def clean_data(data):

    data = data.dropna(
        subset=["text", "labels"]
    )

    data["text"] = (
        data["text"]
        .astype(str)
        .str.strip()
    )

    data["labels"] = (
        data["labels"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    data = data[
        data["text"] != ""
    ]

    return data.drop_duplicates()


english = clean_data(english)

hindi = clean_data(hindi)

marathi = clean_data(marathi)

hinglish = clean_data(hinglish)


# ==========================================
# 8. EXTRA ENGLISH EXAMPLES
# ==========================================

english_extra = [

    # SCAM

    ("Your bank account has been suspended. Verify your details now.", "spam"),

    ("Your bank account has been blocked. Verify your account immediately.", "spam"),

    ("Your bank account will be closed unless you verify your details.", "spam"),

    ("Your KYC verification is pending. Complete it immediately.", "spam"),

    ("Your KYC has expired. Click the link to update it.", "spam"),

    ("Your UPI payment failed. Click here to receive your refund.", "spam"),

    ("Your UPI account has been suspended. Verify immediately.", "spam"),

    ("Click this link to claim your reward.", "spam"),

    ("You have won a prize. Click the link to claim it.", "spam"),

    ("Share your OTP to receive your reward.", "spam"),

    ("Send your OTP to verify your bank account.", "spam"),

    ("Verify your bank details immediately to avoid account closure.", "spam"),

    ("Your account has suspicious activity. Login immediately.", "spam"),

    ("Click here to receive your bank refund.", "spam"),

    ("Complete KYC immediately or your account will be blocked.", "spam"),

    ("Your card will be blocked. Verify your details now.", "spam"),

    ("You have received a cashback reward. Claim it now.", "spam"),

    ("Enter your OTP to receive cashback.", "spam"),

    ("Click this link to activate your bank account.", "spam"),

    ("Your account verification is required urgently.", "spam"),


    # SAFE

    ("I visited the bank today to deposit a cheque.", "ham"),

    ("My UPI payment was successful.", "ham"),

    ("I received the OTP for my login.", "ham"),

    ("I went to the bank this morning.", "ham"),

    ("I checked my bank account today.", "ham"),

    ("I made a UPI payment to my friend.", "ham"),

    ("The bank sent me an OTP for my login.", "ham"),

    ("I received a bank statement today.", "ham"),

    ("My bank transaction was successful.", "ham"),

    ("I transferred money to my brother using UPI.", "ham"),

    ("I paid the electricity bill using UPI.", "ham"),

    ("I deposited a cheque at the bank.", "ham"),

    ("The bank confirmed my payment.", "ham"),

    ("I received an OTP while logging into my account.", "ham"),

    ("I am going to the bank tomorrow.", "ham"),

    ("The UPI payment was completed successfully.", "ham"),

    ("I checked my KYC details at the bank.", "ham"),

    ("I updated my bank information at the branch.", "ham"),

    ("I received my bank statement.", "ham"),

    ("The bank employee helped me with my account.", "ham")

]


# ==========================================
# 9. EXTRA HINDI EXAMPLES
# ==========================================

hindi_extra = [

    # SCAM

    ("आपका बैंक खाता बंद कर दिया गया है। तुरंत सत्यापित करें।", "spam"),

    ("आपका बैंक खाता ब्लॉक होने वाला है। अभी विवरण सत्यापित करें।", "spam"),

    ("आपका KYC समाप्त हो गया है। तुरंत अपडेट करें।", "spam"),

    ("आपका KYC सत्यापन लंबित है। अभी पूरा करें।", "spam"),

    ("आपका UPI भुगतान विफल हुआ है। रिफंड पाने के लिए लिंक पर क्लिक करें।", "spam"),

    ("आपका UPI खाता निलंबित है। तुरंत सत्यापन करें।", "spam"),

    ("आपने इनाम जीता है। पुरस्कार पाने के लिए लिंक खोलें।", "spam"),

    ("अपना OTP साझा करें और कैशबैक प्राप्त करें।", "spam"),

    ("बैंक की ओर से जरूरी सूचना। अपना OTP भेजें।", "spam"),

    ("अपना बैंक विवरण तुरंत सत्यापित करें।", "spam"),

    ("आपका कार्ड बंद कर दिया जाएगा। सत्यापन के लिए लिंक खोलें।", "spam"),

    ("रिफंड पाने के लिए अपनी बैंक जानकारी दर्ज करें।", "spam"),

    ("आपके खाते में संदिग्ध गतिविधि मिली है। अभी लॉगिन करें।", "spam"),

    ("कैशबैक पाने के लिए अपना OTP दर्ज करें।", "spam"),

    ("बैंक रिफंड के लिए नीचे दिए गए लिंक पर क्लिक करें।", "spam"),

    ("KYC पूरा करने के लिए इस लिंक पर क्लिक करें।", "spam"),

    ("आपका खाता बंद होने वाला है। तुरंत सत्यापन करें।", "spam"),

    ("बैंक खाता सुरक्षित रखने के लिए OTP भेजें।", "spam"),

    ("आपका इनाम तैयार है। अपना बैंक विवरण भेजें।", "spam"),

    ("तुरंत लिंक खोलें और अपना खाता सत्यापित करें।", "spam"),


    # SAFE

    ("मैंने आज बैंक में चेक जमा किया।", "ham"),

    ("मेरा UPI भुगतान सफल हो गया।", "ham"),

    ("मुझे लॉगिन के लिए OTP मिला है।", "ham"),

    ("मैं आज बैंक गया था।", "ham"),

    ("मैंने आज अपना बैंक खाता चेक किया।", "ham"),

    ("मैंने अपने दोस्त को UPI से पैसे भेजे।", "ham"),

    ("बैंक ने मुझे लॉगिन के लिए OTP भेजा।", "ham"),

    ("मुझे आज बैंक स्टेटमेंट मिला।", "ham"),

    ("मेरा बैंक लेनदेन सफल रहा।", "ham"),

    ("मैंने UPI से अपने भाई को पैसे भेजे।", "ham"),

    ("मैंने UPI से बिजली का बिल भरा।", "ham"),

    ("मैंने बैंक में चेक जमा किया।", "ham"),

    ("बैंक ने मेरे भुगतान की पुष्टि की।", "ham"),

    ("मुझे अपने खाते में लॉगिन करने के लिए OTP मिला।", "ham"),

    ("मैं कल बैंक जा रहा हूँ।", "ham"),

    ("मेरा UPI भुगतान सफलतापूर्वक पूरा हुआ।", "ham"),

    ("मैंने बैंक में अपने KYC विवरण चेक किए।", "ham"),

    ("मैंने बैंक शाखा में अपनी जानकारी अपडेट की।", "ham"),

    ("मुझे अपना बैंक स्टेटमेंट मिला।", "ham"),

    ("बैंक कर्मचारी ने मेरे खाते में मदद की।", "ham")

]


# ==========================================
# 10. EXTRA MARATHI EXAMPLES
# ==========================================

marathi_extra = [

    # SCAM

    ("तुमचे बँक खाते बंद करण्यात आले आहे. त्वरित सत्यापित करा.", "spam"),

    ("तुमचे बँक खाते ब्लॉक होणार आहे. तपशील त्वरित सत्यापित करा.", "spam"),

    ("तुमचे KYC कालबाह्य झाले आहे. आत्ताच अपडेट करा.", "spam"),

    ("तुमचे KYC सत्यापन प्रलंबित आहे. त्वरित पूर्ण करा.", "spam"),

    ("तुमचे UPI पेमेंट अयशस्वी झाले. परतावा मिळवण्यासाठी लिंकवर क्लिक करा.", "spam"),

    ("तुमचे UPI खाते निलंबित आहे. त्वरित सत्यापन करा.", "spam"),

    ("तुम्ही बक्षीस जिंकले आहे. बक्षीस मिळवण्यासाठी लिंक उघडा.", "spam"),

    ("कॅशबॅक मिळवण्यासाठी तुमचा OTP शेअर करा.", "spam"),

    ("बँकेकडून महत्त्वाची सूचना. तुमचा OTP पाठवा.", "spam"),

    ("तुमचे बँक तपशील त्वरित सत्यापित करा.", "spam"),

    ("तुमचे कार्ड बंद केले जाईल. सत्यापनासाठी लिंक उघडा.", "spam"),

    ("परतावा मिळवण्यासाठी तुमची बँक माहिती भरा.", "spam"),

    ("तुमच्या खात्यात संशयास्पद हालचाल आढळली आहे. आत्ताच लॉगिन करा.", "spam"),

    ("कॅशबॅक मिळवण्यासाठी तुमचा OTP टाका.", "spam"),

    ("बँक परताव्यासाठी खालील लिंकवर क्लिक करा.", "spam"),

    ("KYC पूर्ण करण्यासाठी या लिंकवर क्लिक करा.", "spam"),

    ("तुमचे खाते बंद होणार आहे. त्वरित सत्यापन करा.", "spam"),

    ("बँक खाते सुरक्षित ठेवण्यासाठी OTP पाठवा.", "spam"),

    ("तुमचे बक्षीस तयार आहे. तुमचे बँक तपशील पाठवा.", "spam"),

    ("आत्ताच लिंक उघडा आणि तुमचे खाते सत्यापित करा.", "spam"),


    # SAFE

    ("मी आज बँकेत चेक जमा केला.", "ham"),

    ("माझे UPI पेमेंट यशस्वी झाले.", "ham"),

    ("मला लॉगिनसाठी OTP मिळाला.", "ham"),

    ("मी आज बँकेत गेलो होतो.", "ham"),

    ("मी आज माझे बँक खाते तपासले.", "ham"),

    ("मी माझ्या मित्राला UPI ने पैसे पाठवले.", "ham"),

    ("बँकेने मला लॉगिनसाठी OTP पाठवला.", "ham"),

    ("मला आज बँक स्टेटमेंट मिळाले.", "ham"),

    ("माझा बँक व्यवहार यशस्वी झाला.", "ham"),

    ("मी UPI ने माझ्या भावाला पैसे पाठवले.", "ham"),

    ("मी UPI ने वीजेचे बिल भरले.", "ham"),

    ("मी बँकेत चेक जमा केला.", "ham"),

    ("बँकेने माझ्या पेमेंटची पुष्टी केली.", "ham"),

    ("मला माझ्या खात्यात लॉगिन करण्यासाठी OTP मिळाला.", "ham"),

    ("मी उद्या बँकेत जाणार आहे.", "ham"),

    ("माझे UPI पेमेंट यशस्वीपणे पूर्ण झाले.", "ham"),

    ("मी बँकेत माझे KYC तपशील तपासले.", "ham"),

    ("मी बँक शाखेत माझी माहिती अपडेट केली.", "ham"),

    ("मला माझे बँक स्टेटमेंट मिळाले.", "ham"),

    ("बँक कर्मचाऱ्याने माझ्या खात्यात मला मदत केली.", "ham")

]


# ==========================================
# 11. EXTRA HINGLISH EXAMPLES
# ==========================================

hinglish_extra = [

    # SCAM

    ("Aapka bank account suspend ho gaya hai. Abhi verify karo.", "spam"),

    ("Aapka bank account block ho jayega. KYC immediately update karo.", "spam"),

    ("Aapka KYC expire ho gaya hai. Link par click karke update karo.", "spam"),

    ("Aapka KYC pending hai. Turant verification complete karo.", "spam"),

    ("Aapka UPI payment fail ho gaya. Refund lene ke liye link open karo.", "spam"),

    ("Aapka UPI account suspend ho gaya hai. Abhi verify karo.", "spam"),

    ("Aapne prize jeeta hai. Reward claim karne ke liye link par click karo.", "spam"),

    ("Cashback receive karne ke liye apna OTP share karo.", "spam"),

    ("Bank ki taraf se important message hai. Apna OTP send karo.", "spam"),

    ("Apne bank details immediately verify karo.", "spam"),

    ("Aapka card block ho jayega. Verification ke liye link open karo.", "spam"),

    ("Refund lene ke liye apni bank information enter karo.", "spam"),

    ("Aapke account mein suspicious activity mili hai. Abhi login karo.", "spam"),

    ("Cashback paane ke liye OTP enter karo.", "spam"),

    ("Bank refund ke liye neeche diye gaye link par click karo.", "spam"),

    ("KYC complete karne ke liye is link par click karo.", "spam"),

    ("Aapka account close hone wala hai. Turant verify karo.", "spam"),

    ("Bank account safe rakhne ke liye OTP send karo.", "spam"),

    ("Aapka reward ready hai. Apne bank details bhejo.", "spam"),

    ("Abhi link open karo aur account verify karo.", "spam"),


    # SAFE

    ("Maine aaj bank mein cheque deposit kiya.", "ham"),

    ("Mera UPI payment successfully ho gaya.", "ham"),

    ("Mujhe login ke liye OTP mila hai.", "ham"),

    ("Main aaj bank gaya tha.", "ham"),

    ("Maine aaj apna bank account check kiya.", "ham"),

    ("Maine apne friend ko UPI se paise bheje.", "ham"),

    ("Bank ne mujhe login ke liye OTP bheja.", "ham"),

    ("Mujhe aaj bank statement mila.", "ham"),

    ("Mera bank transaction successful tha.", "ham"),

    ("Maine UPI se apne brother ko paise bheje.", "ham"),

    ("Maine UPI se electricity bill pay kiya.", "ham"),

    ("Maine bank mein cheque deposit kiya.", "ham"),

    ("Bank ne mere payment ko confirm kiya.", "ham"),

    ("Mujhe account login karne ke liye OTP mila.", "ham"),

    ("Main kal bank ja raha hoon.", "ham"),

    ("Mera UPI payment successfully complete hua.", "ham"),

    ("Maine bank mein apna KYC details check kiya.", "ham"),

    ("Maine bank branch mein apni information update ki.", "ham"),

    ("Mujhe mera bank statement mil gaya.", "ham"),

    ("Bank employee ne mere account mein help ki.", "ham")

]


# ==========================================
# 12. ADD EXTRA DATA
# ==========================================

english_extra_df = pd.DataFrame(
    english_extra,
    columns=["text", "labels"]
)

hindi_extra_df = pd.DataFrame(
    hindi_extra,
    columns=["text", "labels"]
)

marathi_extra_df = pd.DataFrame(
    marathi_extra,
    columns=["text", "labels"]
)

hinglish_extra_df = pd.DataFrame(
    hinglish_extra,
    columns=["text", "labels"]
)


english = pd.concat(
    [english, english_extra_df],
    ignore_index=True
)

hindi = pd.concat(
    [hindi, hindi_extra_df],
    ignore_index=True
)

marathi = pd.concat(
    [marathi, marathi_extra_df],
    ignore_index=True
)

hinglish = pd.concat(
    [hinglish, hinglish_extra_df],
    ignore_index=True
)


english = clean_data(english)

hindi = clean_data(hindi)

marathi = clean_data(marathi)

hinglish = clean_data(hinglish)


# ==========================================
# 13. SHOW FINAL DATASET SIZE
# ==========================================

print("\n==========================================")
print("FINAL TRAINING DATA")
print("==========================================")

print("English:", len(english))
print("Hindi:", len(hindi))
print("Marathi:", len(marathi))
print("Hinglish:", len(hinglish))

print("\nEnglish labels:")
print(english["labels"].value_counts())

print("\nHindi labels:")
print(hindi["labels"].value_counts())

print("\nMarathi labels:")
print(marathi["labels"].value_counts())

print("\nHinglish labels:")
print(hinglish["labels"].value_counts())


# ==========================================
# 14. TRAIN FUNCTION
# ==========================================

def train_model(name, data):

    print("\n==========================================")

    print(
        "Training",
        name,
        "model..."
    )

    print("==========================================")

    print(
        "Total messages:",
        len(data)
    )

    print(
        "\nLabels:"
    )

    print(
        data["labels"].value_counts()
    )

    X = data["text"]

    y = data["labels"]


    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=42,

        stratify=y

    )


    model = Pipeline([

        (

            "tfidf",

            TfidfVectorizer(

                analyzer="char",

                ngram_range=(2, 5),

                min_df=1,

                sublinear_tf=True

            )

        ),

        (

            "classifier",

            LogisticRegression(

                max_iter=3000,

                class_weight="balanced"

            )

        )

    ])


    model.fit(

        X_train,

        y_train

    )


    predictions = model.predict(
        X_test
    )


    accuracy = accuracy_score(

        y_test,

        predictions

    )


    print(
        "\nAccuracy:",
        round(accuracy, 4)
    )


    print(
        "\nClassification Report:"
    )


    print(
        classification_report(
            y_test,
            predictions
        )
    )


    return model


# ==========================================
# 15. TRAIN ALL FOUR MODELS
# ==========================================

english_model = train_model(
    "ENGLISH",
    english
)


hindi_model = train_model(
    "HINDI",
    hindi
)


marathi_model = train_model(
    "MARATHI",
    marathi
)


hinglish_model = train_model(
    "HINGLISH",
    hinglish
)


# ==========================================
# 16. SAVE MODELS
# ==========================================

models = {

    "en": english_model,

    "hi": hindi_model,

    "mr": marathi_model,

    "hinglish": hinglish_model

}


joblib.dump(

    models,

    "model/multilingual_models.pkl"

)


print("\n==========================================")

print(
    "✅ ALL FOUR MODELS TRAINED SUCCESSFULLY!"
)

print("==========================================")

print(
    "Models:"
)

print(
    "English"
)

print(
    "Hindi"
)

print(
    "Marathi"
)

print(
    "Hinglish"
)

print("\nSaved as:")

print(
    "model/multilingual_models.pkl"
)

print("==========================================")