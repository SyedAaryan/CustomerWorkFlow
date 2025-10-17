import re


def extract_email_address(from_field: str) -> str:
    """
    Extracts a plain email address from a 'From' field.
    e.g. 'John Doe <john@example.com>' -> 'john@example.com'
    """
    match = re.search(r'<(.+?)>', from_field)
    return match.group(1) if match else from_field
