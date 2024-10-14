# TerminalQuest/utils/text_processor.py

import re

def process_text(text, variables=None):
    """
    Process text by replacing variables and applying basic formatting.
    
    Args:
    text (str): The text to process.
    variables (dict): A dictionary of variables to replace in the text.
    
    Returns:
    str: The processed text.
    """
    if variables:
        for key, value in variables.items():
            text = text.replace(f"{{{key}}}", str(value))
    
    # Apply basic formatting
    text = apply_formatting(text)
    
    return text

def apply_formatting(text):
    """
    Apply basic formatting to the text.
    
    Args:
    text (str): The text to format.
    
    Returns:
    str: The formatted text.
    """
    # Convert **bold** to ANSI bold
    text = re.sub(r'\*\*(.*?)\*\*', '\033[1m\\1\033[0m', text)
    
    # Convert *italic* to ANSI italic (not widely supported)
    text = re.sub(r'\*(.*?)\*', '\033[3m\\1\033[0m', text)
    
    # Convert _underline_ to ANSI underline
    text = re.sub(r'_(.*?)_', '\033[4m\\1\033[0m', text)
    
    return text

def word_wrap(text, width=80):
    """
    Wrap text to a specified width.
    
    Args:
    text (str): The text to wrap.
    width (int): The maximum line width.
    
    Returns:
    str: The wrapped text.
    """
    return '\n'.join(text[i:i+width] for i in range(0, len(text), width))

# Example usage:
# processed_text = process_text("Hello, {name}! This is **bold** and *italic*.", {"name": "Alice"})
# wrapped_text = word_wrap(processed_text, width=40)
# print(wrapped_text)