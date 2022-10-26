from __future__ import print_function

import grpc
import ASR_pb2_grpc as ASR_pb2_grpc
import ASR_pb2 as pb2
import sys


def make_SpeechRecognitionRequest(voice):
    return pb2.SpeechRecognitionRequest(
        speechVoice=voice
    )


def generate_voices():
    with open('kaitomm.mp3', 'rb') as fd:
        content = fd.read()

        requests = [
            make_SpeechRecognitionRequest(content),
            make_SpeechRecognitionRequest(content),
            make_SpeechRecognitionRequest(content)
        ]
        for request in requests:
            print("Hello Server Sending voiceStreaming to you with size %d" % len(request.speechVoice))
            yield request


def test(stub, message):
    """
    Client function to call the rpc for GetServerResponse
    """
    message = pb2.SpeechRecognitionMessage(message=message)
    print(f'Sending Message: {message}', file=sys.stderr)
    return stub.test(message)
    
def asr_voice_streaming(stub):
    responses = stub.recognize(generate_voices())
    print(responses, file=sys.stderr)
    for response in responses:
        print(type(response))
        print("Hello from the server received your %s" % response, file=sys.stderr)


def run():
    # Please contact ai@iapp.co.th for gRPC HOST address.
    with grpc.insecure_channel('{gRPC HOST}') as channel:
        stub = ASR_pb2_grpc.ASRStub(channel)
        resp = test(stub, "Hello World!")
        print(resp.message)
        asr_voice_streaming(stub)

if __name__ == '__main__':
    run()