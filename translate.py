import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import os
import cv2
import pytesseract
from tkinter import messagebox
import geopy.geocoders
from collections import Counter
import threading
import time

class TranslatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Language Translator")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        self.translator = Translator()
        self.geolocator = geopy.geocoders.Nominatim(user_agent="translator_app")

        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill='both')

        self.label1 = ttk.Label(self.frame, text="Enter text:")
        self.label1.pack(side="top", anchor="center", padx=10, pady=5)

        self.entry = ttk.Entry(self.frame, width=30)
        self.entry.pack(side="top", anchor="center", padx=10, pady=5)

        self.label2 = ttk.Label(self.frame, text="From language:")
        self.label2.pack(side="top", anchor="center", padx=10, pady=5)

        self.from_language = tk.StringVar(master)
        self.from_language.set("English")
        self.from_language_dropdown = ttk.Combobox(self.frame, textvariable=self.from_language, values=["Tamil", "English", "French", "German", "Spanish", "Kannada", "Hindi"])
        self.from_language_dropdown.pack(side="top", anchor="center", padx=10, pady=5)

        self.label3 = ttk.Label(self.frame, text="To language:")
        self.label3.pack(side="top", anchor="center", padx=10, pady=5)

        self.to_language = tk.StringVar(master)
        self.to_language.set("English")
        self.to_language_dropdown = ttk.Combobox(self.frame, textvariable=self.to_language, values=["English", "French", "German", "Spanish", "Tamil", "Kannada", "Hindi"])
        self.to_language_dropdown.pack(side="top", anchor="center", padx=10, pady=5)

        self.most_used_language_label = ttk.Label(self.frame, text="Most Used Language:")
        self.most_used_language_label.pack(side="top", anchor="center", padx=10, pady=5)

        self.most_used_language_output = tk.Text(self.frame, height=1, width=30)
        self.most_used_language_output.pack(side="top", anchor="center", padx=10, pady=5)

        self.translate_button = ttk.Button(self.frame, text="Translate", command=self.translate_text)
        self.translate_button.pack(side="top", anchor="center", padx=10, pady=5)

        self.speak_translated_button = ttk.Button(self.frame, text="Speak Translated", command=self.speak_user_text)
        self.speak_translated_button.pack(side="top", anchor="center", padx=10, pady=5)

        self.label4 = ttk.Label(self.frame, text="Translation:")
        self.label4.pack(side="top", anchor="center", padx=10, pady=5)

        self.translation_output = tk.Text(self.frame, height=5, width=30)
        self.translation_output.pack(side="top", anchor="center", padx=10, pady=5)

        self.speech_button = ttk.Button(self.frame, text="Speak", command=self.speech_to_text)
        self.speech_button.pack(side="top", anchor="center", padx=10, pady=5)

        self.camera_button = ttk.Button(self.frame, text="Camera", command=self.start_video_feed)
        self.camera_button.pack(side="top", anchor="center", padx=10, pady=5)

        self.location_label = ttk.Label(self.frame, text="Location:")
        self.location_label.pack(side="top", anchor="center", padx=20, pady=5)

        self.location_output = tk.Text(self.frame, height=1, width=30)
        self.location_output.pack(side="top", anchor="center", padx=10, pady=5)

        self.latitude_label = ttk.Label(self.frame, text="Latitude:")
        self.latitude_label.pack(side="top", anchor="center", padx=10, pady=5)

        self.latitude_entry = ttk.Entry(self.frame, width=30)
        self.latitude_entry.pack(side="top", anchor="center", padx=10, pady=5)

        self.longitude_label = ttk.Label(self.frame, text="Longitude:")
        self.longitude_label.pack(side="top", anchor="center", padx=10, pady=5)

        self.longitude_entry = ttk.Entry(self.frame, width=30)
        self.longitude_entry.pack(side="top", anchor="center", padx=10, pady=5)

        self.get_location_button = ttk.Button(self.frame, text="Get Location", command=self.get_location)
        self.get_location_button.pack(side="top", anchor="center", padx=10, pady=5)

        self.clear_button = ttk.Button(self.frame, text="Clear", command=self.clear_data)
        self.clear_button.pack(side="top", anchor="center", padx=10, pady=5)

        self.reply_button = ttk.Button(self.frame, text="Reply", command=self.swap_languages)
        self.reply_button.pack(side="top", anchor="center", padx=10, pady=5)

        # Center-align all widgets vertically and horizontally
        for widget in self.frame.winfo_children():
            widget.pack_configure(side="top", anchor="center")

    def translate_text(self):
        input_text = self.entry.get()
        from_lang = self.from_language.get()
        to_lang = self.to_language.get()

        from_lang_code = self.get_language_code(from_lang)
        to_lang_code = self.get_language_code(to_lang)

        try:
            translated_text = self.translator.translate(input_text, src=from_lang_code, dest=to_lang_code).text
            self.translation_output.delete(1.0, tk.END)
            self.translation_output.insert(tk.END, translated_text)
            self.speak_translated_text()  # Speak the translated text after translation
        except AttributeError as e:
            print("Failed to translate:", e)
            self.translation_output.delete(1.0, tk.END)
            self.translation_output.insert(tk.END, "Translation failed. Please try again later.")
        except Exception as e:
            print("An error occurred:", e)
            self.translation_output.delete(1.0, tk.END)
            self.translation_output.insert(tk.END, "An error occurred. Please try again later.")

    def get_language_code(self, language):
        language_codes = {"English": "en", "Tamil": "ta", "Kannada": "kn", "Hindi": "hi"}
        return language_codes.get(language, "en")  # Default to English if language not found

    def speech_to_text(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Say something")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

            if audio:
                text = r.recognize_google(audio)
                self.entry.delete(0, tk.END)
                self.entry.insert(0, text)
            else:
                print("No audio input received")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error fetching results:", e)
        except Exception as e:
            print("An error occurred:", e)

    def text_to_speech(self, text, language='en'):
        if text:
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save("output.mp3")
            os.system("start output.mp3")

    def start_video_feed(self):
        cap = cv2.VideoCapture(0)

        def process_frame():
            while True:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Error", "Failed to capture frame from camera.")
                    break

                # Only process a frame every second
                time.sleep(1)
                text = self.ocr_and_translate(frame)
                if text:
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, text)
                    self.translate_text()

                cv2.imshow('Live Video Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        threading.Thread(target=process_frame).start()

    def ocr_and_translate(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Apply thresholding to preprocess the image
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            text = pytesseract.image_to_string(binary)
            return text if text else None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_location(self):
        try:
            latitude = float(self.latitude_entry.get())
            longitude = float(self.longitude_entry.get())

            location = self.geolocator.reverse((latitude, longitude), language='en')
            if location:
                address = location.address
                self.location_output.delete(1.0, tk.END)
                self.location_output.insert(tk.END, address)

                country_code = location.raw['address']['country_code'].upper()
                language_code = self.get_most_common_language(country_code)
                if language_code:
                    self.to_language.set(language_code)
                    self.most_used_language_output.delete(1.0, tk.END)
                    self.most_used_language_output.insert(tk.END, language_code)
            else:
                self.location_output.delete(1.0, tk.END)
                self.location_output.insert(tk.END, "Location not found")
        except ValueError:
            messagebox.showerror("Error", "Latitude and Longitude must be valid numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_most_common_language(self, country_code):
        country_to_language = {
            'US': 'English',
            'IN': 'Hindi',
            'FR': 'French',
            'DE': 'German',
            'ES': 'Spanish',
            'BR': 'Portuguese',
            'CN': 'Chinese',
            'JP': 'Japanese',
        }

        language_counter = Counter(country_to_language.values())
        most_common_language = language_counter.most_common(1)

        return country_to_language.get(country_code, most_common_language[0][0])

    def clear_data(self):
        self.entry.delete(0, tk.END)
        self.translation_output.delete(1.0, tk.END)
        self.location_output.delete(1.0, tk.END)
        self.latitude_entry.delete(0, tk.END)
        self.longitude_entry.delete(0, tk.END)
        self.most_used_language_output.delete(1.0, tk.END)

    def swap_languages(self):
        from_language = self.from_language.get()
        to_language = self.to_language.get()

        self.from_language.set(to_language)
        self.to_language.set(from_language)

        if self.entry.get():
            self.translate_text()

    def speak_user_text(self):
        entered_text = self.entry.get()
        from_lang = self.from_language.get()
        from_lang_code = self.get_language_code(from_lang)
        if entered_text:
            self.text_to_speech(entered_text, from_lang_code)

    def speak_translated_text(self):
        translated_text = self.translation_output.get(1.0, tk.END).strip()
        to_lang = self.to_language.get()
        language_code = self.get_language_code(to_lang)

        if translated_text:
            self.text_to_speech(translated_text, language_code)

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
