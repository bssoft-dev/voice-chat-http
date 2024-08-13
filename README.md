# Voice Chat

## Requirement
python >= 3.9  
Sound card (hareware) for client  

### Tested
Server: RaspberryPi 4  
Client: RaspberryPi zero WiFi, of course it works better on the other devices, PCs. 

## How To Test
1. Clone this repository
~~~bash
git clone https://github.com/bssoft-dev/voice-chat-ws
~~~
2. Install Dependencies
~~~bash
cd voice-chat-ws
pip install requirements.txt
cd client
pip install requirements.txt
cd ..
~~~
3. Start Server  
~~~bash
python app.py
~~~
4. Create Room  
- Open Web Browser, than connect [http://localhost:24015/docs](http://localhost:24015/docs)
- Unfold /create_room API and Click `Try it out` button on the right top
- Replace "string" to "test_room" in the Request body
- Click `Execute` button. It will show you "message": "Room 'test_room' created successfully".
5. Start Client  
Open another terminal window and execute.
~~~bash
cd client
python client.py 
~~~
