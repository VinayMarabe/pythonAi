import openai
import pyttsx3
import time 
import speech_recognition as sr

# set api key
openai.api_key="OpenAi API key"
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)  
    except:
        print('Skipping unknown error')

def generate_response(prompt):
  
    response = openai.Completion.create(
        engine ="text-davinci-002",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0        
    )
    return response["choices"][0]["text"]

def speak_text(text, is_print_only=False):
    if is_print_only:
        print(text)
    else:
        engine.say(text)
        engine.runAndWait()

def should_print_response(question):
    # check if question includes certain keywords
    keywords = ["program", "code", "write","webpage"]
    for keyword in keywords:
        if keyword in question.lower():
            return True
    return False

def ask_another_question_or_stop():
    while True:
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio, language='en-in')
                if transcription.lower() == "friday":
                    return True
                elif transcription.lower() == "stop":
                    return False            
            except:
                pass

def main():
    while True:
        speak_text("Say 'friday' to start recording your question..... ")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio, language='en-in')
                if transcription.lower() == "friday":
                    while True:
                        speak_text("Say your question....")
                        filename = "input.wav"
                        with sr.Microphone() as source:
                            print("Listening.......")
                            recognizer = sr.Recognizer()
                            source.pause_threshold = 1
                            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                            with open(filename, "wb") as f:
                                f.write(audio.get_wav_data())
        
                        text = transcribe_audio_to_text(filename)
                        if text:
                            print(f"You said: {text}")
                            response = generate_response(text)
                            print(f"Friday says: {response}")
                            if should_print_response(text):
                                speak_text(response, is_print_only=True)
                            else:
                                speak_text(response)
                            speak_text("Do you want to ask another question or stop?")
                            if not ask_another_question_or_stop():
                                speak_text("Good bye!!!")
                                return
                            
                        
            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
