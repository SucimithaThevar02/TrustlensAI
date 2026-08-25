import pandas as pd

print("\n======================================")
print("TRUSTLENS AI - DATASET PREPARATION")
print("======================================\n")


# ======================================
# 1. LOAD DATASETS
# ======================================

print("Loading datasets...\n")

df1 = pd.read_csv("dataset/scam_messages.csv")
df2 = pd.read_csv("dataset/dataset.csv")
df3 = pd.read_csv("dataset/marathi.csv")
df4 = pd.read_csv("dataset/new.csv")
df5 = pd.read_csv("dataset/Personal SMS Data-set .csv")
df6 = pd.read_csv("dataset/indian_spam.csv")
df7 = pd.read_csv("dataset/ultra_premium_scam_dataset.csv")
df8 = pd.read_csv("dataset/India_Cyber_Scam_Hinglish_Dataset.csv")


print("scam_messages.csv:", len(df1))
print("dataset.csv:", len(df2))
print("marathi.csv:", len(df3))
print("new.csv:", len(df4))
print("Personal SMS Data-set:", len(df5))
print("indian_spam.csv:", len(df6))
print("ultra_premium_scam_dataset.csv:", len(df7))
print("India_Cyber_Scam_Hinglish_Dataset.csv:", len(df8))


# ======================================
# 2. ORIGINAL ENGLISH DATA
# ======================================

data1 = pd.DataFrame({

    "text": df1["text"],

    "labels": df1["labels"],

    "language": "english"

})


# ======================================
# 3. LARGE DATASET
# ======================================

data2 = pd.DataFrame({

    "text": df2["text"],

    "labels": df2["labels"],

    "language": df2["lang"]

})


# ======================================
# 4. MARATHI DATASET
# ======================================

# English messages

marathi_english = pd.DataFrame({

    "text": df3["text"],

    "labels": df3["labels"],

    "language": "english"

})


# Hindi translations

marathi_hindi = pd.DataFrame({

    "text": df3["text_hi"],

    "labels": df3["labels"],

    "language": "hindi"

})


# Marathi translations

marathi_marathi = pd.DataFrame({

    "text": df3["text_mr"],

    "labels": df3["labels"],

    "language": "marathi"

})


data3 = pd.concat(

    [
        marathi_english,
        marathi_hindi,
        marathi_marathi
    ],

    ignore_index=True

)


# ======================================
# 5. NEW DATASET
# ======================================

data4 = pd.DataFrame({

    "text": df4["Message"],

    "labels": df4["Label"],

    "language": "english"

})


# ======================================
# 6. PERSONAL SMS
# ======================================

data5 = pd.DataFrame({

    "text": df5["text"],

    "labels": df5["label"],

    "language": "hinglish"

})


# ======================================
# 7. INDIAN SPAM
# ======================================

data6 = pd.DataFrame({

    "text": df6["message"],

    "labels": df6["label"],

    "language": "hinglish"

})


# ======================================
# 8. FUNCTION FOR NEW DATASETS
# ======================================

def prepare_new_dataset(df, name, language):

    print("\n--------------------------------------")
    print("Preparing:", name)
    print("--------------------------------------")

    print("Columns:", df.columns.tolist())


    # Possible label columns

    label_columns = [

        "labels",
        "label",
        "Label",
        "Labels",
        "category",
        "Category"

    ]


    # Possible text columns

    text_columns = [

        "text",
        "Text",
        "message",
        "Message",
        "sms",
        "SMS"

    ]


    label_column = None

    text_column = None


    # Find label column

    for column in label_columns:

        if column in df.columns:

            label_column = column

            break


    # Find text column

    for column in text_columns:

        if column in df.columns:

            text_column = column

            break


    if label_column is None:

        raise ValueError(

            f"No label column found in {name}. "
            f"Columns available: {df.columns.tolist()}"

        )


    if text_column is None:

        raise ValueError(

            f"No text column found in {name}. "
            f"Columns available: {df.columns.tolist()}"

        )


    print("Label column:", label_column)

    print("Text column:", text_column)


    data = pd.DataFrame({

        "text": df[text_column],

        "labels": df[label_column],

        "language": language

    })


    return data


# ======================================
# 9. ULTRA PREMIUM DATASET
# ======================================

data7 = prepare_new_dataset(

    df7,

    "ultra_premium_scam_dataset.csv",

    "english"

)


# ======================================
# 10. HINGLISH DATASET
# ======================================

data8 = prepare_new_dataset(

    df8,

    "India_Cyber_Scam_Hinglish_Dataset.csv",

    "hinglish"

)


# ======================================
# 11. COMBINE EVERYTHING
# ======================================

combined = pd.concat(

    [

        data1,
        data2,
        data3,
        data4,
        data5,
        data6,
        data7,
        data8

    ],

    ignore_index=True

)


print("\n======================================")

print(
    "Total rows before cleaning:",
    len(combined)
)

print("======================================")


# ======================================
# 12. CLEAN LABELS
# ======================================

combined["labels"] = (

    combined["labels"]

    .astype(str)

    .str.lower()

    .str.strip()

)


# Convert numeric labels

combined["labels"] = combined["labels"].replace({

    "0": "ham",

    "1": "spam"

})


# ======================================
# 13. CLEAN TEXT
# ======================================

combined["text"] = (

    combined["text"]

    .fillna("")

    .astype(str)

    .str.strip()

)


# ======================================
# 14. CLEAN LANGUAGE
# ======================================

combined["language"] = (

    combined["language"]

    .fillna("unknown")

    .astype(str)

    .str.lower()

    .str.strip()

)


# ======================================
# 15. REMOVE EMPTY TEXT
# ======================================

combined = combined[

    combined["text"] != ""

]


# ======================================
# 16. KEEP ONLY HAM / SPAM
# ======================================

combined = combined[

    combined["labels"].isin(
        ["ham", "spam"]
    )

]


# ======================================
# 17. REMOVE DUPLICATES
# ======================================

before = len(combined)


combined = combined.drop_duplicates(

    subset=[
        "text",
        "labels",
        "language"
    ]

)


after = len(combined)


print(

    "Duplicates removed:",

    before - after

)


# ======================================
# 18. RESET INDEX
# ======================================

combined = combined.reset_index(
    drop=True
)


# ======================================
# 19. SHOW FINAL RESULTS
# ======================================

print("\n======================================")

print(
    "FINAL DATASET:",
    len(combined)
)

print("======================================")


print("\nLabel distribution:")

print(
    combined["labels"].value_counts()
)


print("\nLanguage distribution:")

print(
    combined["language"].value_counts()
)


# ======================================
# 20. SAVE FINAL DATASET
# ======================================

output_file = (
    "dataset/combined_scam_dataset.csv"
)


combined.to_csv(

    output_file,

    index=False,

    encoding="utf-8-sig"

)


print("\n======================================")

print("✅ COMBINED DATASET CREATED!")

print("======================================")

print(
    output_file
)