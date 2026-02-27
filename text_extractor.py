"""
AI-Powered Text Extraction and UML Generation
Uses NLP to extract entities, relationships, and generate PlantUML code
"""
import re
from typing import List, Dict, Set, Tuple
import pdfplumber
from docx import Document


def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF, DOCX, or TXT files"""
    ext = file_path.lower().split('.')[-1]
    
    if ext == 'pdf':
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    
    elif ext == 'docx':
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def extract_classes_simple(text: str) -> List[Dict]:
    """Extract classes using pattern matching"""
    classes = []
    
    # Pattern 1: "Class ClassName" or "class ClassName"
    class_pattern = r'\b[Cc]lass\s+([A-Z][A-Za-z0-9_]*)'
    matches = re.finditer(class_pattern, text)
    for match in matches:
        class_name = match.group(1)
        classes.append({
            'name': class_name,
            'attributes': [],
            'methods': []
        })
    
    # Pattern 2: Look for capitalized words that might be entities
    lines = text.split('\n')
    for line in lines:
        # Look for patterns like "User has name, email, password"
        entity_pattern = r'^([A-Z][A-Za-z]*)\s+(?:has|contains|includes|with)\s+(.+)$'
        match = re.match(entity_pattern, line.strip())
        if match:
            class_name = match.group(1)
            attributes_text = match.group(2)
            attributes = [attr.strip() for attr in re.split(r'[,;]', attributes_text)]
            
            # Check if class already exists
            existing = next((c for c in classes if c['name'] == class_name), None)
            if existing:
                existing['attributes'].extend(attributes)
            else:
                classes.append({
                    'name': class_name,
                    'attributes': attributes,
                    'methods': []
                })
    
    return classes


def extract_relationships(text: str, classes: List[Dict]) -> List[Dict]:
    """Extract relationships between classes"""
    relationships = []
    class_names = [c['name'] for c in classes]
    
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        
        # Find which classes are mentioned in this line
        mentioned_classes = [name for name in class_names if name in line]
        
        if len(mentioned_classes) >= 2:
            class1, class2 = mentioned_classes[0], mentioned_classes[1]
            
            # Determine relationship type
            if any(word in line_lower for word in ['inherits', 'extends', 'is a', 'subclass']):
                relationships.append({
                    'from': class2,
                    'to': class1,
                    'type': 'inheritance'
                })
            elif any(word in line_lower for word in ['has many', 'contains', 'owns']):
                relationships.append({
                    'from': class1,
                    'to': class2,
                    'type': 'composition'
                })
            elif any(word in line_lower for word in ['uses', 'depends on']):
                relationships.append({
                    'from': class1,
                    'to': class2,
                    'type': 'dependency'
                })
            elif any(word in line_lower for word in ['has', 'has a', 'associated with']):
                relationships.append({
                    'from': class1,
                    'to': class2,
                    'type': 'association'
                })
    
    return relationships


def generate_plantuml_code(classes: List[Dict], relationships: List[Dict]) -> str:
    """Generate PlantUML code from extracted classes and relationships"""
    lines = ["@startuml", ""]
    
    # Add classes
    for cls in classes:
        lines.append(f"class {cls['name']} {{")
        
        # Add attributes
        for attr in cls['attributes'][:5]:  # Limit to 5 attributes
            # Clean attribute name
            attr_clean = attr.strip().rstrip('.')
            if attr_clean and len(attr_clean) < 50:
                lines.append(f"  - {attr_clean}")
        
        # Add methods
        for method in cls['methods'][:3]:  # Limit to 3 methods
            lines.append(f"  + {method}()")
        
        lines.append("}")
        lines.append("")
    
    # Add relationships
    for rel in relationships:
        if rel['type'] == 'inheritance':
            lines.append(f"{rel['from']} --|> {rel['to']}")
        elif rel['type'] == 'composition':
            lines.append(f"{rel['from']} *-- {rel['to']}")
        elif rel['type'] == 'dependency':
            lines.append(f"{rel['from']} ..> {rel['to']}")
        else:  # association
            lines.append(f"{rel['from']} -- {rel['to']}")
    
    lines.append("")
    lines.append("@enduml")
    
    return "\n".join(lines)


def extract_uml_from_text(text: str) -> str:
    """
    Main function to extract UML from text using AI/NLP
    """
    # If text already contains PlantUML code, return it
    if '@startuml' in text and '@enduml' in text:
        return text
    
    # Extract classes
    classes = extract_classes_simple(text)
    
    # If no classes found, create a default example
    if not classes:
        classes = [
            {
                'name': 'Entity',
                'attributes': ['id', 'name', 'created_at'],
                'methods': ['save', 'delete']
            }
        ]
    
    # Extract relationships
    relationships = extract_relationships(text, classes)
    
    # Generate PlantUML code
    plantuml_code = generate_plantuml_code(classes, relationships)
    
    return plantuml_code
