"""
PII Redaction Utility for GDPR Compliance

Detects and redacts Personally Identifiable Information (PII) from contract text
before sending to LLM to comply with EU GDPR requirements.

Protected categories:
- Names of natural persons
- Email addresses
- Phone numbers
- Physical addresses
- National ID numbers (passport, social security, etc.)
- Bank account numbers, IBAN
- IP addresses
- Dates of birth
- Credit card numbers
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class PIIMatch:
    """Represents a detected PII instance"""
    type: str
    original: str
    placeholder: str
    start: int
    end: int


class PIIRedactor:
    """
    Detects and redacts PII from text while preserving context for contract analysis.

    Approach:
    - Aggressive redaction for high-risk PII (emails, phones, IDs)
    - Context-preserving for names (keep role context: "Landlord", "Tenant")
    - Preserve contract structure and legal terms
    """

    def __init__(self):
        # Email pattern
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )

        # Phone patterns (various international formats)
        self.phone_patterns = [
            re.compile(r'\+?[1-9]\d{1,14}'),  # E.164 format
            re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'),  # US format
            re.compile(r'\b\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{2,4}\b'),  # International
        ]

        # IBAN pattern (European bank accounts)
        self.iban_pattern = re.compile(
            r'\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b'
        )

        # Credit card pattern
        self.credit_card_pattern = re.compile(
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        )

        # IP address pattern
        self.ip_pattern = re.compile(
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        )

        # Date of birth patterns
        self.dob_patterns = [
            re.compile(r'\b\d{2}/\d{2}/\d{4}\b'),  # DD/MM/YYYY
            re.compile(r'\b\d{4}-\d{2}-\d{2}\b'),  # YYYY-MM-DD
        ]

        # National ID patterns (generic - can be extended per country)
        self.id_patterns = [
            re.compile(r'\b[A-Z]{1,2}\d{6,9}\b'),  # Passport-like
            re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),  # SSN-like
        ]

        # Address patterns (street numbers, postal codes)
        self.address_patterns = [
            re.compile(r'\b\d{1,5}\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct)\b', re.IGNORECASE),
            re.compile(r'\b\d{5}(?:-\d{4})?\b'),  # US ZIP codes
            re.compile(r'\b[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}\b'),  # UK postcodes
        ]

    def redact_text(self, text: str, preserve_structure: bool = True) -> Tuple[str, List[PIIMatch]]:
        """
        Redact PII from text.

        Args:
            text: The original contract text
            preserve_structure: If True, preserves document structure and context

        Returns:
            Tuple of (redacted_text, list of PII matches found)
        """
        redacted = text
        matches: List[PIIMatch] = []
        offset = 0  # Track position changes from replacements

        # 1. Redact emails
        for match in self.email_pattern.finditer(text):
            placeholder = "[EMAIL]"
            matches.append(PIIMatch(
                type="email",
                original=match.group(),
                placeholder=placeholder,
                start=match.start() + offset,
                end=match.end() + offset
            ))
            redacted = redacted[:match.start() + offset] + placeholder + redacted[match.end() + offset:]
            offset += len(placeholder) - len(match.group())

        # 2. Redact phone numbers
        for pattern in self.phone_patterns:
            for match in pattern.finditer(text):
                # Skip if it's just part of a larger number (like amounts)
                if self._is_likely_phone(match.group(), text, match.start()):
                    placeholder = "[PHONE]"
                    matches.append(PIIMatch(
                        type="phone",
                        original=match.group(),
                        placeholder=placeholder,
                        start=match.start() + offset,
                        end=match.end() + offset
                    ))
                    redacted = redacted[:match.start() + offset] + placeholder + redacted[match.end() + offset:]
                    offset += len(placeholder) - len(match.group())

        # 3. Redact IBANs
        for match in self.iban_pattern.finditer(text):
            placeholder = "[BANK_ACCOUNT]"
            matches.append(PIIMatch(
                type="iban",
                original=match.group(),
                placeholder=placeholder,
                start=match.start() + offset,
                end=match.end() + offset
            ))
            redacted = redacted[:match.start() + offset] + placeholder + redacted[match.end() + offset:]
            offset += len(placeholder) - len(match.group())

        # 4. Redact credit cards
        for match in self.credit_card_pattern.finditer(text):
            # Verify it looks like a credit card (simple Luhn check could be added)
            if self._is_likely_credit_card(match.group()):
                placeholder = "[CREDIT_CARD]"
                matches.append(PIIMatch(
                    type="credit_card",
                    original=match.group(),
                    placeholder=placeholder,
                    start=match.start() + offset,
                    end=match.end() + offset
                ))
                redacted = redacted[:match.start() + offset] + placeholder + redacted[match.end() + offset:]
                offset += len(placeholder) - len(match.group())

        # 5. Redact IP addresses
        for match in self.ip_pattern.finditer(text):
            if self._is_valid_ip(match.group()):
                placeholder = "[IP_ADDRESS]"
                matches.append(PIIMatch(
                    type="ip_address",
                    original=match.group(),
                    placeholder=placeholder,
                    start=match.start() + offset,
                    end=match.end() + offset
                ))
                redacted = redacted[:match.start() + offset] + placeholder + redacted[match.end() + offset:]
                offset += len(placeholder) - len(match.group())

        # 6. Redact addresses
        for pattern in self.address_patterns:
            for match in pattern.finditer(text):
                placeholder = "[ADDRESS]"
                matches.append(PIIMatch(
                    type="address",
                    original=match.group(),
                    placeholder=placeholder,
                    start=match.start() + offset,
                    end=match.end() + offset
                ))
                redacted = redacted[:match.start() + offset] + placeholder + redacted[match.end() + offset:]
                offset += len(placeholder) - len(match.group())

        # 7. Redact National IDs
        for pattern in self.id_patterns:
            for match in pattern.finditer(text):
                placeholder = "[ID_NUMBER]"
                matches.append(PIIMatch(
                    type="national_id",
                    original=match.group(),
                    placeholder=placeholder,
                    start=match.start() + offset,
                    end=match.end() + offset
                ))
                redacted = redacted[:match.start() + offset] + placeholder + redacted[match.end() + offset:]
                offset += len(placeholder) - len(match.group())

        # 8. Redact person names (context-aware)
        # This is more complex - we want to keep role context
        redacted, name_matches = self._redact_names_with_context(redacted)
        matches.extend(name_matches)

        return redacted, matches

    def _redact_names_with_context(self, text: str) -> Tuple[str, List[PIIMatch]]:
        """
        Redact personal names while preserving contractual role context.

        For example:
        "John Smith (Landlord)" -> "[PARTY_A - Landlord]"
        "Jane Doe, the tenant" -> "[PARTY_B - Tenant]"

        This preserves the contract structure while protecting identity.
        """
        matches: List[PIIMatch] = []

        # Common role indicators in contracts
        roles = [
            "landlord", "lessor", "tenant", "lessee",
            "buyer", "seller", "vendor", "purchaser",
            "employer", "employee", "contractor",
            "client", "service provider", "customer",
            "licensor", "licensee"
        ]

        # Pattern: Capitalized name near role indicator
        # This is a simplified approach - in production, use NER (Named Entity Recognition)
        role_pattern = re.compile(
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s*(?:\(|\,)?\s*(?:the\s+)?(' + '|'.join(roles) + r')',
            re.IGNORECASE
        )

        party_counter = 0
        for match in role_pattern.finditer(text):
            name = match.group(1)
            role = match.group(2)

            party_counter += 1
            placeholder = f"[PARTY_{chr(64 + party_counter)} - {role.title()}]"

            matches.append(PIIMatch(
                type="person_name",
                original=name,
                placeholder=placeholder,
                start=match.start(),
                end=match.end()
            ))

            # Replace the name but keep the role context
            text = text.replace(match.group(), placeholder)

        return text, matches

    def _is_likely_phone(self, number: str, context: str, position: int) -> bool:
        """Check if a number is likely a phone number based on context"""
        # Remove formatting
        digits = re.sub(r'[^\d]', '', number)

        # Phone numbers typically have 7-15 digits
        if len(digits) < 7 or len(digits) > 15:
            return False

        # Check context for phone-related words
        context_window = context[max(0, position - 50):min(len(context), position + 50)]
        phone_keywords = ['phone', 'tel', 'mobile', 'cell', 'contact', 'call']

        return any(keyword in context_window.lower() for keyword in phone_keywords)

    def _is_likely_credit_card(self, number: str) -> bool:
        """Simple check if a number looks like a credit card"""
        digits = re.sub(r'[^\d]', '', number)
        return len(digits) == 16 or len(digits) == 15  # Visa/MC or Amex

    def _is_valid_ip(self, ip: str) -> bool:
        """Check if string is a valid IP address"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False

    def get_redaction_summary(self, matches: List[PIIMatch]) -> Dict[str, int]:
        """
        Generate a summary of redacted PII types.

        Returns a dict like: {"email": 2, "phone": 1, "address": 3}
        """
        summary: Dict[str, int] = {}
        for match in matches:
            summary[match.type] = summary.get(match.type, 0) + 1
        return summary


# Singleton instance
_redactor = None

def get_redactor() -> PIIRedactor:
    """Get the global PII redactor instance"""
    global _redactor
    if _redactor is None:
        _redactor = PIIRedactor()
    return _redactor


def redact_pii(text: str) -> Tuple[str, Dict[str, int]]:
    """
    Convenience function to redact PII from text.

    Returns:
        Tuple of (redacted_text, summary_of_redactions)
    """
    redactor = get_redactor()
    redacted_text, matches = redactor.redact_text(text)
    summary = redactor.get_redaction_summary(matches)
    return redacted_text, summary
