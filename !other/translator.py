from deep_translator import GoogleTranslator

text = "Welcome to our tutorial!"

# Використання Google Translate
google_translation = GoogleTranslator(target='en').translate(text)
print(f"Google Translate: {google_translation}")

