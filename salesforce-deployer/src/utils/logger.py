import logging

def setup_logger(name=None, log_file=None, level=logging.INFO, verbose=False):
    """
    Set up a logger with console and optional file output.
    
    Args:
        name: Logger name (optional)
        log_file: Path to log file (optional)
        level: Logging level
        verbose: Enable debug level if True
        
    Returns:
        Configured logger instance
    """
    # If name not provided, use default
    if name is None:
        name = "salesforce_deployer"
        
    # Set level based on verbose flag
    if verbose:
        level = logging.DEBUG
        
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Example usage
# logger = setup_logger('salesforce_deployer', 'salesforce_deployer.log')
# logger = setup_logger(verbose=True)  # Debug level with default name
# logger = setup_logger()  # Default configuration