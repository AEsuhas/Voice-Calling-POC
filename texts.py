"""Voice prompts (TTS) per language, with template ids/versions for the audit trail.

Placeholders: {t} ticket, {s} site, {alarm} optional alarm sentence, {ack}/{rej} DTMF digits,
{name} technician name, {reason} escalation reason sentence, {n} number of calls.
"""
from xml.sax.saxutils import escape

from config import CFG

TEMPLATES = {  # purpose -> (template id, version) recorded on every call
    "technician": ("uc1_technician_ack", "v1"),
    "escalation": ("uc1_escalation", "v1"),
    "reminder": ("uc1_followup_reminder", "v1"),
}

LANGS = {
    "en": {
        "name": "English", "voice": "Polly.Aditi", "language": "en-IN",
        "menu": "For English, press {n}.",
        "alarm": " Alarm {a}.",
        "technician": "Hello. This is the Automation Edge helpdesk. Ticket {t} has been assigned to you, "
                      "at site {s}.{alarm} Press {ack} to acknowledge this ticket. Press {rej} to reject it.",
        "escalation": "Hello. This is the Automation Edge helpdesk escalation. Ticket {t}, at site {s}.{alarm} "
                      "The technician {name} {reason}. Please follow up in NexTask.",
        "escalation_confirm": "Press {ack} to confirm that you will follow up.",
        "confirmed": "Thank you. Your confirmation has been recorded. Goodbye.",
        "reason_rejected": "has rejected the assignment",
        "reason_no_ack": "has not acknowledged the assignment after {n} calls",
        "reminder": "Reminder from the Automation Edge helpdesk. Ticket {t}, at site {s}, is still waiting for "
                    "your status update. Please update departed, arrived or started in NexTask.",
        "ack": "Thank you. Your acknowledgement has been recorded. Goodbye.",
        "reject": "Your rejection has been recorded. The ticket will be escalated. Goodbye.",
        "invalid": "Sorry, that is not a valid option.",
        "noinput": "We did not receive any input. Goodbye.",
        "goodbye": "Goodbye.",
    },
    "ar": {
        "name": "Arabic", "voice": "Polly.Zeina", "language": "arb",
        "menu": "للعربية، اضغط {n}.",
        "alarm": " التنبيه {a}.",
        "technician": "مرحبا. هذا مكتب المساعدة من أوتوميشن إيدج. تم تعيين التذكرة {t} لك، في الموقع {s}.{alarm} "
                      "اضغط {ack} لتأكيد الاستلام. اضغط {rej} للرفض.",
        "escalation": "مرحبا. هذا تصعيد من مكتب المساعدة. التذكرة {t}، في الموقع {s}.{alarm} "
                      "الفني {name} {reason}. يرجى المتابعة في نكست تاسك.",
        "escalation_confirm": "اضغط {ack} لتأكيد أنك ستتابع.",
        "confirmed": "شكرا لك. تم تسجيل تأكيدك. مع السلامة.",
        "reason_rejected": "رفض المهمة",
        "reason_no_ack": "لم يؤكد استلام المهمة بعد {n} مكالمات",
        "reminder": "تذكير من مكتب المساعدة. التذكرة {t} في الموقع {s} ما زالت بانتظار تحديث حالتك. "
                    "يرجى تحديث الحالة في نكست تاسك: غادرت، وصلت أو بدأت.",
        "ack": "شكرا لك. تم تسجيل تأكيد الاستلام. مع السلامة.",
        "reject": "تم تسجيل الرفض وسيتم تصعيد التذكرة. مع السلامة.",
        "invalid": "عذرا، هذا خيار غير صالح.",
        "noinput": "لم نتلق أي إدخال. مع السلامة.",
        "goodbye": "مع السلامة.",
    },
    # Twilio <Say> has no Urdu voice: spoken Urdu is written in Devanagari and read by the Hindi voice.
    "ur": {
        "name": "Urdu", "voice": "Polly.Aditi", "language": "hi-IN",
        "menu": "उर्दू के लिए {n} दबाइए।",
        "alarm": " अलार्म {a}।",
        "technician": "अस्सलाम-ओ-अलैकुम। यह ऑटोमेशन एज हेल्पडेस्क है। टिकट {t} आपको दिया गया है, साइट {s}।{alarm} "
                      "टिकट क़ुबूल करने के लिए {ack} दबाइए। मुस्तरद करने के लिए {rej} दबाइए।",
        "escalation": "अस्सलाम-ओ-अलैकुम। यह हेल्पडेस्क एस्केलेशन है। टिकट {t}, साइट {s}।{alarm} "
                      "टेक्नीशियन {name} {reason}। बराए मेहरबानी नेक्स्ट टास्क में फ़ॉलो-अप कीजिए।",
        "escalation_confirm": "फ़ॉलो-अप की तस्दीक़ के लिए {ack} दबाइए।",
        "confirmed": "शुक्रिया। आपकी तस्दीक़ दर्ज कर ली गई है। ख़ुदा हाफ़िज़।",
        "reason_rejected": "ने असाइनमेंट मुस्तरद कर दिया है",
        "reason_no_ack": "ने {n} कॉल के बाद भी असाइनमेंट क़ुबूल नहीं किया",
        "reminder": "हेल्पडेस्क की याद-दहानी। टिकट {t}, साइट {s}, पर आपका स्टेटस अपडेट अभी बाक़ी है। "
                    "बराए मेहरबानी नेक्स्ट टास्क में रवाना, पहुँच गए या काम शुरू, अपडेट कीजिए।",
        "ack": "शुक्रिया। आपकी तस्दीक़ दर्ज कर ली गई है। ख़ुदा हाफ़िज़।",
        "reject": "आपका इनकार दर्ज कर लिया गया है। टिकट आगे भेजा जाएगा। ख़ुदा हाफ़िज़।",
        "invalid": "माज़रत, यह दुरुस्त इंतिख़ाब नहीं है।",
        "noinput": "हमें कोई जवाब नहीं मिला। ख़ुदा हाफ़िज़।",
        "goodbye": "ख़ुदा हाफ़िज़।",
    },
    "hi": {
        "name": "Hindi", "voice": "Polly.Aditi", "language": "hi-IN",
        "menu": "हिंदी के लिए {n} दबाएं।",
        "alarm": " अलार्म {a}।",
        "technician": "नमस्ते। यह ऑटोमेशन एज हेल्पडेस्क है। टिकट {t} आपको सौंपा गया है, साइट {s}।{alarm} "
                      "टिकट स्वीकार करने के लिए {ack} दबाएं। अस्वीकार करने के लिए {rej} दबाएं।",
        "escalation": "नमस्ते। यह हेल्पडेस्क एस्केलेशन है। टिकट {t}, साइट {s}।{alarm} "
                      "तकनीशियन {name} {reason}। कृपया नेक्स्ट टास्क में फ़ॉलो-अप करें।",
        "escalation_confirm": "फ़ॉलो-अप की पुष्टि के लिए {ack} दबाएं।",
        "confirmed": "धन्यवाद। आपकी पुष्टि दर्ज कर ली गई है। अलविदा।",
        "reason_rejected": "ने असाइनमेंट अस्वीकार कर दिया है",
        "reason_no_ack": "ने {n} कॉल के बाद भी असाइनमेंट स्वीकार नहीं किया",
        "reminder": "हेल्पडेस्क रिमाइंडर। टिकट {t}, साइट {s}, पर आपका स्टेटस अपडेट बाकी है। "
                    "कृपया नेक्स्ट टास्क में डिपार्टेड, अराइव्ड या स्टार्टेड अपडेट करें।",
        "ack": "धन्यवाद। आपकी स्वीकृति दर्ज कर ली गई है। अलविदा।",
        "reject": "आपका अस्वीकार दर्ज कर लिया गया है। टिकट आगे भेजा जाएगा। अलविदा।",
        "invalid": "क्षमा करें, यह मान्य विकल्प नहीं है।",
        "noinput": "हमें कोई इनपुट नहीं मिला। अलविदा।",
        "goodbye": "अलविदा।",
    },
}

