"""
GraphViz visualization generator for the Funding DSL Metamodel
Generates visual diagrams showing class relationships and structure.
"""

from typing import List
try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Warning: graphviz not available. Install with: pip install graphviz")


class MetamodelVisualizer:
    """Generates GraphViz diagrams for the Funding DSL metamodel"""
    
    def __init__(self):
        if GRAPHVIZ_AVAILABLE:
            self.dot = graphviz.Digraph(comment='Funding DSL Metamodel')
            self.dot.attr(rankdir='TB', size='12,8', dpi='300')
            self.dot.attr('node', shape='box', style='filled', fontname='Arial')
        else:
            self.dot = None
        
    def generate_class_diagram(self) -> str:
        """Generate a complete class diagram of the metamodel"""
        
        if not GRAPHVIZ_AVAILABLE:
            return "# Graphviz not available - install with: pip install graphviz"
        
        # Define node styles
        enum_style = {'fillcolor': 'lightblue', 'shape': 'box'}
        dataclass_style = {'fillcolor': 'lightgreen', 'shape': 'record'}
        abstract_style = {'fillcolor': 'lightyellow', 'shape': 'box', 'style': 'filled,dashed'}
        
        # Add enum nodes
        self.dot.node('FundingPlatform', 
                     '<<B>FundingPlatform</B>|GITHUB_SPONSORS|PATREON|OPEN_COLLECTIVE|KO_FI|BUY_ME_A_COFFEE|LIBERAPAY|PAYPAL|CUSTOM>',
                     **enum_style)
        
        self.dot.node('FundingType',
                     '<<B>FundingType</B>|ONE_TIME|RECURRING|BOTH>',
                     **enum_style)
        
        self.dot.node('CurrencyType',
                     '<<B>CurrencyType</B>|USD|EUR|GBP|CAD|AUD>',
                     **enum_style)
        
        # Add dataclass nodes
        self.dot.node('FundingAmount',
                     '<<B>FundingAmount</B>|+ value: float|+ currency: CurrencyType>',
                     **dataclass_style)
        
        self.dot.node('Beneficiary',
                     '<<B>Beneficiary</B>|+ name: str|+ email: Optional[str]|+ github_username: Optional[str]|+ website: Optional[str]|+ description: Optional[str]>',
                     **dataclass_style)
        
        self.dot.node('FundingTier',
                     '<<B>FundingTier</B>|+ name: str|+ amount: FundingAmount|+ description: Optional[str]|+ benefits: List[str]|+ max_sponsors: Optional[int]|+ is_active: bool>',
                     **dataclass_style)
        
        self.dot.node('FundingGoal',
                     '<<B>FundingGoal</B>|+ name: str|+ target_amount: FundingAmount|+ description: Optional[str]|+ deadline: Optional[datetime]|+ current_amount: FundingAmount|+ is_reached: bool|+ progress_percentage: float>',
                     **dataclass_style)
        
        self.dot.node('FundingSource',
                     '<<B>FundingSource</B>|+ platform: FundingPlatform|+ username: str|+ funding_type: FundingType|+ is_active: bool|+ custom_url: Optional[str]|+ platform_specific_config: Dict[str, str]>',
                     **dataclass_style)
        
        self.dot.node('FundingConfiguration',
                     '<<B>FundingConfiguration</B>|+ project_name: str|+ description: Optional[str]|+ beneficiaries: List[Beneficiary]|+ funding_sources: List[FundingSource]|+ tiers: List[FundingTier]|+ goals: List[FundingGoal]|+ preferred_currency: CurrencyType|+ min_amount: Optional[FundingAmount]|+ max_amount: Optional[FundingAmount]>',
                     **dataclass_style)
        
        # Add abstract classes
        self.dot.node('FundingModelVisitor',
                     '<<B>FundingModelVisitor</B>|+ visit_configuration()|+ visit_beneficiary()|+ visit_funding_source()|+ visit_tier()|+ visit_goal()>',
                     **abstract_style)
        
        self.dot.node('FundingModelValidator',
                     '<<B>FundingModelValidator</B>|+ validate_configuration()|+ is_valid_configuration()>',
                     **dataclass_style)
        
        # Add relationships (composition and association)
        
        # FundingAmount uses CurrencyType
        self.dot.edge('FundingAmount', 'CurrencyType', label='uses', style='dashed')
        
        # FundingSource uses FundingPlatform and FundingType
        self.dot.edge('FundingSource', 'FundingPlatform', label='uses', style='dashed')
        self.dot.edge('FundingSource', 'FundingType', label='uses', style='dashed')
        
        # FundingTier contains FundingAmount
        self.dot.edge('FundingTier', 'FundingAmount', label='contains', style='solid')
        
        # FundingGoal contains FundingAmount (2 relationships)
        self.dot.edge('FundingGoal', 'FundingAmount', label='contains (2)', style='solid')
        
        # FundingConfiguration aggregates multiple entities
        self.dot.edge('FundingConfiguration', 'Beneficiary', label='aggregates *', style='solid', arrowhead='diamond')
        self.dot.edge('FundingConfiguration', 'FundingSource', label='aggregates *', style='solid', arrowhead='diamond')
        self.dot.edge('FundingConfiguration', 'FundingTier', label='aggregates *', style='solid', arrowhead='diamond')
        self.dot.edge('FundingConfiguration', 'FundingGoal', label='aggregates *', style='solid', arrowhead='diamond')
        self.dot.edge('FundingConfiguration', 'CurrencyType', label='uses', style='dashed')
        self.dot.edge('FundingConfiguration', 'FundingAmount', label='uses', style='dashed')
        
        # Visitor pattern relationships
        self.dot.edge('FundingModelVisitor', 'FundingConfiguration', label='visits', style='dotted')
        self.dot.edge('FundingModelVisitor', 'Beneficiary', label='visits', style='dotted')
        self.dot.edge('FundingModelVisitor', 'FundingSource', label='visits', style='dotted')
        self.dot.edge('FundingModelVisitor', 'FundingTier', label='visits', style='dotted')
        self.dot.edge('FundingModelVisitor', 'FundingGoal', label='visits', style='dotted')
        
        # Validator relationship
        self.dot.edge('FundingModelValidator', 'FundingConfiguration', label='validates', style='dotted')
        
        return self.dot.source
    
    def save_diagram(self, filename: str = 'funding_metamodel', format: str = 'png') -> None:
        """Save the diagram to a file"""
        self.dot.render(filename, format=format, cleanup=True)
        print(f"Diagram saved as {filename}.{format}")
    
    def generate_concept_map(self) -> str:
        """Generate a simplified concept map showing main relationships"""
        if not GRAPHVIZ_AVAILABLE:
            return "# Graphviz not available - install with: pip install graphviz"
            
        concept_dot = graphviz.Digraph(comment='Funding DSL Concept Map')
        concept_dot.attr(rankdir='LR', size='10,6')
        concept_dot.attr('node', shape='ellipse', style='filled', fontname='Arial')
        
        # Main concepts
        concept_dot.node('Project', 'Project/Repository', fillcolor='lightcoral')
        concept_dot.node('Funding', 'Funding Configuration', fillcolor='lightgreen')
        concept_dot.node('Beneficiaries', 'Beneficiaries', fillcolor='lightblue')
        concept_dot.node('Sources', 'Funding Sources', fillcolor='lightyellow')
        concept_dot.node('Tiers', 'Sponsorship Tiers', fillcolor='lightpink')
        concept_dot.node('Goals', 'Funding Goals', fillcolor='lightgray')
        concept_dot.node('Platforms', 'Platforms\n(GitHub, Patreon, etc.)', fillcolor='lavender')
        
        # Relationships
        concept_dot.edge('Project', 'Funding', label='has')
        concept_dot.edge('Funding', 'Beneficiaries', label='defines')
        concept_dot.edge('Funding', 'Sources', label='includes')
        concept_dot.edge('Funding', 'Tiers', label='offers')
        concept_dot.edge('Funding', 'Goals', label='sets')
        concept_dot.edge('Sources', 'Platforms', label='uses')
        concept_dot.edge('Tiers', 'Goals', label='contribute to')
        
        return concept_dot.source


