# Write a simple flask app with one route to return an response from OpenAI's Gpt3.5 turbo model using the completions API
from flask  import Flask, Response, stream_with_context, request
import os
import openai
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
        resp = ''
        openai.api_key = os.getenv('OPEN_API_KEY')
        for chunk in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content":prompt
            }],
            stream=True,
        ):
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                    print(content, end='')
                    resp += content
                    yield f'data: %s\n\n' % resp

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