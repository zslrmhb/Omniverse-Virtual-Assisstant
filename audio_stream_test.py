from riva.client.audio_io import MicrophoneStream
from typing import Callable, Dict, Generator, Iterable, List, Optional, TextIO, Union
import riva.client.proto.riva_asr_pb2 as rasr
import riva.client
from config import URI

config = riva.client.StreamingRecognitionConfig(
    config=riva.client.RecognitionConfig(
        encoding=riva.client.AudioEncoding.LINEAR_PCM,
        language_code='en-US',
        max_alternatives=1,
        profanity_filter=False,
        enable_automatic_punctuation=True,
        verbatim_transcripts=True,
        sample_rate_hertz=16000
    ),
    interim_results=True,
)

default_device_info = riva.client.audio_io.get_default_input_device_info()
default_device_index = None if default_device_info is None else default_device_info['index']
sample_rate_hz = 16000
file_streaming_chunk = 1600
input_device = 1
# streaming_config = riva.client.StreamingRecognitionConfig(config=deepcopy(offline_config), interim_results=True)\


auth = riva.client.Auth(uri=URI)
asr_service = riva.client.ASRService(auth)
# micstream = MicrophoneStream(rate=sample_rate_hz,
#     chunk=sample_rate_hz // 10, device=input_device)
count = 0


def run():
    with riva.client.audio_io.MicrophoneStream(
            rate=sample_rate_hz,
            chunk=file_streaming_chunk,
            device=input_device,
    ) as audio_chunk_iterator:
        # riva.client.print_streaming(
        #     responses=asr_service.streaming_response_generator(
        #         audio_chunks=audio_chunk_iterator,
        #         streaming_config=config,
        #     ),
        #     show_intermediate=False,
        # )
        # print("hello")
        # if count == 1: break
        print_response(responses=asr_service.streaming_response_generator(
                audio_chunks=audio_chunk_iterator,
                streaming_config=config,
            ))



def print_response(responses: Iterable[rasr.StreamingRecognizeResponse]):
    transcript = ""
    for response in responses:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue
            if result.is_final:
                partial_transcript = result.alternatives[0].transcript
                transcript += partial_transcript
                print(transcript)
                answer = input("Press a key")
                if answer == "q": return transcript





run()
