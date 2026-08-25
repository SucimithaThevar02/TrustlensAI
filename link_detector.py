import re
from urllib.parse import urlparse


def detect_links(text):

    # ==========================================
    # FIND URLS
    # ==========================================

    # First find normal URLs
    url_pattern = r'https?://[^\s<>"\']+|www\.[^\s<>"\']+'

    links = re.findall(url_pattern, text, re.IGNORECASE)

    # ==========================================
    # HANDLE MARKDOWN LINKS
    # ==========================================

    # Example:
    # [http://google.com](http://google.com)

    markdown_pattern = r'\[([^\]]+)\]\((https?://[^\s\)]+)\)'

    markdown_links = re.findall(
        markdown_pattern,
        text,
        re.IGNORECASE
    )

    # If markdown link exists, use actual URL
    if markdown_links:

        links = [url for label, url in markdown_links]

    # Remove duplicates
    links = list(dict.fromkeys(links))

    # ==========================================
    # NO LINK FOUND
    # ==========================================

    if not links:

        return {
            "status": "No Link Detected",
            "risk": "Low",
            "score": 0,
            "links": [],
            "reasons": [
                "No web link was found in the entered text."
            ],
            "recommendation":
                "No link was detected. Continue to be careful with unexpected messages."
        }

    # ==========================================
    # VARIABLES
    # ==========================================

    score = 0
    reasons = []

    # ==========================================
    # SUSPICIOUS WORDS
    # ==========================================

    suspicious_words = [
        "prize",
        "lottery",
        "winner",
        "winning",
        "reward",
        "claim",
        "free",
        "gift",
        "bonus",
        "urgent",
        "verify",
        "verification",
        "account",
        "suspended",
        "blocked",
        "security",
        "refund",
        "cash",
        "money",
        "offer",
        "coupon",
        "congratulations",
        "selected"
    ]

    # ==========================================
    # CHECK EACH LINK
    # ==========================================

    for link in links:

        # Remove punctuation accidentally captured
        clean_link = link.rstrip(".,!?;:)]}")

        # Add HTTPS for www links
        parse_link = clean_link

        if parse_link.lower().startswith("www."):
            parse_link = "https://" + parse_link

        parsed = urlparse(parse_link)

        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        # Remove username/password if present
        if "@" in domain:
            domain_without_auth = domain.split("@")[-1]
        else:
            domain_without_auth = domain

        # ======================================
        # 1. HTTP CHECK
        # ======================================

        if clean_link.lower().startswith("http://"):

            score += 2

            reasons.append(
                "⚠️ Link uses HTTP instead of HTTPS."
            )

        # ======================================
        # 2. SUSPICIOUS WORDS
        # ======================================

        found_words = []

        for word in suspicious_words:

            if word in clean_link.lower():

                found_words.append(word)

        if found_words:

            word_score = min(len(found_words), 3)

            score += word_score

            reasons.append(
                "⚠️ Suspicious words found in link: "
                + ", ".join(found_words)
            )

        # ======================================
        # 3. IP ADDRESS CHECK
        # ======================================

        ip_pattern = r'^(?:\d{1,3}\.){3}\d{1,3}$'

        if re.match(ip_pattern, domain_without_auth):

            score += 4

            reasons.append(
                "🚨 Link uses an IP address instead of a normal domain name."
            )

        # ======================================
        # 4. @ SYMBOL CHECK
        # ======================================

        if "@" in clean_link:

            score += 4

            reasons.append(
                "🚨 Link contains '@', which can be used to disguise "
                "the actual destination."
            )

        # ======================================
        # 5. VERY LONG URL
        # ======================================

        if len(clean_link) > 100:

            score += 2

            reasons.append(
                "⚠️ Link is unusually long."
            )

        # ======================================
        # 6. MANY SUBDOMAINS
        # ======================================

        domain_parts = domain_without_auth.split(".")

        if len(domain_parts) >= 4:

            score += 2

            reasons.append(
                "⚠️ Link contains an unusually large number of subdomains."
            )

        # ======================================
        # 7. MULTIPLE HYPHENS
        # ======================================

        hyphen_count = domain_without_auth.count("-")

        if hyphen_count >= 2:

            score += 2

            reasons.append(
                "⚠️ Domain contains multiple hyphens."
            )

        # ======================================
        # 8. SUSPICIOUS FILE EXTENSIONS
        # ======================================

        suspicious_extensions = [
            ".exe",
            ".scr",
            ".bat",
            ".cmd",
            ".apk"
        ]

        for extension in suspicious_extensions:

            if extension in path:

                score += 4

                reasons.append(
                    "🚨 Link points to a potentially dangerous file type: "
                    + extension
                )

                break

        # ======================================
        # 9. SENSITIVE PATH
        # ======================================

        sensitive_words = [
            "login",
            "signin",
            "verify",
            "verification",
            "password",
            "otp",
            "bank",
            "wallet"
        ]

        found_sensitive = []

        for word in sensitive_words:

            if word in path:

                found_sensitive.append(word)

        if found_sensitive:

            score += 1

            reasons.append(
                "⚠️ Link contains a sensitive login or verification path."
            )

    # ==========================================
    # REMOVE DUPLICATE REASONS
    # ==========================================

    reasons = list(dict.fromkeys(reasons))

    # ==========================================
    # NO WARNING SIGNS
    # ==========================================

    if not reasons:

        reasons = [
            "No major suspicious patterns were detected in the link."
        ]

    # ==========================================
    # RISK LEVEL
    # ==========================================

    if score >= 6:

        risk = "High"
        status = "Suspicious Link"

        recommendation = (
            "🚨 Do not open this link. Verify the sender and website "
            "through an official source before taking any action."
        )

    elif score >= 2:

        risk = "Medium"
        status = "Potentially Suspicious"

        recommendation = (
            "⚠️ Be careful with this link. Verify the website and sender "
            "before opening it or entering personal information."
        )

    else:

        risk = "Low"
        status = "Link Detected"

        recommendation = (
            "✅ No major warning signs were detected by our current checks. "
            "Always verify unexpected links before opening them."
        )

    # ==========================================
    # FINAL RESULT
    # ==========================================

    return {
        "status": status,
        "risk": risk,
        "score": score,
        "links": links,
        "reasons": reasons,
        "recommendation": recommendation
    }