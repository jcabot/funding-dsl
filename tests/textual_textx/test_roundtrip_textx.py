#!/usr/bin/env python3
"""
Round-trip Test: TextX DSL -> Model -> GitHub YAML -> Comparison
Tests the complete pipeline from TextX parsing to GitHub funding.yml export.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from textual_textx import parse_funding_dsl_file_textx
from export.funding_exporter import FundingExporter

def main():
    print("TextX DSL -> GitHub YAML Round-trip Test")
    print("=" * 50)
    
    # Parse the DSL file (now in same directory)
    test_file = Path(__file__).parent / "test_equivalent.dsl"
    config = parse_funding_dsl_file_textx(str(test_file))
    print(f"PASS: Parsed project: {config.project_name}")
    print(f"   - Sources: {len(config.funding_sources)}")
    
    # Export to GitHub YAML
    exporter = FundingExporter(config)
    generated_yaml = exporter.to_github_funding_yml()
    
    print("\nGenerated YAML:")
    print("-" * 30)
    print(generated_yaml)
    print("-" * 30)
    
    # Read original (from project root)
    original_file = Path(__file__).parent.parent.parent / "TEST-FUNDING.yml"
    with open(original_file, "r") as f:
        original_yaml = f.read()
    
    print("\nOriginal YAML:")
    print("-" * 30)
    print(original_yaml)
    print("-" * 30)
    
    # Compare
    match = generated_yaml.strip() == original_yaml.strip()
    print(f"\nComparison Result: {'PERFECT MATCH!' if match else 'DIFFERENCES FOUND'}")
    
    if match:
        print("Round-trip test PASSED!")
        print("   TextX DSL successfully converts to identical GitHub YAML format")
    else:
        print("Generated differs from original")
        print(f"Generated: {repr(generated_yaml)}")
        print(f"Original:  {repr(original_yaml)}")
    
    return match

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 