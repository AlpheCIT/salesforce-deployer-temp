import xml.etree.ElementTree as ET
from xml.dom import minidom
import builtins
import functools
import contextlib

def element_to_string(element: ET.Element, pretty=True) -> str:
    """
    Convert XML Element to string.
    
    Args:
        element: XML Element to convert
        pretty: Whether to pretty-print the XML
        
    Returns:
        XML string
    """
    if pretty:
        rough_string = ET.tostring(element, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    else:
        return ET.tostring(element, encoding='unicode')

# Example usage:
# xml_element = ET.Element('root')
# xml_string = element_to_string(xml_element)
# with open(file_path, 'w') as f:
#     f.write(xml_string)

def safe_xml_write(file_obj, content):
    """
    Safely write XML content to a file, ensuring it's a string.
    
    Args:
        file_obj: File object or path
        content: XML content (Element or string)
    """
    # Convert Element to string if needed
    if hasattr(content, 'tag'):  # It's an Element
        content = element_to_string(content)
    
    # Write to file
    if isinstance(file_obj, str):
        with open(file_obj, 'w') as f:
            f.write(content)
    else:
        file_obj.write(content)

@contextlib.contextmanager
def patch_xml_writing():
    """
    Context manager that patches open() to safely handle XML writing.
    
    Usage:
        with patch_xml_writing():
            # Code that might write XML to files
    """
    original_open = builtins.open
    
    @functools.wraps(original_open)
    def patched_open(*args, **kwargs):
        file_obj = original_open(*args, **kwargs)
        if 'w' in args[1] if len(args) > 1 else kwargs.get('mode', ''):
            # This is a write operation
            original_write = file_obj.write
            
            @functools.wraps(original_write)
            def safe_write(content):
                # If content looks like XML Element, convert it
                if hasattr(content, 'tag'):
                    return original_write(element_to_string(content))
                return original_write(content)
            
            file_obj.write = safe_write
        return file_obj
    
    # Apply the patch
    builtins.open = patched_open
    try:
        yield
    finally:
        # Restore original
        builtins.open = original_open