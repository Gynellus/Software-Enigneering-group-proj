from flask import Flask, render_template, request, jsonify
from utils import process_paper_data, convert_input_to_string, summarize, translate_to_dutch
import os
from werkzeug.utils import secure_filename

application = Flask(__name__)

@application.route('/')
def index():
    """ Render the main page. """
    return render_template('input.html')

@application.route('/summarize', methods=['POST'])
def summarize_paper():
    try:
        # Check if the request has a file part
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            temp_path = os.path.join('temp', filename)
            file.save(temp_path)
            input_data = temp_path
        else:
            input_data = request.form.get('text', '')

        # Convert input to string
        paper_text = convert_input_to_string(input_data)
        
        # Summarize the input paper
        paper_summary = summarize(paper_text)

        # If temp file was created, delete it
        if os.listdir(os.path.join(os.getcwd(), 'temp')) != []:
            os.remove(temp_path)       

        return jsonify({'result': paper_summary})
    except Exception as e:
        application.logger.error(f"Error in summarize_paper: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@application.route('/find_similar', methods=['POST'])
def find_similar_papers():
    try:
        # Retrieve the text for which similar papers are to be found
        paper_text = request.form.get('text', '')
        
        # Call utility function to process the paper data
        similar_papers = process_paper_data(paper_text)

        application.logger.info(f"Similar papers: {similar_papers}")

        # Prepare and return the response
        return jsonify({'similar_papers': similar_papers})
    except Exception as e:
        application.logger.error(f"Error in find_similar_papers: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@application.route('/translate', methods=['POST'])
def translate_text():
    try:
        text = request.form.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided for translation'}), 400

        translated_text = translate_to_dutch(text)
        return jsonify({'translatedText': translated_text})
    except Exception as e:
        application.logger.error(f"Error in translate_text: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    application.run(debug=False)