def generate_metamodel_documentation() -> str:
    """Generate textual documentation of the metamodel"""
    
    doc = """
# Funding DSL Metamodel Documentation

## Core Concepts

### 1. FundingConfiguration
The root entity that represents the complete funding setup for a project.
- **Attributes**: project_name, description, preferred_currency, min/max amounts
- **Relationships**: Contains multiple Beneficiaries, FundingSources, FundingTiers, and FundingGoals

### 2. Beneficiary  
Represents individuals or organizations that receive funding.
- **Attributes**: name, email, github_username, website, description
- **Purpose**: Identifies who benefits from the sponsorships

### 3. FundingSource
Represents a specific platform where sponsors can contribute.
- **Attributes**: platform, username, funding_type, custom_url, configuration
- **Supported Platforms**: GitHub Sponsors, Patreon, Open Collective, Ko-fi, etc.

### 4. FundingTier
Represents different sponsorship levels with specific benefits.
- **Attributes**: name, amount, description, benefits, max_sponsors, is_active
- **Purpose**: Structures sponsorship offerings with clear value propositions

### 5. FundingGoal
Represents funding targets and milestones.
- **Attributes**: name, target_amount, current_amount, deadline, description
- **Features**: Progress tracking, milestone management

### 6. Supporting Types
- **FundingAmount**: Monetary values with currency support
- **Enums**: FundingPlatform, FundingType, CurrencyType
- **Patterns**: Visitor pattern for traversal, Validator for consistency

## Key Relationships

1. **FundingConfiguration** aggregates all other entities (1-to-many)
2. **FundingTier** and **FundingGoal** both contain **FundingAmount** objects
3. **FundingSource** references **FundingPlatform** and **FundingType** enums
4. **FundingAmount** uses **CurrencyType** enum

## Design Patterns Used

- **Composite**: FundingConfiguration aggregates multiple funding entities
- **Visitor**: FundingModelVisitor enables extensible operations on the model
- **Strategy**: Different funding platforms can have different behaviors
- **Validation**: Centralized validation logic for model consistency
"""
    
    return doc


if __name__ == "__main__":
    # Generate and display the metamodel visualization
    visualizer = MetamodelVisualizer()
    
    print("Generating Funding DSL Metamodel Visualization...")
    print("=" * 50)
    
    # Generate class diagram
    class_diagram = visualizer.generate_class_diagram()
    print("Class Diagram GraphViz Source:")
    print(class_diagram)
    print("\n" + "=" * 50)
    
    # Generate concept map
    concept_map = visualizer.generate_concept_map()
    print("Concept Map GraphViz Source:")
    print(concept_map)
    print("\n" + "=" * 50)
    
    # Generate documentation
    documentation = generate_metamodel_documentation()
    print("Metamodel Documentation:")
    print(documentation) 