import re


def CHECK_CONTENT(email_content):
    # List of words and phrases to check for
    keywords = ["security", "password", "changed", "someone may have accessed",
                "password was just changed", "secure your account", "was just added"]

    # Create a regex pattern by joining the keywords with the '|' (OR) operator
    pattern = re.compile(
        r'\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b', re.IGNORECASE)

    # Use the regex pattern to find matches in the email content
    matches = pattern.findall(email_content)

    # If there are matches, return True; otherwise, return False
    return bool(matches)
    
def EVENT_TYPE_REST(event):
    """Returns bool of true if email event is incoming to lambda handler, if not...i.e webhook for call controls, will return false."""
    result = False
    for k, v in event.items():
        if k == "httpMethod":
            result = True
        elif type(k) == dict:
            EVENT_TYPE_REST(v)
    return result


if __name__ == "__main__":
    # Example usage:
    plaintext_email_content = "This is a sample email with the word 'password' in it."
    html_email_content = "<p>This is another email with the phrase 'secure your account'.</p>"

    # Test the plaintext email content
    result_plaintext = check_email_content(plaintext_email_content)
    print("Plaintext email content:", result_plaintext)

    # Test the HTML email content
    result_html = check_email_content(html_email_content)
    print("HTML email content:", result_html)
