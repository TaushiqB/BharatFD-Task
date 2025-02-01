from google.cloud import translate

def translate_text(text="Hello, world!", target_language="fr"):
    client = translate.TranslationServiceClient()
    project_id = "faq-translation-bharatfd"  # Change this to your project ID
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en",
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")

# Run the function
translate_text("How are you?", "es")  # Spanish
translate_text("How are you?", "fr")  # French
translate_text("How are you?", "de")  # German
