import asyncio
import websockets
import pyaudio
import time
import numpy as np
from collections import deque
from concurrent.futures import ThreadPoolExecutor

# 오디오 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
BUFFER_SIZE = 10

class AudioClient:
    def __init__(self, ws_base_url, room_name):
        self.ws_base_url = ws_base_url
        self.room_name = room_name
        self.p = pyaudio.PyAudio()
        self.input_stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=self.record_callback)
        self.output_stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
        self.websocket = None
        self.is_running = True
        self.input_buffer = deque(maxlen=BUFFER_SIZE)
        self.output_buffer = deque(maxlen=BUFFER_SIZE)
        self.executor = ThreadPoolExecutor(max_workers=2) 

    def record_callback(self, in_data, frame_count, time_info, status):
        self.input_buffer.append(in_data)
        return (None, pyaudio.paContinue)

    async def connect(self):
        uri = f"{self.ws_base_url}/{self.room_name}"
        self.websocket = await websockets.connect(uri)

    async def send_audio(self):
        try:
            while True:
                if self.input_buffer:
                    data = self.input_buffer.popleft()
                    await self.websocket.send(data)
                else:
                    await asyncio.sleep(0.001)
        except Exception as e:
            print(f"Error in send_audio: {e}")

    async def receive_audio(self):
        try:
            while True:
                data = await self.websocket.recv()
                self.output_buffer.append(data)
        except Exception as e:
            print(f"Error in receive_audio: {e}")

    def play_audio(self):
        while self.is_running:
            if self.output_buffer and self.output_stream and self.output_stream.is_active():
                audio_data = self.output_buffer.popleft()
                self.output_stream.write(audio_data)
            else:
                time.sleep(0.001)  # 큐가 비어있을 때 짧게 대기

    async def run(self):
        self.input_stream.start_stream()
        self.output_stream.start_stream()
        loop = asyncio.get_event_loop()
        playing_task = loop.run_in_executor(self.executor, self.play_audio)
        await self.connect()
        await asyncio.gather(
            self.send_audio(),
            self.receive_audio(),
            playing_task
        )

    def close(self):
        self.is_running = False
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
        if self.p:
            self.p.terminate()

async def main():
    ws_base_url = "ws://localhost:24015/ws"
    room_name = "test_room"  # 원하는 방 이름으로 변경하세요
    client = AudioClient(ws_base_url, room_name)
    
    try:
        await client.run()
    except KeyboardInterrupt:
        print("클라이언트를 종료합니다.")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())

