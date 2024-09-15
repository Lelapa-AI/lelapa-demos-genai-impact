from vulavula import VulavulaClient
import pyttsx3
import tkinter as tk
from tkinter import messagebox

male_voices = [{'voice-code': 'afr-ZA-hmm-bennie', 'name': 'Bennie', 'description': 'Afrikaans male child voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'afrikaans', 'lang-code': 'afr', 'country-code': 'ZA', 'gender': 'male', 'age': 'child', 'sample-rate': 16000}, 
               {'voice-code': 'afr-ZA-dnn-kobus', 'name': 'Kobus', 'description': 'Afrikaans male voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'afrikaans', 'lang-code': 'afr', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 22050}, 
               {'voice-code': 'afr-ZA-hmm-kobus', 'name': 'Kobus', 'description': 'Afrikaans male voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'afrikaans', 'lang-code': 'afr', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 16000}, 
               {'voice-code': 'eng-ZA-dnn-tim', 'name': 'Tim', 'description': 'South African English male voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'englishza', 'lang-code': 'eng', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 22050},
               {'voice-code': 'eng-ZA-hmm-tim', 'name': 'Tim', 'description': 'South African English male voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'englishza', 'lang-code': 'eng', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 16000}, 
                {'voice-code': 'nbl-ZA-dnn-banele', 'name': 'Banele', 'description': 'isiNdebele male voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'isindebele', 'lang-code': 'nbl', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 22050},
               {'voice-code': 'nbl-ZA-hmm-banele', 'name': 'Banele', 'description': 'isiNdebele male voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'isindebele', 'lang-code': 'nbl', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 16000},
               {'voice-code': 'nso-ZA-dnn-tshepo', 'name': 'Tshepo', 'description': 'Sepedi male voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'sepedi', 'lang-code': 'nso', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 22050},
               {'voice-code': 'nso-ZA-hmm-tshepo', 'name': 'Tshepo', 'description': 'Sepedi male voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'sepedi', 'lang-code': 'nso', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 16000},
               {'voice-code': 'ven-ZA-dnn-rabelani', 'name': 'Rabelani', 'description': 'Tshivenda male voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'tshivenda', 'lang-code': 'ven', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 22050},
               {'voice-code': 'ven-ZA-hmm-rabelani', 'name': 'Rabelani', 'description': 'Tshivenda male voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'tshivenda', 'lang-code': 'ven', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 16000}, 
               {'voice-code': 'xho-ZA-dnn-vuyo', 'name': 'Vuyo', 'description': 'isiXhosa male voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'isixhosa', 'lang-code': 'xho', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 22050},
               {'voice-code': 'xho-ZA-hmm-vuyo', 'name': 'Vuyo', 'description': 'isiXhosa male voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'isixhosa', 'lang-code': 'xho', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 16000},
               {'voice-code': 'zul-ZA-dnn-sifiso', 'name': 'Sifiso', 'description': 'isiZulu male voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'isizulu', 'lang-code': 'zul', 'country-code': 'ZA', 'gender': 'male', 'age': 'adult', 'sample-rate': 22050}]

female_voices = [{'voice-code': 'afr-ZA-dnn-maryna', 'name': 'Maryna', 'description': 'Afrikaans female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'afrikaans', 'lang-code': 'afr', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050}, 
                 {'voice-code': 'afr-ZA-hmm-maryna', 'name': 'Maryna', 'description': 'Afrikaans female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'afrikaans', 'lang-code': 'afr', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000},
                 {'voice-code': 'eng-ZA-dnn-candice', 'name': 'Candice', 'description': 'South African English female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'englishza', 'lang-code': 'eng', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050}, 
                 {'voice-code': 'eng-ZA-hmm-candice', 'name': 'Candice', 'description': 'South African English female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'englishza', 'lang-code': 'eng', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000},
                 {'voice-code': 'nso-ZA-dnn-mmapitsi', 'name': 'Mmapitsi', 'description': 'Sepedi female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'sepedi', 'lang-code': 'nso', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050}, 
                 {'voice-code': 'nso-ZA-hmm-mmapitsi', 'name': 'Mmapitsi', 'description': 'Sepedi female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'sepedi', 'lang-code': 'nso', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000},
                 {'voice-code': 'sot-ZA-dnn-kamohelo', 'name': 'Kamohelo', 'description': 'Sesotho female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'sesotho', 'lang-code': 'sot', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050},
                 {'voice-code': 'sot-ZA-hmm-kamohelo', 'name': 'Kamohelo', 'description': 'Sesotho female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'sesotho', 'lang-code': 'sot', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000},
                 {'voice-code': 'ssw-ZA-dnn-temaswati', 'name': 'Temaswati', 'description': 'siSwati female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'siswati', 'lang-code': 'ssw', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050},
                 {'voice-code': 'ssw-ZA-hmm-temaswati', 'name': 'Temaswati', 'description': 'siSwati female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'siswati', 'lang-code': 'ssw', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000}, 
                 {'voice-code': 'tsn-ZA-dnn-lethabo', 'name': 'Lethabo', 'description': 'Setswana female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'setswana', 'lang-code': 'tsn', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050},
                 {'voice-code': 'tsn-ZA-hmm-lethabo', 'name': 'Lethabo', 'description': 'Setswana female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'setswana', 'lang-code': 'tsn', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000}, 
                 {'voice-code': 'tso-ZA-dnn-sasekani', 'name': 'Sasekani', 'description': 'Xitsonga female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'xitsonga', 'lang-code': 'tso', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050},
                 {'voice-code': 'tso-ZA-hmm-sasekani', 'name': 'Sasekani', 'description': 'Xitsonga female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'xitsonga', 'lang-code': 'tso', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000}, 
                 {'voice-code': 'xho-ZA-dnn-zoleka', 'name': 'Zoleka', 'description': 'isiXhosa female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'isixhosa', 'lang-code': 'xho', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050}, 
                 {'voice-code': 'xho-ZA-hmm-zoleka', 'name': 'Zoleka', 'description': 'isiXhosa female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'isixhosa', 'lang-code': 'xho', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000},
                 {'voice-code': 'zul-ZA-dnn-lindiwe', 'name': 'Lindiwe', 'description': 'isiZulu female voice with neural acoustic and vocoder models', 'technique': 'DNN', 'language': 'isizulu', 'lang-code': 'zul', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 22050},
                 {'voice-code': 'zul-ZA-hmm-lindiwe', 'name': 'Lindiwe', 'description': 'isiZulu female voice with HMM acoustic models and mixed-excitation vocoder', 'technique': 'HMM', 'language': 'isizulu', 'lang-code': 'zul', 'country-code': 'ZA', 'gender': 'female', 'age': 'adult', 'sample-rate': 16000}]

client = VulavulaClient("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImI5OWMxOWQ5NmJjYzQzNzU4MjQ5ZDhkOTk5ZTE1N2MxIiwiY2xpZW50X2lkIjoyNzcsInJlcXVlc3RzX3Blcl9taW51dGUiOjAsImxhc3RfcmVxdWVzdF90aW1lIjpudWxsfQ.wWkLvpTD0nM1WW2BrZ8_S3dx8E2uLxd_JRO-VETFYxA")

def choose_voice_code(target_lang, user_gender, user_age):
    # Combine male and female voices into one list
    all_voices = male_voices + female_voices
    
    # Loop through all voices to find a match
    for voice in all_voices:
        if voice['language'] == target_lang and voice['gender'] == user_gender and voice['age'] == user_age:
            return voice['voice-code'], voice['sample-rate']
    

    
      
def convert_lang_code(lang_code):
  lang_mapping = {
    "nso_Latn": "sepedi",
    "afr_Latn": "afrikaans",
    "sot_Latn": "sesotho",
    "ssw_Latn": "siswati",
    "tso_Latn": "xitsonga",
    "tsn_Latn": "setswana",
    "xho_Latn": "isixhosa",
    "zul_Latn": "isizulu",
    "eng_Latn": "english",
    "swh_Latn": "swahili"
  }
  return lang_mapping.get(lang_code, lang_code)


def text_to_speech(text):
    # Placeholder function for text-to-speech conversion
    print("Translating....")
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

    engine.say(text)
    engine.runAndWait()
    engine.stop()



def translation(text):
  translation_data = {
      "input_text": f"{text}" , # this will come in from siya's mediapipe
      "source_lang": ("eng_Latn"),
      "target_lang": ("zul_Latn")
    }

    # Placeholder variables for demonstration
  source_lang = convert_lang_code(translation_data['source_lang'])
  target_lang = convert_lang_code(translation_data['target_lang'])

  translation_result = client.translate(translation_data)
  spoken_text = translation_result['translation'][0]['translated_text']
  
 

  # Create the main window
  root = tk.Tk()
  root.title("Text to speech translation")
  root.geometry("500x300")

  # Create and place the widgets for text translation
  text_frame = tk.Frame(root)
  text_frame.pack(pady=10)
  tk.Label(text_frame, text="Text Translation Option:").pack(anchor=tk.W)
  tk.Radiobutton(text_frame, text="Text", variable=tk.StringVar(value="text"), value="text").pack(anchor=tk.W)
  tk.Button(text_frame, text="Translate", command=lambda: display_translation(translation_data, source_lang, target_lang, spoken_text)).pack(pady=10)

  # Create and place the widgets for speech translation
  speech_frame = tk.Frame(root)
  speech_frame.pack(pady=10)
  tk.Label(speech_frame, text="Speech Translation Option:").pack(anchor=tk.W)
  tk.Radiobutton(speech_frame, text="Speech", variable=tk.StringVar(value="speech"),command=lambda: text_to_speech(spoken_text)).pack(anchor=tk.W)
  tk.Button(speech_frame, text="Speak",command=lambda: text_to_speech(spoken_text)).pack(pady=10)

  # Create a text widget to display the translation
  output_text = tk.Text(root, height=10, width=50)
  output_text.pack(pady=10)

  def display_translation(translation_data, source_lang, target_lang, spoken_text):
      message = f"Your text, '{translation_data['input_text']}' translated from {source_lang} may be translated into {target_lang} as '{spoken_text}'"
      output_text.delete(1.0, tk.END)
      output_text.insert(tk.END, message)

  # Run the main loop
  root.mainloop()

if __name__ == "__main__":
    translation(text="hello")