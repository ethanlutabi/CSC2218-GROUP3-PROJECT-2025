from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
# Mock adapters - in production you'd integrate with real services
class EmailNotificationAdapter:
    def send(self, recipient: str, message: str) -> bool:
        print(f"Email to {recipient}: {message}")
        return True

class SMSNotificationAdapter:
    def send(self, recipient: str, message: str) -> bool:
        print(f"SMS to {recipient}: {message}")
        return True
class NotificationAdapter(ABC):
    """Interface for sending notifications through various channels."""
    
    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str, **kwargs) -> bool:
        """
        Send an email notification.
        
        Args:
            recipient: Email address of the recipient
            subject: Email subject line
            body: Email body content
            **kwargs: Additional parameters (like attachments, cc, etc.)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def send_sms(self, phone_number: str, message: str, **kwargs) -> bool:
        """
        Send an SMS notification.
        
        Args:
            phone_number: Recipient's phone number
            message: SMS message content
            **kwargs: Additional parameters (like sender ID, etc.)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def send_notification(self, channel: str, recipient: str, content: Dict[str, Any]) -> bool:
        """
        Generic method to send notification through specified channel.
        
        Args:
            channel: Notification channel ("email", "sms", etc.)
            recipient: Recipient address (email, phone number, etc.)
            content: Content of the notification with channel-specific fields
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        pass


class CompositeNotificationAdapter(NotificationAdapter):
    """
    Implementation of NotificationAdapter that composes multiple channel-specific adapters.
    This allows for easy integration of different notification providers.
    """
    
    def __init__(self, email_adapter: EmailNotificationAdapter, sms_adapter: SMSNotificationAdapter):
        self.email_adapter = email_adapter
        self.sms_adapter = sms_adapter
    
    def send_email(self, recipient: str, subject: str, body: str, **kwargs) -> bool:
        """Send an email using the configured email adapter."""
        message = f"Subject: {subject}\n\n{body}"
        return self.email_adapter.send(recipient, message)
    
    def send_sms(self, phone_number: str, message: str, **kwargs) -> bool:
        """Send an SMS using the configured SMS adapter."""
        return self.sms_adapter.send(phone_number, message)
    
    def send_notification(self, channel: str, recipient: str, content: Dict[str, Any]) -> bool:
        """
        Send notification through the specified channel.
        
        Args:
            channel: "email" or "sms"
            recipient: Email address or phone number
            content: For email: {"subject": "...", "body": "..."}
                     For SMS: {"message": "..."}
        """
        if channel.lower() == "email":
            return self.send_email(
                recipient=recipient,
                subject=content.get("subject", "Notification"),
                body=content.get("body", "")
            )
        elif channel.lower() == "sms":
            return self.send_sms(
                phone_number=recipient,
                message=content.get("message", "")
            )
        else:
            raise ValueError(f"Unsupported notification channel: {channel}")


# Example of creating the composite adapter with the mock adapters
def create_notification_service():
    """Factory function to create a notification service with configured adapters."""
    email_adapter = EmailNotificationAdapter()
    sms_adapter = SMSNotificationAdapter()
    return CompositeNotificationAdapter(email_adapter, sms_adapter)
