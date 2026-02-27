"""
UML Diagram Renderer
Renders PlantUML diagrams to PNG/SVG without CLI installation
"""
from plantuml import PlantUML
import os

def render_diagram(puml_file, output_format='png'):
    """
    Render PlantUML diagram using remote server
    
    Args:
        puml_file: Path to .puml file
        output_format: 'png' or 'svg'
    """
    # Use public PlantUML server
    plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    
    with open(puml_file, 'r') as f:
        puml_code = f.read()
    
    output_file = puml_file.replace('.puml', f'.{output_format}')
    
    print(f"Rendering {puml_file}...")
    
    if output_format == 'png':
        plantuml.processes_file(puml_file, outfile=output_file)
    else:
        # For SVG, switch to SVG server
        svg_plantuml = PlantUML(url='http://www.plantuml.com/plantuml/svg/')
        svg_plantuml.processes_file(puml_file, outfile=output_file)
    
    print(f"✓ Diagram saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    # Render the example diagram
    diagram_file = "diagram.puml"
    
    if os.path.exists(diagram_file):
        render_diagram(diagram_file, 'png')
        render_diagram(diagram_file, 'svg')
    else:
        print(f"Error: {diagram_file} not found!")
