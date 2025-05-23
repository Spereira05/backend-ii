import logging
import os
from logging.handlers import TimedRotatingFileHandler
import time
from datetime import datetime
import sys

class CustomFormatter(logging.Formatter):
    """Custom formatter that includes milliseconds and timezone info"""
    
    def formatTime(self, record, datefmt=None):
        """Override to include milliseconds in timestamps"""
        if datefmt:
            return datetime.fromtimestamp(record.created).strftime(datefmt)
        else:
            # Format with ISO 8601 and milliseconds
            return datetime.fromtimestamp(record.created).isoformat(timespec='milliseconds')

def setup_advanced_logger(name, log_dir='logs'):
    """
    Sets up an advanced logger with:
    - Console output for INFO and above
    - Daily rotating files for all logs
    - A separate rotating file for errors
    - Detailed formatting with millisecond precision
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    detailed_formatter = CustomFormatter(
        '%(asctime)s %(levelname)-8s [%(processName)s:%(process)d] [%(threadName)s:%(thread)d] '
        '%(name)s.%(funcName)s:%(lineno)d - %(message)s'
    )
    
    console_formatter = CustomFormatter('%(asctime)s %(levelname)-8s - %(message)s')
    
    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Set up daily rotating file handler for all logs
    all_logs_file = os.path.join(log_dir, 'application.log')
    file_handler = TimedRotatingFileHandler(
        all_logs_file,
        when='midnight',
        interval=1,  # Rotate every day
        backupCount=30  # Keep 30 days of logs
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    file_handler.suffix = "%Y-%m-%d"  # Date suffix for rotated files
    
    # Set up daily rotating file handler for errors only
    error_logs_file = os.path.join(log_dir, 'errors.log')
    error_handler = TimedRotatingFileHandler(
        error_logs_file,
        when='midnight',
        interval=1,
        backupCount=60  # Keep 60 days of error logs
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    error_handler.suffix = "%Y-%m-%d"
    
    # Add all handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger

def simulate_application_with_logs(logger):
    """Simulate an application that generates logs at different levels"""
    logger.info("Application started")
    
    # Simulate normal operation logs
    for i in range(5):
        logger.debug(f"Debug information #{i+1}: Processing data batch")
        logger.info(f"Successfully processed item #{i+1}")
        time.sleep(0.5)  # Small delay to demonstrate timestamps
    
    # Simulate a warning condition
    logger.warning("System resource usage is high (CPU: 85%)")
    
    # Simulate error conditions
    try:
        # Intentional error
        value = 100 / 0
    except Exception as e:
        logger.error(f"Division error occurred: {str(e)}", exc_info=True)
    
    try:
        # Another intentional error
        non_existent = {}
        value = non_existent['key']
    except Exception as e:
        logger.critical(f"Critical error in data access: {str(e)}", exc_info=True)
    
    logger.info("Application finished")

if __name__ == "__main__":
    # Set up our advanced logger
    logger = setup_advanced_logger('advanced_app')
    
    # Run the simulation
    logger.info("="*50)
    logger.info(f"Log demonstration started at {datetime.now().isoformat()}")
    logger.info("="*50)
    
    simulate_application_with_logs(logger)
    
    print("\nLogs have been generated with the following features:")
    print("1. Daily log rotation (files will rotate at midnight)")
    print("2. Detailed timestamps with millisecond precision")
    print("3. Process and thread information included")
    print("4. Separate error log file")
    print("\nCheck the generated log files in the 'logs' directory:")
    print("- logs/application.log - Contains all logs (DEBUG and above)")
    print("- logs/errors.log - Contains only ERROR and CRITICAL logs")