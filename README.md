# OTP Token Generator

A simple desktop application built with Python and tkinter to generate TOTP (Time-based One-Time Password) tokens from OTPAuth URIs.

## Features

- **Simple GUI**: Clean and intuitive user interface
- **TOTP Support**: Generates time-based one-time passwords
- **Real-time Updates**: Tokens automatically refresh every 30 seconds
- **Progress Bar**: Visual indicator showing time until next token
- **Cross-platform**: Works on Linux and macOS
- **Example URI**: Built-in example for testing

## Requirements

- Python 3.6 or higher
- tkinter (usually comes built-in with Python)

## Installation

1. **Clone or download** this repository to your local machine

2. **Install dependencies**:

   ```bash
   pip install .
   ```
## Usage

1. **Run the application**:

   ```bash
   python otp_generator.py
   ```

2. **Enter an OTPAuth URI** in the input field. The format should be:

   ```
   otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
   ```

3. **Click "Generate Token"** to start generating TOTP tokens

4. **View the current token** in the large blue text display

5. **Monitor the countdown** showing seconds until the next token

6. **Use the progress bar** to visualize time progression

## OTPAuth URI Format

The application expects OTPAuth URIs in the following format:

```
otpauth://totp/[label]?secret=[secret]&issuer=[issuer]
```

Where:

- `[label]` is the account identifier (e.g., "<alice@google.com>")
- `[secret]` is the base32-encoded secret key
- `[issuer]` is the service name (e.g., "Google")

## Example

The application includes a working example URI:

```
otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
```

You can click "Copy Example" to copy this URI to your clipboard for testing.

## How TOTP Works

TOTP (Time-based One-Time Password) generates 6-digit codes that change every 30 seconds based on:

- A shared secret key
- The current Unix timestamp
- A cryptographic hash function (HMAC-SHA1)

This is the same technology used by Google Authenticator, Authy, and other 2FA apps.

## Troubleshooting

### Common Issues

1. **"Invalid OTPAuth URI format"**: Make sure the URI starts with `otpauth://totp/`

2. **"No secret found in URI"**: Ensure the URI contains a `secret` parameter

3. **Import errors**: Make sure you have installed the required packages:

   ```bash
   pip install .
   ```

   Or install pyotp directly:

   ```bash
   pip install pyotp
   ```

4. **tkinter not found**: On some Linux distributions, you may need to install tkinter separately:

   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk

   # CentOS/RHEL
   sudo yum install tkinter
   ```

### Getting OTPAuth URIs

You can get OTPAuth URIs from:

- QR codes in 2FA setup screens
- Manual entry in authenticator apps
- Exporting from existing authenticator apps

## Security Notes

- **Never share your secret keys** - they are used to generate your 2FA codes
- **Keep your device secure** - anyone with access to your device can generate codes
- **Use HTTPS** when setting up 2FA to prevent interception of secrets

## Development

The application is built with:

- **Python 3.6+**: Core programming language
- **tkinter**: GUI framework (built-in)
- **pyotp**: TOTP implementation library
- **threading**: For background token updates

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.
