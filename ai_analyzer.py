"""
Advanced AI-Powered UML Analyzer using LangChain
Implements Phase 1 & 2: Preprocessing, Text Analysis, and Component Identification
"""
import os
import json
import re
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Try to import LangChain components
try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import PydanticOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("⚠️ LangChain not available. Install with: pip install langchain langchain-groq")


class UMLAttribute(BaseModel):
    """Represents a class attribute"""
    name: str = Field(description="Attribute name")
    data_type: Optional[str] = Field(default="String", description="Data type")
    visibility: str = Field(default="-", description="Visibility: + (public), - (private), # (protected)")
    confidence: float = Field(default=0.8, description="Confidence score 0-1")


class UMLMethod(BaseModel):
    """Represents a class method"""
    name: str = Field(description="Method name")
    return_type: Optional[str] = Field(default="void", description="Return type")
    visibility: str = Field(default="+", description="Visibility")
    confidence: float = Field(default=0.8, description="Confidence score 0-1")


class UMLClass(BaseModel):
    """Represents a UML class"""
    name: str = Field(description="Class name")
    attributes: List[UMLAttribute] = Field(default_factory=list, description="Class attributes")
    methods: List[UMLMethod] = Field(default_factory=list, description="Class methods")
    stereotype: Optional[str] = Field(default=None, description="Stereotype (e.g., <<interface>>, <<abstract>>)")
    confidence: float = Field(default=0.9, description="Confidence score 0-1")


class UMLRelationship(BaseModel):
    """Represents a UML relationship"""
    from_class: str = Field(description="Source class name")
    to_class: str = Field(description="Target class name")
    relationship_type: str = Field(description="Type: inheritance, association, aggregation, composition, dependency")
    multiplicity_from: str = Field(default="", description="Source multiplicity (e.g., '1', '0..*')")
    multiplicity_to: str = Field(default="", description="Target multiplicity")
    label: Optional[str] = Field(default=None, description="Relationship label")
    confidence: float = Field(default=0.85, description="Confidence score 0-1")


class UMLDiagramData(BaseModel):
    """Complete UML diagram data structure"""
    classes: List[UMLClass] = Field(default_factory=list)
    relationships: List[UMLRelationship] = Field(default_factory=list)
    overall_confidence: float = Field(default=0.8, description="Overall extraction confidence")


class AdvancedUMLAnalyzer:
    """Advanced AI-powered UML analyzer using LangChain and LLMs"""
    
    def __init__(self, use_groq: bool = True):
        """Initialize the analyzer"""
        self.use_llm = use_groq and LANGCHAIN_AVAILABLE
        
        if self.use_llm:
            api_key = os.getenv("GROQ_API_KEY")
            if api_key and api_key != "your_groq_api_key_here":
                try:
                    self.llm = ChatGroq(
                        model=os.getenv("AI_MODEL", "llama-3.3-70b-versatile"),
                        temperature=float(os.getenv("AI_TEMPERATURE", "0.3")),
                        max_tokens=int(os.getenv("AI_MAX_TOKENS", "2000"))
                    )
                    print("✅ Groq LLM initialized successfully")
                except Exception as e:
                    print(f"⚠️ Failed to initialize Groq: {e}")
                    self.use_llm = False
            else:
                print("⚠️ Groq API key not configured. Using fallback NLP.")
                self.use_llm = False
    
    def extract_with_llm(self, text: str) -> UMLDiagramData:
        """Extract UML components using LLM (Groq with Llama 3.3 70B)"""
        
        # Create parser for structured output
        parser = PydanticOutputParser(pydantic_object=UMLDiagramData)
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert software architect specialized in UML diagram generation.
Analyze the provided Software Requirements Specification (SRS) text and extract:
1. **Classes**: Identify all nouns that represent entities (User, Product, Order, etc.)
2. **Attributes**: Properties of each class (name, email, price, etc.) with data types
3. **Methods**: Actions/behaviors (login(), save(), calculate(), etc.)
4. **Relationships**: 
   - Inheritance (is-a): "Admin extends User", "Customer inherits from User"
   - Association: "User places Order", "Customer has Account"
   - Aggregation: "Cart contains Products" (weak ownership)
   - Composition: "Order owns OrderItems" (strong ownership)
   - Dependency: "Service uses Repository"
5. **Multiplicities**: "1", "0..1", "1..*", "0..*"
6. **Confidence Scores**: Rate your certainty (0.0 to 1.0) for each component

Apply semantic analysis to resolve synonyms (e.g., "Client" = "Customer", "Product" = "Item").

{format_instructions}

