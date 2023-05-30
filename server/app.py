# Write a simple flask app with one route to return an response from OpenAI's Gpt3.5 turbo model using the completions API
from flask  import Flask, Response, stream_with_context, request
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import json
app = Flask(__name__)
CORS(app)

def chat_gpt_helper(prompt):
    """
    This function returns the response from OpenAI's Gpt3.5 turbo model using the completions API
    """
    try:
        url = "https://api.openai.com/v1/chat/completions"
        session = requests.Session()
        payload = json.dumps({
             "model" : "gpt-3.5-turbo",
             "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
                ],
            "temperature": 0,
            "stream": True,
            })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ os.getenv('OPEN_API_KEY') # type: ignore
        }
        with session.post(url, headers=headers, data=payload) as resp:
            for line in resp.iter_lines():
                if line:
                    print(line)
                    yield f'data: %s\n\n' % line.decode('utf-8')

    except Exception as e:
        print(e)
        return str(e)

@app.route('/create-completions/gpt3', methods=['POST'])
def stream_chat_gpt():
        """
        This streams the response from ChatGPT
        """
        prompt = request.get_json(force = True).get('prompt','')
        return Response(stream_with_context(chat_gpt_helper(prompt)),
                         mimetype='text/event-stream')
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded = True)