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
       
        pass
    
    @abstractmethod
    def send_sms(self, phone_number: str, message: str, **kwargs) -> bool:
      
    
     @abstractmethod
     def send_notification(self, channel: str, recipient: str, content: Dict[str, Any]) -> bool:
        

      class CompositeNotificationAdapter(NotificationAdapter):
    
    
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


