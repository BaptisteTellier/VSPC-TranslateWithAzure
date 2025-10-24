
"""
Azure Translation Script for Veeam Service Provider JavaScript Localization Files
Handles the full file structure including header, footer, and proper JavaScript formatting
Install KB : https://www.veeam.com/kb4544
"""

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
import re
import os

# Azure Cognitive Services Configuration
key = "XXXXXXXXXXXXXXXX"
endpoint = "https://XXXXcognitive.cognitiveservices.azure.com/"
region = "francecentral"

# Translation Settings
source_language = "en"
target_language = ["fr"]  # French

# File Paths
input_file = "C:/.../vspc v9/en.template.js"
output_file = "C:/.../vspc v9/fr.template.js"

# Initialize Azure Translator
credential = TranslatorCredential(key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

def extract_js_structure(file_path):
    """
    Extract header, footer, and translation entries from JavaScript file
    Returns: (header, entries_dict, footer)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find the start of the locale object
    locale_start = content.find('window.VSPC.localesOverwrite.locale = {')

    if locale_start == -1:
        raise ValueError("Could not find locale object in file")

    # Extract header (everything before locale object content)
    header = content[:locale_start + len('window.VSPC.localesOverwrite.locale = {\n')]

    # Find the closing brace
    locale_end = content.rfind('};')
    if locale_end == -1:
        raise ValueError("Could not find closing brace of locale object")

    # Extract footer
    footer = content[locale_end:]

    # Extract the content between braces
    locale_content = content[locale_start + len('window.VSPC.localesOverwrite.locale = {'):locale_end]

    # Parse entries using regex
    # Pattern matches: KEY: 'value', or KEY: "value",
    pattern = r"([A-Z_][A-Z0-9_]*):\s*'([^'\\]*(?:\\.[^'\\]*)*)',?"

    entries = {}
    for match in re.finditer(pattern, locale_content):
        key = match.group(1)
        value = match.group(2)
        # Unescape the value
        value = value.replace("\\'", "'").replace("\\\\", "\\")
        entries[key] = value

    return header, entries, footer

def translate_text(text, text_translator, source_lang, target_langs):
    """
    Translate a single text using Azure Translator
    Returns translated text
    """
    if not text or text.strip() == '':
        return text

    try:
        input_text = [InputTextItem(text=text)]
        response = text_translator.translate(
            content=input_text,
            to=target_langs,
            from_parameter=source_lang
        )

        if response and len(response) > 0:
            translation = response[0]
            if translation.translations and len(translation.translations) > 0:
                return translation.translations[0].text

        return text  # Return original if translation fails
    except Exception as e:
        print(f"Error translating '{text[:50]}...': {e}")
        return text

def clean_translated_text(text):
    """
    Clean problematic characters from translated text
    """
    # Remove or replace problematic quotes
    text = text.replace('\u00ab', '').replace('\u00bb', '')
    text = text.replace(""", '"').replace(""", '"')
    text = text.replace("'", "'").replace("'", "'")

    return text

def escape_js_string(text):
    """
    Properly escape string for JavaScript
    """
    # Escape backslashes first
    text = text.replace("\\", "\\\\")
    # Escape single quotes
    text = text.replace("'", "\\'")
    return text

def write_js_file(output_path, header, translated_entries, footer):
    """
    Write the translated entries back to JavaScript file with proper formatting
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        # Write header
        file.write(header)

        # Write translated entries
        entries_list = list(translated_entries.items())
        for i, (key, value) in enumerate(entries_list):
            # Escape the value for JavaScript
            escaped_value = escape_js_string(value)

            # Determine if we need a comma (not on last entry)
            comma = ',' if i < len(entries_list) - 1 else ''

            # Write the entry
            file.write(f"{key}: '{escaped_value}'{comma}\n")

        # Write footer
        file.write(footer)

def main():
    """
    Main translation workflow
    """
    print("Starting translation process...")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Source language: {source_language}")
    print(f"Target language: {target_language[0]}\n")

    # Step 1: Extract structure from input file
    print("Step 1: Extracting file structure...")
    try:
        header, entries, footer = extract_js_structure(input_file)
        print(f"   - Found {len(entries)} translation entries")
        print(f"   - Header length: {len(header)} characters")
        print(f"   - Footer length: {len(footer)} characters\n")
    except Exception as e:
        print(f"ERROR: Failed to extract file structure: {e}")
        return

    # Step 2: Translate entries
    print("Step 2: Translating entries...")
    translated_entries = {}
    total = len(entries)

    for idx, (key, value) in enumerate(entries.items(), 1):
        if idx % 100 == 0:
            print(f"   - Progress: {idx}/{total} entries translated")

        # Translate the value
        translated_value = translate_text(value, text_translator, source_language, target_language)

        # Clean the translated text
        cleaned_value = clean_translated_text(translated_value)

        # Store in dictionary
        translated_entries[key] = cleaned_value

    print(f"   - Completed: {total}/{total} entries translated\n")

    # Step 3: Write output file
    print("Step 3: Writing output file...")
    try:
        write_js_file(output_file, header, translated_entries, footer)
        print(f"   - File written successfully to: {output_file}\n")
    except Exception as e:
        print(f"ERROR: Failed to write output file: {e}")
        return

    print("Translation process completed successfully!")
    print(f"\nOutput file is ready at: {output_file}")

if __name__ == "__main__":
    main()