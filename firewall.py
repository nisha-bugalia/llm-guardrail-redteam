import re

# RegEx patterns for common prompt injection, jailbreak, and policy-override attacks
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(all\s+)?(previous|above)\s+directives",
    r"you\s+are\s+now\s+in\s+DAN\s+mode",
    r"system\s+prompt\s+override",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"bypass\s+(safety|security)\s+filters?",
    r"jailbreak\s+mode",
]

def inspect_prompt(prompt: str) -> dict:
    """
    Scans an incoming text prompt against security rules.
    Returns a dict with safety status, risk score, and detailed reason.
    """
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return {
                "is_safe": False,
                "risk_score": 0.95,
                "flagged_pattern": pattern,
                "reason": "Prompt Injection / Jailbreak attempt detected"
            }
    
    return {
        "is_safe": True,
        "risk_score": 0.05,
        "flagged_pattern": None,
        "reason": "Clean prompt"
    }