#!/usr/bin/env python3
"""
Test script for OTP Token Generator
This script tests the basic functionality without the GUI.
"""

import pyotp


def test_totp_generation():
    """Test TOTP token generation"""
    print("Testing TOTP token generation...")

    # Test secret from the example URI
    secret = "JBSWY3DPEHPK3PXP"

    # Create TOTP object
    totp = pyotp.TOTP(secret)

    # Generate current token
    current_token = totp.now()
    print(f"Current token: {current_token}")

    # Verify token format (should be 6 digits)
    if len(current_token) == 6 and current_token.isdigit():
        print("✓ Token format is correct (6 digits)")
    else:
        print("✗ Token format is incorrect")

    # Test URI parsing
    test_uri = (
        "otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"
    )
    print(f"\nTesting URI parsing: {test_uri}")

    try:
        from urllib.parse import parse_qs, urlparse

        parsed = urlparse(test_uri)
        query_params = parse_qs(parsed.query)
        extracted_secret = query_params.get("secret", [None])[0]

        if extracted_secret == secret:
            print("✓ URI parsing successful")
        else:
            print("✗ URI parsing failed")

    except Exception as e:
        print(f"✗ URI parsing error: {e}")

    # Test token validation
    print("\nTesting token validation...")
    if totp.verify(current_token):
        print("✓ Current token is valid")
    else:
        print("✗ Current token validation failed")

    # Test with a wrong token
    wrong_token = "000000"
    if not totp.verify(wrong_token):
        print("✓ Wrong token correctly rejected")
    else:
        print("✗ Wrong token incorrectly accepted")

    print("\nAll tests completed!")


if __name__ == "__main__":
    test_totp_generation()
