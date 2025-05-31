# setup.py
import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_directories():
    """Create necessary directories"""
    directories = [
        'static/videos',
        'static/css',
        'static/js',
        'templates',
        'text_to_isl'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def download_models():
    """Download required models"""
    import nltk
    import stanza
    
    # Download NLTK data
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('stopwords')
    
    # Download Stanza models
    stanza.download('en')

def clone_isl_repo():
    """Clone the ISL repository if not present"""
    if not os.path.exists('text_to_isl'):
        subprocess.run([
            'git', 'clone', 
            'https://github.com/shoebham/text_to_isl.git'
        ])

if __name__ == '__main__':
    print("Setting up Text to Sign Language Translator...")
    
    print("1. Creating directories...")
    setup_directories()
    
    print("2. Cloning ISL repository...")
    clone_isl_repo()
    
    print("3. Installing requirements...")
    install_requirements()
    
    print("4. Downloading models...")
    download_models()
    
    print("Setup complete! Run 'python app.py' to start the application.")
