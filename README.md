# Translator
Multilanguage Translator using AI:
        
The project is a Language Translator application built using Python and several libraries such as Tkinter for the GUI, Googletrans for translation, SpeechRecognition for speech-to-text, gTTS for text-to-speech, OpenCV for camera integration, pytesseract for optical character recognition (OCR), and geopy for geocoding.

Here's a breakdown of the features and functionalities of the Translator application:

1. **User Interface (UI)**:
   - The UI is developed using Tkinter, providing a user-friendly interface for interacting with the application.
   - It consists of input fields, dropdown menus, buttons, and output text areas for various functionalities.

2. **Translation**:
   - Users can enter text in one language and select both the source language and the target language from dropdown menus.
   - Upon clicking the "Translate" button, the application translates the input text from the source language to the target language using Googletrans.
   - The translated text is displayed in a text area, and users can also choose to speak the translated text using the "Speak Translated" button.

3. **Speech Recognition**:
   - Users can click the "Speak" button to start speaking, and the application converts the spoken words into text using SpeechRecognition.
   - The recognized text is then displayed in the input field for translation.

4. **Text-to-Speech**:
   - Users can click the "Speak" button to listen to the text entered in the input field using gTTS.
   - Additionally, users can choose to listen to the translated text by clicking the "Speak Translated" button.

5. **Camera Integration**:
   - Users can click the "Camera" button to access the live video feed from their webcam using OpenCV.
   - The application performs optical character recognition (OCR) on the video feed to extract text, which is then automatically translated and displayed in the input field.

6. **Geocoding**:
   - Users can enter latitude and longitude coordinates in the input fields to retrieve the corresponding location information.
   - The application uses geopy to perform reverse geocoding and displays the location address in a text area.

7. **Language Detection**:
   - The application automatically detects the most commonly spoken language based on the country code derived from the provided latitude and longitude coordinates.
   - The detected language is then set as the target language for translation.

8. **Other Features**:
   - Users can clear the input fields and output areas using the "Clear" button.
   - The application allows users to swap the source and target languages by clicking the "Reply" button.

Overall, the Translator application provides a comprehensive set of features for text translation, speech recognition, text-to-speech conversion, camera integration, geocoding, and language detection, making it a versatile tool for multilingual communication and interaction.
The latest installers can be downloaded here for the OCR:
                                                tesseract-ocr-w64-setup-5.3.4.20240503.exe (64 bit)
                                                tesseract-ocr-w64-setup-5.4.0.20240519-1-ga5ff320e.exe (64 bit)
                                                set the path of tesseract in Environment Variables 
