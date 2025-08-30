#!/usr/bin/env python3
"""
OTP Token Generator
A simple desktop application to generate TOTP tokens from otpauth URIs.
"""

import time
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional
from urllib.parse import parse_qs, urlparse

import pyotp


class OTPGeneratorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("OTP Token Generator")
        self.root.geometry("650x450")
        self.root.resizable(True, True)

        # Configure style
        style = ttk.Style()
        style.theme_use("clam")

        # Variables
        self.current_token: tk.StringVar = tk.StringVar()
        self.time_remaining: tk.StringVar = tk.StringVar()
        self.otpauth_uri: tk.StringVar = tk.StringVar()
        self.otpauth_uri.set(
            "otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"
        )
        self.totp: Optional[pyotp.TOTP] = None
        self.running: bool = False

        self.setup_ui()
        self.start_token_update()

    def setup_ui(self) -> None:
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))  # type: ignore

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=0)  # Keep paste button at fixed size

        # Title
        title_label = ttk.Label(
            main_frame, text="OTP Token Generator", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # OTPAuth URI input
        ttk.Label(main_frame, text="OTPAuth URI:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        uri_entry = ttk.Entry(main_frame, textvariable=self.otpauth_uri, width=50)
        uri_entry.grid(row=1, column=1, sticky="we", padx=(10, 0), pady=5)

        # Paste from clipboard button
        paste_btn = ttk.Button(
            main_frame, text="Paste", command=self.paste_from_clipboard, width=4
        )
        paste_btn.grid(row=1, column=2, sticky="w", padx=(10, 0), pady=5)

        # Generate button
        generate_btn = ttk.Button(
            main_frame, text="Generate Token", command=self.generate_token
        )
        generate_btn.grid(row=2, column=0, columnspan=3, pady=20)

        # Token display
        token_frame = ttk.LabelFrame(main_frame, text="Current Token", padding="10")
        token_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)  # type: ignore
        token_frame.columnconfigure(0, weight=1)

        self.token_label = ttk.Label(
            token_frame,
            textvariable=self.current_token,
            font=("Courier", 24, "bold"),
            foreground="blue",
        )
        self.token_label.grid(row=0, column=0, pady=10)

        # Time remaining
        time_label = ttk.Label(
            token_frame, textvariable=self.time_remaining, font=("Arial", 12)
        )
        time_label.grid(row=1, column=0, pady=5)

        # Progress bar
        self.progress_bar = ttk.Progressbar(token_frame, mode="determinate", length=200)
        self.progress_bar.grid(row=2, column=0, pady=10)

        # Copy token button
        copy_token_btn = ttk.Button(
            token_frame,
            text="Copy Token to Clipboard",
            command=self.copy_token_to_clipboard,
        )
        copy_token_btn.grid(row=3, column=0, pady=10)

    def copy_to_clipboard(self, text: str) -> None:
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def copy_token_to_clipboard(self) -> None:
        """Copy current token to clipboard"""
        if self.current_token.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_token.get())
        else:
            messagebox.showerror("Error", "No token available to copy")

    def paste_from_clipboard(self) -> None:
        """Paste OTPAuth URI from clipboard"""
        try:
            if clipboard_content := self.root.clipboard_get():
                self.otpauth_uri.set(clipboard_content.strip())
            else:
                messagebox.showerror("Error", "Clipboard is empty")
        except tk.TclError:
            messagebox.showerror("Error", "No text content in clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste from clipboard: {str(e)}")

    def parse_otpauth_uri(self, uri: str) -> str:
        """Parse OTPAuth URI and extract secret"""
        try:
            # Basic validation
            if not uri.startswith("otpauth://"):
                raise ValueError("Invalid OTPAuth URI format")

            # Parse the URI
            parsed = urlparse(uri)
            if parsed.scheme != "otpauth" or parsed.netloc != "totp":
                raise ValueError("Only TOTP is supported")

            # Extract query parameters
            query_params = parse_qs(parsed.query)
            secret = query_params.get("secret", [None])[0]

            if not secret:
                raise ValueError("No secret found in URI")

            return secret

        except ValueError as ve:
            raise ValueError(f"Failed to parse OTPAuth URI: {str(ve)}")
        except Exception as e:
            import logging
            logging.exception("Unexpected error while parsing OTPAuth URI")
            raise

    def generate_token(self) -> None:
        """Generate TOTP token from the entered URI"""
        uri = self.otpauth_uri.get().strip()

        if not uri:
            messagebox.showerror("Error", "Please enter an OTPAuth URI")
            return

        try:
            secret = self.parse_otpauth_uri(uri)
            self.totp = pyotp.TOTP(secret)

            # Generate initial token
            self.update_token()

            # Start automatic updates
            if not self.running:
                self.running = True
                self.start_token_update()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def update_token(self) -> None:
        """Update the current token and time remaining"""
        if not self.totp:
            return

        try:
            # Generate current token
            token = self.totp.now()
            self.current_token.set(token)

            # Calculate time remaining
            current_time = int(time.time())
            time_step = 30  # TOTP uses 30-second intervals
            time_remaining = time_step - (current_time % time_step)

            self.time_remaining.set(f"Next token in: {time_remaining} seconds")

            # Update progress bar
            progress = ((time_step - time_remaining) / time_step) * 100
            self.progress_bar["value"] = progress

        except Exception as e:
            messagebox.showerror("Token Update Error", f"Failed to update token: {str(e)}")
            self.current_token.set("")
            self.time_remaining.set("Token unavailable")
            self.progress_bar["value"] = 0

    def start_token_update(self) -> None:
        """Start the automatic updates using tkinter's after method"""
        if self.running:
            self.update_token()
            # Schedule next update in 1 second
            self.root.after(1000, self.start_token_update)

    def on_closing(self) -> None:
        """Handle application closing"""
        self.running = False
        self.root.destroy()


def main() -> None:
    """Main function to run the application"""
    root = tk.Tk()
    app = OTPGeneratorApp(root)

    # Set up closing handler
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
