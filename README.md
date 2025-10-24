# AZURE TRANSLATION SCRIPT for VSPC v9

## USAGE INSTRUCTIONS

### Prerequisites:
- Python
```bash
pip install azure-ai-translation-text
```
- Azure Cognitives Services subscription (Available in Azure)

### Configuration:
Edit these variables in the script:
```python
# Your Azure credentials (already set)
key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
endpoint = "https://XXXXXcognitive.cognitiveservices.azure.com/"
region = "francecentral"

# Source and target languages
source_language = "en"
target_language = ["fr"]  # Change to your target language

# File paths
input_file = "path/to/en.template.js"
output_file = "path/to/en.overwrite.js"
```

### Supported Language Codes:
- Norwegian Bokmål: "nb"
- French: "fr"
- German: "de"
- Spanish: "es"
- Italian: "it"
- Portuguese: "pt"
- Dutch: "nl"
- Swedish: "sv"
- Danish: "da"
- Finnish: "fi"
- etc.

- supported lang https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support

- sample code https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-text/samples/sample_text_translation_translate.py

### Run:
```bash
python vspc_azure_translation.py
```

---

## OUTPUT 
###  Script Output:
```javascript
/**
 * Copyright © Veeam Software Group GmbH.
 */

(window.VSPC = window.VSPC || {}).localesOverwrite = {};

window.VSPC.localesOverwrite.locale = {
ABOVE: 'Au-dessus',
ABOUT: 'À propos',
ACTION: 'Action',
...
};
```
**Benefits:**
- ✓ Complete valid JavaScript file
- ✓ Ready to use immediately
- ✓ Proper escaping
- ✓ Correct formatting

---

## INSTALLATION / SETUP
-  KB : https://www.veeam.com/kb4544

---

## ADDITIONAL FEATURES

### Progress Reporting:
```
Starting translation process...
Step 1: Extracting file structure...
   - Found 1250 translation entries
Step 2: Translating entries...
   - Progress: 100/1250 entries translated
   - Progress: 200/1250 entries translated
   ...
Step 3: Writing output file...
Translation process completed successfully!
```

### Error Handling:
- Validates file structure
- Handles missing translations gracefully
- Reports specific errors with context
- Continues on individual translation failures

### Batch Processing:
To translate to multiple languages at once:
```python
target_languages = ["nb", "sv", "da", "fi"]

for lang in target_languages:
    output_file = f"output_{lang}.js"
    target_language = [lang]
    # Run translation
```

---

## TESTING THE OUTPUT

After running the script, verify the output:

1. **Check file opens:** Open output.js in text editor
2. **Validate JavaScript:** Load in browser console or check syntax
3. **Verify structure:** Check header and footer are intact
4. **Spot check translations:** Review a few random entries
5. **Check special chars:** Look for entries with quotes, colons, etc.

---

## TROUBLESHOOTING

### "Could not find locale object in file"
- Check input file format matches expected structure
- Verify file encoding is UTF-8

### Translation API errors:
- Verify Azure credentials are correct
- Check internet connection
- Verify subscription is active

### Missing translations:
- Check Azure Translator supports target language
- Verify source text is not empty

### Encoding issues in output:
- Script uses UTF-8 encoding
- Ensure your editor supports UTF-8

---

## CONCLUSION

The improved script eliminates ALL manual steps:
- ✗ No pre-cleaning needed
- ✗ No post-processing with Notepad++
- ✗ No manual copy-paste
- ✗ No manual formatting
- ✓ Just run and use!

