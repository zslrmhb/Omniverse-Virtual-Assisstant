# Running the Demo

from asr import ASRService
from nlp import NLPService
from tts import TTSService
from audio2face import Audio2FaceService

asr_service = ASRService()
nlp_service = NLPService(max_wiki_articles=5)
tts_service = TTSService()
audio2face_service = Audio2FaceService()

while True:
    # speech recognition
    asr_service.run()
    print(asr_service.transcript)
    
    # natural language processing with the help of Wikipedia API
    nlp_service.wiki_query(asr_service.transcript)
    output = nlp_service.nlp_query()
    print(output)
    
    # text-to-speech
    audio_bytes = tts_service.get_audio_bytes(output)
    
    # Audio2Face Animation
    audio2face_service.make_avatar_speaks(audio_bytes)
