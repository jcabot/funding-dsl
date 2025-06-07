# Funding DSL

A Domain-Specific Language (DSL) for open source maintainers to manage GitHub sponsorships and funding configurations.

## Project Structure

This project is organized into 4 development steps, each building upon the previous:

### Step 1: Metamodel (`metamodel/`)
Python classes representing the abstract syntax of the Funding DSL.
- `funding_metamodel.py` - Core metamodel classes and enums
- `metamodel_visualizer.py` - GraphViz visualization generator
- `example_usage.py` - Comprehensive usage examples
- `STEP1_METAMODEL_SUMMARY.md` - Detailed documentation

### Step 2: Textual Syntax and Parser (`textual/`)
ANTLR grammar and Python parser for converting DSL text to metamodel objects.
- `FundingDSL.g4` - ANTLR grammar definition
- `funding_dsl_parser.py` - Python parser implementation
- `funding_dsl_syntax_design.md` - Syntax design documentation
- `demo_step2.py` - Complete parsing demonstration
- `STEP2_PARSER_SUMMARY.md` - Implementation summary

### Graphical Notation & Visual Model Editor (`graphical/`)
Visual modeling tools AND graphical model editor for funding configurations.
- `funding_visualizer.py` - Core visualization engine with Mermaid diagram generation
- `interactive_diagrams.py` - Interactive chart creation and analysis tools
- `graphical_editor.py` - Canvas-based visual model editor with drag-and-drop
- Multiple diagram types: Flowcharts, Pie charts, Timelines, Class diagrams, ASCII art
- Visual model creation with property editors and export capabilities

### Step 4: Export Functionality (`export/`)
Generate GitHub funding.yml files and other output formats.
- `funding_exporter.py` - Core export functionality
- `cli.py` - Command-line interface for exports
- Multiple output formats: GitHub YAML, JSON, Markdown, CSV

## Testing Structure (`tests/`)

Tests are organized by step:
- `tests/metamodel/` - Metamodel tests
- `tests/textual/` - Parser and syntax tests
- `tests/graphical/` - Graphical notation tests
- `tests/export/` - Export functionality tests

## Examples (`examples/`)

Sample DSL files and usage examples:

- `example_funding.dsl` - Comprehensive example with all features
- `minimal_funding.dsl` - Minimal example equivalent to GitHub's funding.yml format

### Minimal Example

Our DSL can represent the same funding configuration as GitHub's YAML format but with richer metadata and structure. For example, this GitHub funding.yml:

```yaml
github: [octocat, surftocat]
patreon: octocat
tidelift: npm/octo-package
custom: ["https://www.paypal.me/octocat", octocat.com]
```

Is equivalent to our DSL syntax in `examples/minimal_funding.dsl`, which includes additional beneficiary information, structured configuration, and validation capabilities.

Run `python demo_minimal_example.py` to see a live demonstration of how the DSL parses and represents this funding configuration.

## Usage

```python
# Import from specific modules
from metamodel import FundingConfiguration, Beneficiary
from textual import FundingDSLParser
from export import FundingExporter

# Parse a DSL file
parser = FundingDSLParser()
config = parser.parse_file('examples/example_funding.dsl')

# Work with the configuration
print(f"Project: {config.project_name}")
for beneficiary in config.beneficiaries:
    print(f"Beneficiary: {beneficiary.name}")

# Export to GitHub funding.yml
exporter = FundingExporter(config)
github_yml = exporter.to_github_funding_yml()
print(github_yml)

# Generate visualizations
from graphical import FundingVisualizer
visualizer = FundingVisualizer(config)
flowchart = visualizer.generate_mermaid_flowchart()
ascii_art = visualizer.generate_ascii_overview()
print(ascii_art)

# Use the graphical model editor
from graphical import GraphicalFundingEditor
editor = GraphicalFundingEditor()
editor.run()  # Launches the visual editor GUI

# Use the enhanced PoN-based visual editor
from graphical.improved_graphical_editor import ImprovedGraphicalFundingEditor
enhanced_editor = ImprovedGraphicalFundingEditor()
enhanced_editor.run()  # Launches enhanced editor with Physics of Notations principles
```

### Command-Line Usage

```bash
# Launch the graphical model editor
python demo_graphical_editor.py

# Launch the enhanced PoN-based visual editor
python demo_improved_graphical_editor.py

# Generate visualizations for existing models
python demo_visualizations.py

# Export to GitHub funding.yml format
python -m export.cli examples/minimal_funding.dsl -f github_yml -o .github/FUNDING.yml

# Export to JSON with validation
python -m export.cli examples/example_funding.dsl -f json --validate --verbose

# Export to Markdown documentation
python -m export.cli examples/example_funding.dsl -f markdown -o FUNDING.md
```

## Development Status

- ✅ **Metamodel**: Metamodel - Complete
- ✅ **Textual**: Textual Syntax & Parser - Complete  
- ✅ **Step 3**: Graphical Notation - Complete
- ✅ **Export**: Export Functionality - Complete
