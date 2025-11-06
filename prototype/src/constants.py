"""
Constants for Legally AI prototype
Includes UI strings in all supported languages
"""

# Supported languages
LANGUAGES = {
    "english": "English",
    "russian": "Русский",
    "serbian": "Српски",
    "french": "Français"
}

# Language codes for detection
LANG_CODES = {
    "en": "english",
    "ru": "russian",
    "sr": "serbian",
    "fr": "french"
}

# Screening result variants (exact text from spec)
SCREENING_RESULTS = {
    "no_major_issues": {
        "english": "Based only on what you shared, we didn't see major red flags.",
        "russian": "Судя по предоставленному документу, мы не обнаружили серьёзных проблем.",
        "serbian": "Na osnovu onoga što ste podelili, nismo uočili velike probleme.",
        "french": "D'après ce que vous avez partagé, nous n'avons pas détecté de problèmes majeurs."
    },
    "recommended_to_address": {
        "english": "The draft can work if the listed issues are fixed and captured in writing.",
        "russian": "Проект может работать, если указанные проблемы будут исправлены и зафиксированы письменно.",
        "serbian": "Nacrt može funkcionisati ako se navedeni problemi isprave i zabeleze u pisanoj formi.",
        "french": "Le projet peut fonctionner si les problèmes listés sont corrigés et documentés par écrit."
    },
    "high_risk": {
        "english": "As written, some provisions may be unlawful or unenforceable, or they present high risk.",
        "russian": "В текущем виде некоторые положения могут быть незаконными или неисполнимыми, либо представляют высокий риск.",
        "serbian": "U trenutnom obliku, neke odredbe mogu biti nezakonite ili neizvršive, ili predstavljaju visok rizik.",
        "french": "Tel quel, certaines clauses peuvent être illégales ou inapplicables, ou présentent un risque élevé."
    },
    "preliminary_review": {
        "english": "We can't reliably assess this draft due to poor scan/translation or missing parts. Please provide a clean, complete, governing-language copy with all schedules and annexes, then rerun the review.",
        "russian": "Мы не можем надёжно оценить этот проект из-за плохого качества сканирования/перевода или отсутствия частей. Предоставьте чистую, полную копию на основном языке со всеми приложениями, затем запустите проверку снова.",
        "serbian": "Ne možemo pouzdano proceniti ovaj nacrt zbog lošeg skeniranja/prevoda ili nedostajućih delova. Molimo vas da dostavite čist, kompletan primerak na izvornom jeziku sa svim prilozima, a zatim ponovo pokrenete proveru.",
        "french": "Nous ne pouvons pas évaluer ce projet de manière fiable en raison d'une mauvaise numérisation/traduction ou de parties manquantes. Veuillez fournir une copie propre et complète dans la langue d'origine avec toutes les annexes, puis relancez l'examen."
    }
}

# Important limits disclaimer (exact text from spec)
IMPORTANT_LIMITS = {
    "english": """**Important limits:** This is an AI-powered informational screening — not legal advice, not a law-firm review, and it does not create an attorney–client relationship. We looked only at the text you provided and did not verify facts, identities, authority to sign, ownership, required formalities, or compliance with local law. Attachments, the governing-language version, or later edits can change the result. Laws differ by country and state, so enforceability may vary. Don't rely on this summary alone; for meaningful stakes, read everything and consider speaking with a qualified lawyer.""",

    "russian": """**Важные ограничения:** Это информационная проверка на основе ИИ — не юридическая консультация, не обзор юридической фирмы, и она не создаёт отношений адвокат-клиент. Мы рассмотрели только предоставленный вами текст и не проверяли факты, личности, полномочия на подпись, право собственности, необходимые формальности или соответствие местному законодательству. Приложения, версия на основном языке или последующие правки могут изменить результат. Законы различаются по странам и регионам, поэтому исполнимость может варьироваться. Не полагайтесь только на этот анализ; при важных вопросах прочтите всё и рассмотрите возможность консультации с квалифицированным юристом.""",

    "serbian": """**Važna ograničenja:** Ovo je informativna provera zasnovana na AI — nije pravni savet, nije pregled advokatske kancelarije i ne stvara odnos advokat-klijent. Razmatrali smo samo tekst koji ste dostavili i nismo proveravali činjenice, identitete, ovlašćenje za potpisivanje, vlasništvo, potrebne formalnosti ili usklađenost sa lokalnim zakonima. Prilozi, verzija na izvornom jeziku ili naknadne izmene mogu promeniti rezultat. Zakoni se razlikuju po zemljama i državama, pa izvršivost može varirati. Ne oslanjajte se samo na ovaj pregled; za važna pitanja, pročitajte sve i razmotrite konsultaciju sa kvalifikovanim pravnikom.""",

    "french": """**Limites importantes:** Ceci est un examen informatif basé sur l'IA — pas un conseil juridique, pas un examen de cabinet d'avocats, et cela ne crée pas de relation avocat-client. Nous n'avons examiné que le texte que vous avez fourni et n'avons pas vérifié les faits, les identités, l'autorité de signature, la propriété, les formalités requises ou la conformité aux lois locales. Les pièces jointes, la version dans la langue d'origine ou les modifications ultérieures peuvent modifier le résultat. Les lois diffèrent selon les pays et les États, donc l'applicabilité peut varier. Ne vous fiez pas uniquement à cette analyse; pour des enjeux importants, lisez tout et envisagez de consulter un avocat qualifié."""
}

