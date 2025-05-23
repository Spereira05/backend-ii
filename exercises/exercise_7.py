import logging
import sys
from datetime import datetime

# Configure the logging module
def setup_logger():
    # Create a logger
    logger = logging.getLogger('my_application')
    logger.setLevel(logging.DEBUG)  # Capture all levels of logs
    
    # Create console handler with a higher log level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create file handler for all logs
    file_handler = logging.FileHandler('application.log')
    file_handler.setLevel(logging.DEBUG)
    
    # Create file handler for errors only
    error_file_handler = logging.FileHandler('errors.log')
    error_file_handler.setLevel(logging.ERROR)
    
    # Create formatters and add them to the handlers
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)
    error_file_handler.setFormatter(file_format)
    
    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    
    return logger

def simulate_application_activity(logger):
    logger.debug("This is a debug message - detailed information for diagnosing problems")
    logger.info("This is an info message - confirming things are working as expected")
    logger.warning("This is a warning message - indicating something unexpected")
    
    try:
        # Simulate an error
        result = 10 / 0
    except Exception as e:
        logger.error(f"This is an error message - the application couldn't perform an operation: {str(e)}", 
                    exc_info=True)
    
    logger.critical("This is a critical message - the application is about to crash or has a severe error")

if __name__ == "__main__":
    logger = setup_logger()
    
    logger.info(f"Application started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    simulate_application_activity(logger)
    
    logger.info(f"Application ended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\nCheck the generated log files:")
    print("1. application.log - Contains all logs (DEBUG and above)")
    print("2. errors.log - Contains only ERROR and CRITICAL logs")