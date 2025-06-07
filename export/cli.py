#!/usr/bin/env python3
"""
Command-line interface for funding DSL export functionality.
"""

import argparse
import sys
from pathlib import Path
from textual.funding_dsl_parser import FundingDSLParser
from .funding_exporter import export_funding_config


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Export funding DSL configurations to various formats",
        prog="funding-export"
    )
    
    parser.add_argument(
        'input_file',
        help='Input DSL file (.dsl)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['github_yml', 'json', 'markdown', 'csv'],
        default='github_yml',
        help='Output format (default: github_yml)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate configuration before export'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Check input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        return 1
    
    try:
        # Parse the DSL file
        if args.verbose:
            print(f"Parsing DSL file: {args.input_file}")
        
        dsl_parser = FundingDSLParser()
        config = dsl_parser.parse_file(args.input_file)
        
        if args.verbose:
            print(f"✅ Successfully parsed: {config.project_name}")
            print(f"   Beneficiaries: {len(config.beneficiaries)}")
            print(f"   Funding Sources: {len(config.funding_sources)}")
            print(f"   Tiers: {len(config.tiers)}")
            print(f"   Goals: {len(config.goals)}")
        
        # Validate if requested
        if args.validate:
            from metamodel.funding_metamodel import FundingModelValidator
            errors = FundingModelValidator.validate_configuration(config)
            if errors:
                print("❌ Validation errors:", file=sys.stderr)
                for error in errors:
                    print(f"  - {error}", file=sys.stderr)
                return 1
            elif args.verbose:
                print("✅ Configuration is valid")
        
        # Export to requested format
        if args.verbose:
            print(f"Exporting to format: {args.format}")
        
        content = export_funding_config(config, args.format, args.output)
        
        # Output to stdout if no output file specified
        if not args.output:
            print(content)
        elif args.verbose:
            print(f"✅ Exported to: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 