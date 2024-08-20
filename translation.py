from vulavula import VulavulaClient
# import wave
# import pyaudio
# import os
# import re
# import qfrency

  
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

client = VulavulaClient("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU1MzhhMGIzYzNmMDQwMzVhMDNjODhkNmQ2MDlkNWJkIiwiY2xpZW50X2lkIjozNiwicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.C6St-QkEFO-xtrotnOiXt9AnyHauxTAhzuv-bhGWq5E")

def choose_voice_code(target_lang, user_gender, user_age):
    # Combine male and female voices into one list
    all_voices = male_voices + female_voices
    
    # Loop through all voices to find a match
    for voice in all_voices:
        if voice['language'] == target_lang and voice['gender'] == user_gender and voice['age'] == user_age:
            return voice['voice-code'], voice['sample-rate']
    
    # Return None if no match is found
    return None, None

# Example usage

    
      
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

# def get_next_synth_wav_filename():
#       # List all files in the current directory
#     files = os.listdir('.')
#     # Filter files that match the synth_wav pattern and extract numbers
#     synth_wav_files = [f for f in files if re.match(r'synthed_wav_(\d+)\.wav', f)]
#     max_number = 0
#     for file in synth_wav_files:
#         # Extract number from filename
#         number = int(re.search(r'(\d+)', file).group(0))
#         if number > max_number:
#             max_number = number
#     # Increment the highest number found by 1 for the new filename
#     new_filename = f"synthed_wav_{max_number + 1}.wav"
#     return new_filename

# def write_wav_to_file(wav, filename):
#     p = open(filename, "wb")
#     p.write(wav)
#     p.close()
    
# instansiate a cloud API instance

# # Lelapa Hackathon Account Key
# X_ACCOUNT_KEY = "0b5091da-7a2b-476c-9b6d-517baa078ee8" # share this with Hackathon participants

# # Lelapa Hackathon API Keys
# X_API_KEY = "263a08cc-4a1e-4f3c-aef9-69b1223fe668" # share this with Hackathon participants

# cloud_api = qfrency.QfrencyCloudTTS(X_ACCOUNT_KEY, X_API_KEY)
    
def translation(text):
  translation_data = {
    "input_text": f"{text}" , # this will come in from siya's mediapipe
    "source_lang": ("eng_Latn"),
    "target_lang": ("zul_Latn")
  }

  source_lang = convert_lang_code(translation_data['source_lang'])
  target_lang = convert_lang_code(translation_data['target_lang'])

  translation_result = client.translate(translation_data)
  spoken_text = translation_result['translation'][0]['translated_text']

  user_gender="male"
  user_age="adult"

  voice_code,sample_rate=choose_voice_code(target_lang,user_gender,user_age)
  print("Here is the voice code: ", voice_code)
  print("Here is the sample rate: ", sample_rate)


  print("Here is the spoken text: ", spoken_text)
  print(f"Your text, '{translation_data['input_text']}' translated from {source_lang} may be translated into {target_lang} as '{ spoken_text}' ")
# new_filename = get_next_synth_wav_filename()

# synthed_wav = cloud_api.synth("zul-ZA-hmm-lindiwe", #this line represents the voice to be used. this is the voice code. 
#                                 spoken_text, #this line represents the spoken text to be created
#                                 {"sample-rate" :16000}) #ensure this line matches the sample rate of the voice code.
# write_wav_to_file(synthed_wav, new_filename)

# Open the WAV file
# with wave.open(new_filename, 'rb') as wav_file:
#   # Create an instance of the PyAudio class
#   audio = pyaudio.PyAudio()

#   # Open a stream to play the WAV file
#   stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
#             channels=wav_file.getnchannels(),
#             rate=wav_file.getframerate(),
#             output=True)

#   # Read the data from the WAV file and play it
#   data = wav_file.readframes(1024)
#   while data:
#     stream.write(data)
#     data = wav_file.readframes(1024)

#   # Close the stream and terminate PyAudio
#   stream.stop_stream()
#   stream.close()
#   audio.terminate()
if __name__ == "__main__":
  translation("hello")


