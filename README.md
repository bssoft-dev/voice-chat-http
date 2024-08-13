# Voice Chat

## Requirement
python >= 3.9  
Sound card (hareware) for client  

### tested
Server: RaspberryPi 4
Client: RaspberryPi zero WiFi, of course it works better on the other devices, PCs. 

## How To Test
1. Start Server
Open terminal window and execute.
'''bash
python app.py
'''
2. Create Room  
- Open Web Browser, than connect [http://localhost:24015/docs](http://localhost:24015/docs)
- Unfold /create_room API and Click `Try it out` button on the right top
- Replace "string" to "test_room" in the Request body
- Click `Execute` button, it will show you "message": "Room 'test_room' created successfully"
3. Start Client
Open another terminal window and execute.
```bash
cd client
python client.py 
```