# UI Section headings
UI_STRINGS = {
    "english": {
        "summary_title": "Summary",
        "our_quick_take": "Our quick take",
        "important_limits_title": "Important limits",
        "confidence_title": "How sure we are",
        "about_contract": "What this agreement is about",
        "payment_title": "What you pay and when",
        "obligations_title": "What you agree to do (or not to do)",
        "check_terms": "Check these terms",
        "also_think": "Also think about",
        "ask_changes": "Ask for these changes",
        "sign_as_is": 'If you decide to sign "As Is"',
        "act_now": "Act now",
        "all_terms": "All key terms (simple)",
        "more_button": "Helpful, show me more",
        "analyzing": "Analyzing your contract...",
        "upload_prompt": "Upload your contract (PDF or DOCX)",
        "language_selector": "Show results in:",
        "confidence_high": "High",
        "confidence_medium": "Medium",
        "confidence_low": "Low"
    },
    "russian": {
        "summary_title": "Краткое содержание",
        "our_quick_take": "Наша оценка",
        "important_limits_title": "Важные ограничения",
        "confidence_title": "Насколько мы уверены",
        "about_contract": "О чём этот договор",
        "payment_title": "Что и когда вы платите",
        "obligations_title": "Что вы обязуетесь делать (или не делать)",
        "check_terms": "Проверьте эти условия",
        "also_think": "Также подумайте о",
        "ask_changes": "Запросите эти изменения",
        "sign_as_is": 'Если вы решите подписать "как есть"',
        "act_now": "Действуйте сейчас",
        "all_terms": "Все ключевые условия (простым языком)",
        "more_button": "Полезно, покажите ещё",
        "analyzing": "Анализируем ваш договор...",
        "upload_prompt": "Загрузите ваш договор (PDF или DOCX)",
        "language_selector": "Показать результаты на:",
        "confidence_high": "Высокая",
        "confidence_medium": "Средняя",
        "confidence_low": "Низкая"
    },
    "serbian": {
        "summary_title": "Rezime",
        "our_quick_take": "Naša procena",
        "important_limits_title": "Važna ograničenja",
        "confidence_title": "Koliko smo sigurni",
        "about_contract": "O čemu je ovaj ugovor",
        "payment_title": "Šta i kada plaćate",
        "obligations_title": "Šta se obavezujete da činite (ili ne činite)",
        "check_terms": "Proverite ove uslove",
        "also_think": "Takođe razmislite o",
        "ask_changes": "Zatražite ove izmene",
        "sign_as_is": 'Ako odlučite da potpišete "kakav jeste"',
        "act_now": "Delujte sada",
        "all_terms": "Svi ključni uslovi (jednostavno)",
        "more_button": "Korisno, pokažite mi još",
        "analyzing": "Analiziramo vaš ugovor...",
        "upload_prompt": "Otpremite svoj ugovor (PDF ili DOCX)",
        "language_selector": "Prikaži rezultate na:",
        "confidence_high": "Visoka",
        "confidence_medium": "Srednja",
        "confidence_low": "Niska"
    },
    "french": {
        "summary_title": "Résumé",
        "our_quick_take": "Notre évaluation rapide",
        "important_limits_title": "Limites importantes",
        "confidence_title": "Notre niveau de certitude",
        "about_contract": "De quoi parle cet accord",
        "payment_title": "Ce que vous payez et quand",
        "obligations_title": "Ce que vous vous engagez à faire (ou à ne pas faire)",
        "check_terms": "Vérifiez ces conditions",
        "also_think": "Pensez également à",
        "ask_changes": "Demandez ces modifications",
        "sign_as_is": 'Si vous décidez de signer "tel quel"',
        "act_now": "Agissez maintenant",
        "all_terms": "Toutes les conditions clés (simplement)",
        "more_button": "Utile, montrez-m'en plus",
        "analyzing": "Analyse de votre contrat...",
        "upload_prompt": "Téléchargez votre contrat (PDF ou DOCX)",
        "language_selector": "Afficher les résultats en:",
        "confidence_high": "Élevée",
        "confidence_medium": "Moyenne",
        "confidence_low": "Faible"
    }
}

# Contract types
CONTRACT_TYPES = {
    "lease": "Residential lease",
    "nda": "Non-Disclosure Agreement (NDA)",
    "employment": "Employment agreement",
    "tos": "Terms of Service",
    "vendor": "Vendor agreement",
    "freelance": "Freelance/Contractor agreement",
    "partnership": "Partnership agreement",
    "unknown": "Unknown agreement type"
}

# Negotiability levels
NEGOTIABILITY = {
    "high": "High — open negotiation likely",
    "medium": "Medium — some terms negotiable",
    "low": "Low — take-it-or-leave-it (click-wrap, big provider)"
}

# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    "high": 0.8,
    "medium": 0.5,
    "low": 0.0
}

# Quality score factors
QUALITY_FACTORS = {
    "poor_scan": 0.5,
    "missing_annexes": 0.8,
    "translation_without_original": 0.7,
    "ocr_used": 0.8,
    "partial_document": 0.6
}

# Hard gates (stop analysis if below threshold)
HARD_GATES = {
    "scan_legibility": 0.4,
    "coverage": 0.0  # Don't block on missing annexes for prototype testing
}

# Groq model settings
GROQ_SETTINGS = {
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.1,  # Low temperature for consistent, accurate extraction
    "max_tokens": 8000,
    "top_p": 0.9
}
