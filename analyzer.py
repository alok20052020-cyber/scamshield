
import re
from urllib.parse import urlparse

def analyze_input(text, input_type):
    score = 0
    indicators = []

    if input_type == "url":
        url = text.strip()

        parsed = urlparse(
            url if "://" in url else "//" + url
        )

        hostname = parsed.hostname or ""

        if len(url) > 75:
            score += 1
            indicators.append("URL is unusually long")

        shorteners = [
            "bit.ly", "tinyurl.com", "t.co",
            "is.gd", "cutt.ly"
        ]

        if any(domain in hostname.lower() for domain in shorteners):
            score += 2
            indicators.append("URL uses a link shortener")

        if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", hostname):
            score += 2
            indicators.append("URL uses an IP address")

        if "@" in url:
            score += 2
            indicators.append("URL contains an @ symbol")

        if "xn--" in hostname:
            score += 2
            indicators.append("URL contains unusual encoded characters")

    elif input_type == "message":
        message = text.lower()

        keywords = {
            "otp": "Message asks for an OTP",
            "password": "Message mentions a password",
            "urgent": "Message uses urgency",
            "immediately": "Message creates urgency",
           "account is blocked": "Message claims an account is blocked",
            "verify your account": "Message asks for account verification",
            "bank details": "Message asks for bank details",
            "send money": "Message asks to send money",
            "prize": "Message mentions a prize",
            "click here": "Message asks you to click a link"
        }

        for keyword, reason in keywords.items():
            if keyword in message:
                score += 1
                indicators.append(reason)

    if score >= 4:
        risk = "HIGH RISK"
        advice = "Be very careful. Do not click suspicious links or share personal information."

    elif score >= 2:
        risk = "MEDIUM RISK"
        advice = "Check the source carefully before taking any action."

    else:
        risk = "LOW RISK"
        advice = "No major warning indicators were found. Still verify the source independently."

    if not indicators:
        indicators.append("No suspicious indicators found by the basic checker")

    return {
        "risk": risk,
        "score": score,
        "indicators": indicators,
        "advice": advice
    }
