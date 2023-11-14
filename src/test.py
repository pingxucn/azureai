import azure.cognitiveservices.speech as speechsdk
import os
speech_key, service_region = os.getenv("AZURE_SPEECH_KEY"), os.getenv('AZURE_SPEECH_REGION')
def convert_speech_to_text(audio_file):
    print("service_key="+speech_key)
    #speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    #speech_recognition_language="zh-cn"
    speech_recognition_language="english"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region,
                                       speech_recognition_language=speech_recognition_language)

    # Replace with the path to your audio file
    if os.path.exists(audio_file):
        # Creates an audio configuration that points to an audio file
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)

        # Creates a recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        print(speech_recognizer)

        print("Recognizing speech from file...")
        result = speech_recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
        # Prints the recognized text
        print(result.text)

        print("Recognizing finished")
    else:
        print("File doesn't exit:"+ audio_file)

audio_file_path = ".\\data\\speech\\time.wav" 
convert_speech_to_text(audio_file_path)

