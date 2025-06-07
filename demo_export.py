#!/usr/bin/env python3
"""
Export Functionality Demonstration
Shows how to export funding configurations to various formats.
"""

import os

def demonstrate_export():
    print("🚀 Funding DSL Export Functionality Demonstration")
    print("=" * 55)
    print()
    
    # Import required modules
    from textual.funding_dsl_parser import FundingDSLParser
    from export import FundingExporter, export_funding_config
    
    # Parse both examples
    parser = FundingDSLParser()
    
    print("📄 Parsing example configurations...")
    minimal_config = parser.parse_file('examples/minimal_funding.dsl')
    comprehensive_config = parser.parse_file('examples/example_funding.dsl')
    print("✅ Both configurations parsed successfully!")
    print()
    
    # Demonstrate exports for minimal example (GitHub compatible)
    print("1️⃣ MINIMAL EXAMPLE EXPORTS")
    print("-" * 40)
    print(f"Project: {minimal_config.project_name}")
    print()
    
    # GitHub funding.yml export
    print("📋 GitHub funding.yml format:")
    print("```yaml")
    exporter = FundingExporter(minimal_config)
    github_yml = exporter.to_github_funding_yml()
    print(github_yml)
    print("```")
    print()
    
    # JSON export
    print("📄 JSON format (excerpt):")
    print("```json")
    json_content = exporter.to_json()
    # Show first 15 lines
    lines = json_content.split('\n')
    for line in lines[:15]:
        print(line)
    if len(lines) > 15:
        print("  ... (truncated)")
    print("```")
    print()
    
    # Demonstrate exports for comprehensive example
    print("2️⃣ COMPREHENSIVE EXAMPLE EXPORTS")
    print("-" * 45)
    print(f"Project: {comprehensive_config.project_name}")
    print()
    
    # Markdown export
    print("📝 Markdown format (excerpt):")
    print("```markdown")
    comp_exporter = FundingExporter(comprehensive_config)
    markdown_content = comp_exporter.to_markdown()
    # Show first 20 lines
    lines = markdown_content.split('\n')
    for line in lines[:20]:
        print(line)
    if len(lines) > 20:
        print("... (truncated)")
    print("```")
    print()
    
    # CSV export
    print("📊 CSV format:")
    print("```csv")
    csv_content = comp_exporter.to_csv()
    print(csv_content)
    print("```")
    print()
    
    # File export demonstration
    print("3️⃣ FILE EXPORT DEMONSTRATION")
    print("-" * 35)
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    formats = [
        ('github_yml', '.github/FUNDING.yml'),
        ('json', 'funding.json'),
        ('markdown', 'FUNDING.md'),
        ('csv', 'funding_sources.csv')
    ]
    
    for format_name, filename in formats:
        output_path = os.path.join(output_dir, filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            export_funding_config(comprehensive_config, format_name, output_path)
            print(f"✅ Exported {format_name}: {output_path}")
        except Exception as e:
            print(f"❌ Failed to export {format_name}: {e}")
    
    print()
    
    # CLI demonstration
    print("4️⃣ COMMAND-LINE INTERFACE")
    print("-" * 30)
    print("Available CLI commands:")
    print()
    print("# Export minimal example to GitHub funding.yml")
    print("python -m export.cli examples/minimal_funding.dsl -f github_yml -o .github/FUNDING.yml")
    print()
    print("# Export comprehensive example to JSON with validation")
    print("python -m export.cli examples/example_funding.dsl -f json --validate --verbose")
    print()
    print("# Export to Markdown documentation")
    print("python -m export.cli examples/example_funding.dsl -f markdown -o FUNDING.md")
    print()
    
    # Summary
    print("🎯 EXPORT CAPABILITIES SUMMARY")
    print("-" * 35)
    print("✅ GitHub funding.yml - Direct compatibility with GitHub Sponsors")
    print("✅ JSON - API-friendly structured data")
    print("✅ Markdown - Human-readable documentation")
    print("✅ CSV - Spreadsheet analysis of funding sources")
    print("✅ CLI - Command-line export tool")
    print("✅ Validation - Built-in configuration checking")
    print("✅ Automation ready - Integrate into CI/CD pipelines")
    print()
    
    print("🔄 WORKFLOW INTEGRATION")
    print("-" * 25)
    print("1. Write funding configuration in DSL")
    print("2. Validate configuration")
    print("3. Export to GitHub funding.yml")
    print("4. Generate documentation (Markdown)")
    print("5. Create data exports (JSON/CSV)")
    print("6. Automate with CI/CD")

if __name__ == "__main__":
    demonstrate_export() 