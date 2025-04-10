import logging
import json
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)

# Configure logging
log_file = log_dir / 'interview_simulator.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('interview_simulator')

def log_request_response(endpoint: str, request_data: dict, response_data: dict, error: str = None):
    """Log request and response data for an endpoint"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'endpoint': endpoint,
        'request': request_data,
        'response': response_data,
    }
    if error:
        log_entry['error'] = error
    
    logger.info(json.dumps(log_entry, indent=2))

def log_openai_interaction(prompt: str, response: dict, error: str = None):
    """Log OpenAI API interactions"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': 'openai_interaction',
        'prompt': prompt,
        'response': response,
    }
    if error:
        log_entry['error'] = error
    
    logger.info(json.dumps(log_entry, indent=2))
