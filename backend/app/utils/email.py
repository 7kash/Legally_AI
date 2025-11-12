"""
Email Utilities
Send emails via SendGrid for authentication flows
"""

import logging
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from ..config import settings

logger = logging.getLogger(__name__)


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> bool:
    """
    Send an email via SendGrid

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email content
        text_content: Plain text email content (optional)

    Returns:
        True if email sent successfully, False otherwise
    """
    # Skip email sending if SendGrid API key not configured
    if not settings.SENDGRID_API_KEY or settings.SENDGRID_API_KEY.startswith("SG.your_"):
        logger.warning(
            f"SendGrid not configured. Would send email to {to_email} with subject: {subject}"
        )
        # In development, log the email content instead of sending
        logger.info(f"Email content:\n{html_content}")
        return True

    try:
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
            plain_text_content=text_content or ""
        )

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)

        if response.status_code in [200, 201, 202]:
            logger.info(f"Email sent successfully to {to_email}")
            return True
        else:
            logger.error(f"Failed to send email to {to_email}: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {str(e)}")
        return False


def send_verification_email(email: str, token: str) -> bool:
    """
    Send email verification link

    Args:
        email: User's email address
        token: Verification token

    Returns:
        True if email sent successfully
    """
    # Construct verification URL (adjust for your frontend URL)
    verification_url = f"{settings.FRONTEND_URL}/auth/verify-email?token={token}"

    subject = "Verify Your Email - Legally AI"
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #0ea5e9;">Legally AI</h1>
            </div>

            <h2 style="color: #333;">Verify Your Email Address</h2>

            <p style="color: #666; line-height: 1.6;">
                Thank you for signing up for Legally AI! Please verify your email address by clicking the button below:
            </p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}"
                   style="background-color: #0ea5e9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                    Verify Email
                </a>
            </div>

            <p style="color: #999; font-size: 12px; line-height: 1.6;">
                If the button doesn't work, copy and paste this link into your browser:<br>
                <a href="{verification_url}" style="color: #0ea5e9;">{verification_url}</a>
            </p>

            <p style="color: #999; font-size: 12px; margin-top: 30px;">
                This link will expire in 24 hours. If you didn't create an account with Legally AI, please ignore this email.
            </p>
        </body>
    </html>
    """

    text_content = f"""
    Verify Your Email Address

    Thank you for signing up for Legally AI!

    Please verify your email address by clicking this link:
    {verification_url}

    This link will expire in 24 hours.

    If you didn't create an account with Legally AI, please ignore this email.
    """

    return send_email(email, subject, html_content, text_content)


def send_password_reset_email(email: str, token: str) -> bool:
    """
    Send password reset link

    Args:
        email: User's email address
        token: Password reset token

    Returns:
        True if email sent successfully
    """
    # Construct reset URL (adjust for your frontend URL)
    reset_url = f"{settings.FRONTEND_URL}/auth/reset-password?token={token}"

    subject = "Reset Your Password - Legally AI"
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #0ea5e9;">Legally AI</h1>
            </div>

            <h2 style="color: #333;">Reset Your Password</h2>

            <p style="color: #666; line-height: 1.6;">
                We received a request to reset your password. Click the button below to create a new password:
            </p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}"
                   style="background-color: #0ea5e9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                    Reset Password
                </a>
            </div>

            <p style="color: #999; font-size: 12px; line-height: 1.6;">
                If the button doesn't work, copy and paste this link into your browser:<br>
                <a href="{reset_url}" style="color: #0ea5e9;">{reset_url}</a>
            </p>

            <p style="color: #999; font-size: 12px; margin-top: 30px;">
                This link will expire in 1 hour. If you didn't request a password reset, please ignore this email or contact support if you have concerns.
            </p>
        </body>
    </html>
    """

    text_content = f"""
    Reset Your Password

    We received a request to reset your password.

    Click this link to create a new password:
    {reset_url}

    This link will expire in 1 hour.

    If you didn't request a password reset, please ignore this email.
    """

    return send_email(email, subject, html_content, text_content)
