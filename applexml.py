import xml.etree.ElementTree as ET

def xml_to_dict(element):
    """Convert an XML element into a Python dictionary."""
    if element.tag == 'dict':
        result = {}
        key = None
        for child in element:
            if child.tag == 'key':
                key = child.text
            elif child.tag == 'string':
                if key:
                    result[key] = child.text
                    key = None
                else:
                    print(f"Warning: 'string' tag without associated key: {ET.tostring(child, encoding='unicode')}")
            elif child.tag == 'integer':
                if key:
                    result[key] = int(child.text)
                    key = None
                else:
                    print(f"Warning: 'integer' tag without associated key: {ET.tostring(child, encoding='unicode')}")
            elif child.tag == 'real':
                if key:
                    result[key] = float(child.text)
                    key = None
                else:
                    print(f"Warning: 'integer' tag without associated key: {ET.tostring(child, encoding='unicode')}")
            elif child.tag == 'true':
                if key:
                    result[key] = True
                    key = None
                else:
                    print(f"Warning: 'true' tag without associated key: {ET.tostring(child, encoding='unicode')}")
            elif child.tag == 'false':
                if key:
                    result[key] = False
                    key = None
                else:
                    print(f"Warning: 'false' tag without associated key: {ET.tostring(child, encoding='unicode')}")
            elif child.tag == 'array':
                if key:
                    if all(x.tag == 'string' for x in child):
                        result[key] = [int(item.text) for item in child]
                    else:
                        result[key] = [xml_to_dict(item) for item in child]
                        key = None
                else:
                    print(f"Warning: 'array' tag without associated key: {ET.tostring(child, encoding='unicode')}")
            elif child.tag == 'dict':
                if key is not None:
                    result[key] = xml_to_dict(child)
                    key = None
                else:
                    print(f"Warning: Nested 'dict' tag without associated key: {ET.tostring(child)}")
            else:
                print(f"Warning: Unsupported element: {child.tag}, content: {ET.tostring(child, encoding='unicode')}")
        return result
    elif element.tag == 'array':
        return [xml_to_dict(item) for item in element]
    else:
        print(f"Error: Unexpected root element: {element.tag}")
        raise ValueError(f"Unsupported root element: {element.tag}")

def parse_xml(xml_file):
    """Parse XML file and convert it to a dictionary."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    if root.tag == 'plist':
        dict_elem = root.find('dict')
        if dict_elem is not None:
            return xml_to_dict(dict_elem)
        else:
            raise ValueError("Root plist element does not contain a dict.")
    else:
        raise ValueError("Root element is not 'plist'.")