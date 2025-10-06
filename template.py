"""
Email templates for the email sender application.
"""

# Subject template with placeholders for personalization
SUBJECT_TEMPLATE = "Unlock Your Business Potential with AI & Automation"

# Email body template with placeholders for personalization
EMAIL_BODY = """\
Dear {name},

I hope this message finds you well. My name is Stephen Prahl, and I'm a Software & AI Engineer as well as owner at WickedUI out of Brick - NJ, with a passion for helping businesses like {company_name} harness the power of artificial intelligence and automation.

I'm reaching out because I'd like to offer my expertise to you completely free of charge. I believe that every business, regardless of size, can benefit from strategic AI implementation and process automation. My goal is to help you:

• Identify time-consuming tasks that can be automated
• Implement AI solutions to enhance productivity
• Develop custom tools that save money and boost efficiency
• Create data-driven strategies for growth

I'm not here to sell you anything—this is a genuine offer to help. I'm currently expanding my portfolio and would love the opportunity to demonstrate how these technologies can benefit your business.

Would you be open to a quick 15-minute call next week to discuss potential opportunities? I'm confident I can find at least one area where I can help you save time or increase revenue.

Looking forward to your thoughts.

Best regards,
Stephen Prahl
Software & AI Engineer
Wicked UI - https://wicked-ui.com
"""


def render_subject(context: dict) -> str:
    """Render the subject using the provided context.
    Keeps compatibility even if SUBJECT_TEMPLATE has no placeholders today.
    """
    try:
        return SUBJECT_TEMPLATE.format(**context)
    except Exception:
        # Fallback if context is missing keys or template has no placeholders
        return SUBJECT_TEMPLATE


def render_body(context: dict) -> str:
    """Render the email body using the provided context.
    Expected keys include: name, company_name
    """
    return EMAIL_BODY.format(**context)