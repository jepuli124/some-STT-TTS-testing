import json
import piperhandler
import ollama
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


MODEL = "qwen3.6:35b"

CLEAN_SYSTEM = (
    "You are connected to STT pipeline. Your job is to fix user's message to "
    "understandable form. Clean it by fixing spelling, capitalization, and "
    "punctuation errors. The text is in english. There might be missing words "
    "try to fill in or unnecessary words then remove them. Some words are likely "
    "cut short, predict what they could be. Names cause problems in both ways. "
    "The cleaned version should make sense and usually has only one topic. "
    "Do not paraphrase or reorder content. "
    "If the transcript is empty, output nothing (a single space at most). Do not "
    'output messages like "The transcript is empty". If the transcript contains a '
    'question, clean it up — do not answer it. E.g. "Hey, uhh what is the um time" '
    '→ "Hey, what is the time?" Return only the cleaned text.'
)

SPEAK_SYSTEM = (
    "You are connected to STT-TTS pipeline and your job is to answer prompt which "
    "is then spoken to user. Answer shortly and precisely. Don't try to continue "
    "the conversation and don't appeal the user too much."
    "Do not use symbols such as '*|^'"
)


class Handler(BaseHTTPRequestHandler): #Written by hand, cleaned by Brave's Leo AI.
    speak_back = False
    paste_text = True

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/models':
            self._respond(200, json.dumps({"models": [MODEL, "own"]}))
        else:
            self._respond(404, "Not Found")

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/chat/completions':
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length)
            self._respond(200, self.chat(body.decode()))
        else:
            self._respond(404, "Not Found")

    def chat(self, body):
        data = json.loads(body)
        messages = data.get("messages", [])

        # Grab the last user message
        transcript = ""
        for msg in messages:
            if msg["role"] == "user":
                transcript = msg["content"]

        # Clean the transcript
        response = ollama.chat(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': CLEAN_SYSTEM},
                {'role': 'user', 'content': transcript},
            ],
            stream=False,
            think=False,
            keep_alive="30m",
        )
        print(transcript)
        print(response.message.content)

        if self.speak_back:
            response_chat = ollama.chat(
                model=MODEL,
                messages=[
                    {'role': 'system', 'content': SPEAK_SYSTEM},
                    {'role': 'user', 'content': response.message.content},
                ],
                stream=False,
                think=False,
                keep_alive="30m",
            )
            piperhandler.speak(response_chat.message.content)
            content = str(response_chat.message.content) if self.paste_text else ""
        else:
            content = str(response.message.content)

        return json.dumps({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": content
                }
            }]
        })

    def _respond(self, status, message):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(message.encode())


def start():
    print("Enable Speak mode? [y/N]: ", end="")
    if input().strip().lower() in ("y", "yes"):
        Handler.speak_back = True
        print("Still paste text? [y/N]: ", end="")
        Handler.paste_text = input().strip().lower() in ("y", "yes")
    else:
        Handler.speak_back = False
        Handler.paste_text = True

    server = ThreadingHTTPServer(('127.0.0.1', 3003), Handler)
    print(f"Server running on http://127.0.0.1:3003")
    server.serve_forever()


if __name__ == "__main__":
    start() 