Be precise and output valid JSON only."""),
            ("user", "Analyze this SRS and extract UML components:\n\n{text}")
        ])
        
        # Format the prompt
        formatted_prompt = prompt.format_messages(
            text=text,
            format_instructions=parser.get_format_instructions()
        )
        
        try:
            # Get LLM response
            response = self.llm.invoke(formatted_prompt)
            
            # Parse the response
            diagram_data = parser.parse(response.content)
            
            # Calculate overall confidence
            all_confidences = []
            for cls in diagram_data.classes:
                all_confidences.append(cls.confidence)
                all_confidences.extend([attr.confidence for attr in cls.attributes])
                all_confidences.extend([method.confidence for method in cls.methods])
            all_confidences.extend([rel.confidence for rel in diagram_data.relationships])
            
            if all_confidences:
                diagram_data.overall_confidence = sum(all_confidences) / len(all_confidences)
            
            return diagram_data
            
        except Exception as e:
            print(f"❌ LLM extraction failed: {e}")
            print("🔄 Falling back to rule-based extraction...")
            return self.extract_with_rules(text)
    
    def extract_with_rules(self, text: str) -> UMLDiagramData:
        """Fallback: Rule-based extraction using NLP patterns"""
        diagram_data = UMLDiagramData()
        
        # Enhanced patterns for class detection
        class_patterns = [
            r'\b[Cc]lass\s+([A-Z][A-Za-z0-9_]*)',
            r'\b([A-Z][A-Za-z0-9_]*)\s+(?:entity|object|model|class)',
            r'(?:The|A)\s+([A-Z][A-Za-z0-9_]*)\s+(?:has|contains|manages)',
        ]
        
        found_classes = set()
        for pattern in class_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                class_name = match.group(1)
                if class_name[0].isupper():
                    found_classes.add(class_name)
        
        # Create UML classes with attributes
        lines = text.split('\n')
        for line in lines:
            # Pattern: "ClassName has attr1, attr2, attr3"
            attr_match = re.match(r'([A-Z][A-Za-z]*)\s+(?:has|contains|includes|with)\s+(.+)', line.strip())
            if attr_match:
                class_name = attr_match.group(1)
                found_classes.add(class_name)
                attributes_text = attr_match.group(2)
                
                # Extract class from diagram_data or create new
                uml_class = next((c for c in diagram_data.classes if c.name == class_name), None)
                if not uml_class:
                    uml_class = UMLClass(name=class_name, confidence=0.85)
                    diagram_data.classes.append(uml_class)
                
                # Parse attributes
                attr_parts = [a.strip().rstrip('.,;') for a in re.split(r'[,;]', attributes_text)]
                for attr_text in attr_parts:
                    if attr_text and len(attr_text) < 50:
                        # Try to detect data type
                        data_type = "String"
                        if any(word in attr_text.lower() for word in ['id', 'uuid']):
                            data_type = "UUID"
                        elif any(word in attr_text.lower() for word in ['date', 'time']):
                            data_type = "Date"
                        elif any(word in attr_text.lower() for word in ['price', 'cost', 'amount']):
                            data_type = "Decimal"
                        elif any(word in attr_text.lower() for word in ['count', 'number', 'quantity']):
                            data_type = "Integer"
                        
                        uml_class.attributes.append(UMLAttribute(
                            name=attr_text,
                            data_type=data_type,
                            confidence=0.75
                        ))
        
        # Add remaining classes without attributes
        for class_name in found_classes:
            if not any(c.name == class_name for c in diagram_data.classes):
                diagram_data.classes.append(UMLClass(
                    name=class_name,
                    confidence=0.80
                ))
        
        # Extract relationships
        class_names = [c.name for c in diagram_data.classes]
        
        for line in lines:
            line_lower = line.lower()
            
            # Find mentioned classes in this line
            mentioned_classes = [name for name in class_names if name in line]
            
            if len(mentioned_classes) >= 2:
                class1, class2 = mentioned_classes[0], mentioned_classes[1]
                
                # Determine relationship type and confidence
                if any(word in line_lower for word in ['inherits', 'extends', 'is a', 'subclass', 'derives']):
                    diagram_data.relationships.append(UMLRelationship(
                        from_class=class1,
                        to_class=class2,
                        relationship_type='inheritance',
                        confidence=0.90
                    ))
                elif any(word in line_lower for word in ['owns', 'composed of']):
                    diagram_data.relationships.append(UMLRelationship(
                        from_class=class1,
                        to_class=class2,
                        relationship_type='composition',
                        multiplicity_from='1',
                        multiplicity_to='0..*',
                        confidence=0.85
                    ))
                elif any(word in line_lower for word in ['contains', 'has many', 'includes']):
                    diagram_data.relationships.append(UMLRelationship(
                        from_class=class1,
                        to_class=class2,
                        relationship_type='aggregation',
                        multiplicity_from='1',
                        multiplicity_to='0..*',
                        confidence=0.80
                    ))
                elif any(word in line_lower for word in ['uses', 'depends on', 'requires']):
                    diagram_data.relationships.append(UMLRelationship(
                        from_class=class1,
                        to_class=class2,
                        relationship_type='dependency',
                        confidence=0.75
                    ))
                elif any(word in line_lower for word in ['has', 'has a', 'associated with', 'relates to']):
                    diagram_data.relationships.append(UMLRelationship(
                        from_class=class1,
                        to_class=class2,
                        relationship_type='association',
                        confidence=0.70
                    ))
        
        # Calculate overall confidence
        all_confidences = [c.confidence for c in diagram_data.classes]
        all_confidences.extend([r.confidence for r in diagram_data.relationships])
        diagram_data.overall_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.7
        
        return diagram_data
    
    def analyze(self, text: str) -> UMLDiagramData:
        """Main analysis method - routes to LLM or rules"""
        if self.use_llm:
            return self.extract_with_llm(text)
        else:
            return self.extract_with_rules(text)
    
    def to_plantuml(self, diagram_data: UMLDiagramData) -> str:
        """Convert UMLDiagramData to PlantUML code"""
        lines = ["@startuml", ""]
        
        # Add classes
        for cls in diagram_data.classes:
            # Add stereotype if exists
            if cls.stereotype:
                lines.append(f"class {cls.name} {cls.stereotype} {{")
            else:
                lines.append(f"class {cls.name} {{")
            
            # Add attributes
            for attr in cls.attributes:
                lines.append(f"  {attr.visibility} {attr.name}: {attr.data_type}")
            
            # Add methods
            for method in cls.methods:
                lines.append(f"  {method.visibility} {method.name}(): {method.return_type}")
            
            lines.append("}")
            lines.append("")
        
        # Add relationships
        for rel in diagram_data.relationships:
            mult_from = f'"{rel.multiplicity_from}"' if rel.multiplicity_from else ""
            mult_to = f'"{rel.multiplicity_to}"' if rel.multiplicity_to else ""
            label = f": {rel.label}" if rel.label else ""
            
            if rel.relationship_type == 'inheritance':
                lines.append(f"{rel.from_class} --|> {rel.to_class}")
            elif rel.relationship_type == 'composition':
                lines.append(f"{rel.from_class} {mult_from} *-- {mult_to} {rel.to_class}{label}")
            elif rel.relationship_type == 'aggregation':
                lines.append(f"{rel.from_class} {mult_from} o-- {mult_to} {rel.to_class}{label}")
            elif rel.relationship_type == 'dependency':
                lines.append(f"{rel.from_class} ..> {rel.to_class}{label}")
            else:  # association
                lines.append(f"{rel.from_class} {mult_from} -- {mult_to} {rel.to_class}{label}")
        
        lines.append("")
        lines.append("@enduml")
        
        return "\n".join(lines)
    
    def to_json(self, diagram_data: UMLDiagramData) -> str:
        """Export to JSON format"""
        return diagram_data.model_dump_json(indent=2)
    
    def to_xmi(self, diagram_data: UMLDiagramData) -> str:
        """Export to XMI format (XML Metadata Interchange)"""
        xmi_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<XMI xmi.version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.0">',
            '  <uml:Model xmi:id="model" name="GeneratedModel">',
        ]
        
        # Add classes
        for idx, cls in enumerate(diagram_data.classes):
            xmi_lines.append(f'    <packagedElement xmi:type="uml:Class" xmi:id="class_{idx}" name="{cls.name}">')
            
            # Add attributes
            for attr_idx, attr in enumerate(cls.attributes):
                xmi_lines.append(f'      <ownedAttribute xmi:id="attr_{idx}_{attr_idx}" name="{attr.name}" visibility="{attr.visibility.replace("-", "private").replace("+", "public")}">')
                xmi_lines.append(f'        <type xmi:type="uml:PrimitiveType" href="{attr.data_type}"/>')
                xmi_lines.append('      </ownedAttribute>')
            
            xmi_lines.append('    </packagedElement>')
        
        xmi_lines.append('  </uml:Model>')
        xmi_lines.append('</XMI>')
        
        return '\n'.join(xmi_lines)


# Singleton instance
_analyzer_instance = None

def get_analyzer() -> AdvancedUMLAnalyzer:
    """Get or create analyzer instance"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = AdvancedUMLAnalyzer()
    return _analyzer_instance
