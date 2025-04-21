import unittest
import logging
import tempfile
import os
from unittest.mock import patch

from src.utils.logger import setup_logger


class TestLogger(unittest.TestCase):
    
    def setUp(self):
        self.log_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.log_dir, "test.log")
    
    def tearDown(self):
        # Reset logging configuration
        logging.root.handlers = []
        
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.log_dir)
    
    def test_setup_logger_default(self):
        """Test setting up logger with default settings."""
        logger = setup_logger()
        
        # Should have at least one handler
        self.assertGreaterEqual(len(logger.handlers), 1)
        
        # Default level should be INFO
        self.assertEqual(logger.level, logging.INFO)
    
    def test_setup_logger_verbose(self):
        """Test setting up logger in verbose mode."""
        logger = setup_logger(verbose=True)
        
        # Default level should be DEBUG in verbose mode
        self.assertEqual(logger.level, logging.DEBUG)
    
    def test_setup_logger_with_file(self):
        """Test logger with file output."""
        # Use tempfile for safer file operations
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            log_file = temp.name
        
        try:
            logger = setup_logger("test_file_logger", log_file=log_file)
            logger.info("Test message to file")
            
            # Force closure of all handlers
            for handler in logger.handlers:
                handler.close()
                
            logger.handlers.clear()
            
            # Verify the file exists and contains the message
            with open(log_file, 'r') as f:
                content = f.read()
                self.assertTrue("Test message to file" in content)
        finally:
            import os
            # Make sure file is closed and then try to remove
            try:
                os.remove(log_file)
            except:
                pass
    
    def test_log_format(self):
        """Test log format in logs."""
        logger = setup_logger("test_logger")
        # Check if the first handler exists and has a formatter
        self.assertTrue(len(logger.handlers) > 0)
        handler = logger.handlers[0]
        self.assertIsNotNone(handler.formatter)
        # Check the format string
        format_str = handler.formatter._fmt
        self.assertEqual(format_str, '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    unittest.main()