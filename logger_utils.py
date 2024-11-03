# logger_utils.py
import logging
import functools
import inspect
import os
import datetime
from pathlib import Path

def setup_logger():
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = log_dir / f'maml_trace_{timestamp}.log'
    
    # Setup logging configuration
    logging.basicConfig(
        filename=str(log_filename),
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Also print to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console_handler)
    
    return logging.getLogger('MAML')

def trace_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('MAML')
        
        # Get caller information
        frame = inspect.currentframe()
        caller = frame.f_back
        caller_name = caller.f_code.co_name if caller else "None"
        
        # Log function entry
        logger.debug(f"ENTER: {caller_name} -> {func.__name__}")
        
        try:
            # Execute function
            result = func(*args, **kwargs)
            
            # Log function exit
            logger.debug(f"EXIT: {func.__name__}")
            return result
            
        except Exception as e:
            # Log any errors
            logger.error(f"ERROR in {func.__name__}: {str(e)}")
            raise
    
    return wrapper
