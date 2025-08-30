#!/usr/bin/env python3
"""
Test script for OTP Token Generator
This script tests the basic functionality without the GUI.
"""

import pyotp


def test_totp_generation() -> None:
    """Test TOTP token generation"""
    # Test secret from the example URI
    secret = "JBSWY3DPEHPK3PXP"

    # Create TOTP object
    totp = pyotp.TOTP(secret)

    # Generate current token
    current_token = totp.now()

    # Verify token format (should be 6 digits)
    assert len(current_token) == 6 and current_token.isdigit(), "Token format is incorrect"

    # Test URI parsing
    test_uri = (
        "otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"
    )
    from urllib.parse import parse_qs, urlparse
    parsed = urlparse(test_uri)
    query_params = parse_qs(parsed.query)
    extracted_secret = query_params.get("secret", [None])[0]
    assert extracted_secret == secret, "URI parsing failed"

    # Test token validation
    assert totp.verify(current_token), "Current token validation failed"

    # Test with a wrong token
    wrong_token = "000000"
    assert not totp.verify(wrong_token), "Wrong token incorrectly accepted"