# Language menu order (key 1, 2, 3 ...), used only when a recipient's language is "ask"
MENU = [c for c in CFG["menu_languages"].replace(" ", "").split(",") if c in LANGS] or ["en"]


def resolve_language(preferred):
    """(language, source): NexTask preference > configured fallback; 'ask' -> caller menu."""
    pref = (preferred or "").strip().lower()
    if pref in LANGS:
        return pref, "nextask"
    if pref == "ask":
        return None, "menu"
    fallback = CFG["default_language"] if CFG["default_language"] in LANGS else "en"
    return fallback, "fallback"


def spell(text):
    """Read short codes (INC0012345, ALM-77) character by character; longer text as words."""
    text = str(text or "").strip()
    return " ".join(text) if text and " " not in text and len(text) <= 14 else text


def site_words(ticket):
    number, name = ticket.get("site_number"), ticket.get("site_name")
    if number and name:
        return f"{spell(number)}, {name}"
    return spell(number) if number else (name or "unknown")


def voice_text(lang, key, ticket=None, **kw):
    L = LANGS[lang]
    if ticket is not None:
        kw.setdefault("t", spell(ticket["ticket_id"]))
        kw.setdefault("s", site_words(ticket))
        kw.setdefault("alarm", L["alarm"].format(a=spell(ticket["alarm_id"])) if ticket.get("alarm_id") else "")
    return L[key].format(**kw)


def say(lang, text):
    v = LANGS.get(lang, LANGS["en"])
    return f'<Say voice="{v["voice"]}" language="{v["language"]}">{escape(text)}</Say>'
