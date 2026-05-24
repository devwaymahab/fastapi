# WebSocketExample

A simple FastAPI WebSocket chat example.

## What this project does

- Starts a FastAPI server with a WebSocket endpoint.
- Lets a user connect from a web page and send messages.
- The server broadcasts each message to all connected users.

## Files

- `main.py` — FastAPI server with WebSocket logic.
- `ind.html` — Basic browser chat interface.

## How to run

1. Open a terminal and go to this folder:

   ```bash
   cd /Users/mahabbasha/CODE/FASTAPI_SERIES/GITHUB/WebSocketExample
   ```

2. Install FastAPI and uvicorn if you do not have them already:

   ```bash
   pip install fastapi uvicorn
   ```

3. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

4. Open `ind.html` in your browser.

5. Enter a username and click **Connect**.

6. Type a message and click **Send**.

## Notes

- The browser connects to `ws://localhost:8000/ws/<username>`.
- Open the page in more than one browser tab to test chat between users.
- If the page does not connect, make sure the server is running on port `8000`.
