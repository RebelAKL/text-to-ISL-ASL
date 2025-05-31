# app.py
from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import subprocess
import time
from threading import Thread
import json

# Add the ISL repo to path
sys.path.append('text_to_isl')

# Import ISL functionality
try:
    from text_to_isl.main import process_isl_text
except ImportError:
    print("ISL module not found. Please ensure text_to_isl repo is in the directory.")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/videos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class SignLanguageTranslator:
    def __init__(self):
        self.isl_processor = ISLProcessor()
        self.asl_processor = ASLProcessor()
    
    def translate(self, text, language='isl'):
        """Main translation function"""
        if language.lower() == 'isl':
            return self.isl_processor.translate(text)
        elif language.lower() == 'asl':
            return self.asl_processor.translate(text)
        else:
            raise ValueError("Unsupported language. Use 'isl' or 'asl'")

class ISLProcessor:
    """ISL translation using the provided repository"""
    
    def __init__(self):
        self.setup_isl_environment()
    
    def setup_isl_environment(self):
        """Setup ISL processing environment"""
        try:
            # Download required models if not present
            import stanza
            import nltk
            
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('wordnet', quiet=True)
            
        except Exception as e:
            print(f"Warning: Could not setup ISL environment: {e}")
    
    def translate(self, text):
        """Translate text to ISL"""
        try:
            # Use the ISL repository's main processing function
            result = self.process_text_to_isl(text)
            return {
                'success': True,
                'video_path': result.get('video_path'),
                'isl_gloss': result.get('isl_gloss'),
                'processing_time': result.get('processing_time')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_text_to_isl(self, text):
        """Process text using ISL repository logic"""
        start_time = time.time()
        
        # Tokenization and preprocessing
        tokens = self.tokenize_text(text)
        
        # POS tagging
        pos_tags = self.pos_tag(tokens)
        
        # Convert to ISL grammar structure
        isl_tokens = self.convert_to_isl_structure(tokens, pos_tags)
        
        # Generate video
        video_path = self.generate_isl_video(isl_tokens)
        
        processing_time = time.time() - start_time
        
        return {
            'video_path': video_path,
            'isl_gloss': ' '.join(isl_tokens),
            'processing_time': processing_time
        }
    
    def tokenize_text(self, text):
        """Tokenize input text"""
        import nltk
        tokens = nltk.word_tokenize(text.lower())
        return [token for token in tokens if token.isalnum()]
    
    def pos_tag(self, tokens):
        """POS tagging"""
        import nltk
        return nltk.pos_tag(tokens)
    
    def convert_to_isl_structure(self, tokens, pos_tags):
        """Convert English structure to ISL structure (SOV)"""
        # Basic ISL grammar conversion
        # This is a simplified version - the actual repo has more complex rules
        
        subjects = []
        objects = []
        verbs = []
        others = []
        
        for token, pos in pos_tags:
            if pos.startswith('PRP'):  # Pronouns (subjects)
                subjects.append(token.upper())
            elif pos.startswith('NN'):  # Nouns (can be objects)
                objects.append(token.upper())
            elif pos.startswith('VB'):  # Verbs
                verbs.append(token.upper())
            else:
                others.append(token.upper())
        
        # ISL follows SOV structure
        isl_structure = subjects + objects + verbs + others
        return isl_structure
    
    def generate_isl_video(self, isl_tokens):
        """Generate ISL video from tokens"""
        # This would use the actual video generation logic from the repo
        # For demo purposes, return a placeholder
        video_filename = f"isl_{int(time.time())}.mp4"
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
        
        # Simulate video generation
        self.create_placeholder_video(video_path, isl_tokens)
        
        return video_filename

    def create_placeholder_video(self, video_path, tokens):
        """Create a placeholder video (replace with actual ISL video generation)"""
        # This is where the actual SIGML to video conversion would happen
        # For now, create a simple text-based representation
        with open(video_path.replace('.mp4', '.txt'), 'w') as f:
            f.write(f"ISL Signs: {' -> '.join(tokens)}")

class ASLProcessor:
    """ASL translation processor"""
    
    def __init__(self):
        self.setup_asl_environment()
    
    def setup_asl_environment(self):
        """Setup ASL processing environment"""
        pass
    
    def translate(self, text):
        """Translate text to ASL"""
        try:
            result = self.process_text_to_asl(text)
            return {
                'success': True,
                'video_path': result.get('video_path'),
                'asl_gloss': result.get('asl_gloss'),
                'processing_time': result.get('processing_time')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_text_to_asl(self, text):
        """Process text to ASL"""
        start_time = time.time()
        
        # Basic ASL processing
        tokens = text.lower().split()
        asl_tokens = [token.upper() for token in tokens if token.isalnum()]
        
        # Generate ASL video
        video_path = self.generate_asl_video(asl_tokens)
        
        processing_time = time.time() - start_time
        
        return {
            'video_path': video_path,
            'asl_gloss': ' '.join(asl_tokens),
            'processing_time': processing_time
        }
    
    def generate_asl_video(self, asl_tokens):
        """Generate ASL video from tokens"""
        video_filename = f"asl_{int(time.time())}.mp4"
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
        
        # Create placeholder for ASL video
        with open(video_path.replace('.mp4', '.txt'), 'w') as f:
            f.write(f"ASL Signs: {' -> '.join(asl_tokens)}")
        
        return video_filename

# Initialize translator
translator = SignLanguageTranslator()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    """Handle translation requests"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text'].strip()
    language = data.get('language', 'isl').lower()
    
    if not text:
        return jsonify({'error': 'Empty text provided'}), 400
    
    try:
        result = translator.translate(text, language)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/video/<filename>')
def serve_video(filename):
    """Serve generated videos"""
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(video_path):
        return send_file(video_path)
    else:
        return "Video not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
