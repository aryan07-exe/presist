from flask import Flask, request, render_template, redirect, url_for
from huggingface_hub import InferenceClient
from PIL import Image
import io
import base64

app = Flask(__name__)

# Hugging Face API details
HUGGINGFACE_MODEL = "Datou1111/shou_xin"
HUGGINGFACE_TOKEN = "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"
client = InferenceClient(HUGGINGFACE_MODEL, token=HUGGINGFACE_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']

        # Generate image from the prompt using Hugging Face API
        try:
            image = client.text_to_image(prompt)

            # Convert image to base64 for rendering in the UI
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            return render_template('index.html', image_data=image_str, prompt=prompt)
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)