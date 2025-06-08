#!/usr/bin/env python3
"""
Test script for TextX parser implementation
"""

from textual_textx import parse_funding_dsl_file_textx
from metamodel.funding_metamodel import FundingModelValidator

def test_textx_parser():
    print("🚀 Testing TextX Parser")
    print("=" * 40)
    
    try:
        # Parse the example file
        config = parse_funding_dsl_file_textx('textual_textx/example_funding_clean.dsl')
        
        print("✅ Parsing successful!")
        print(f"Project: {config.project_name}")
        print(f"Description: {config.description}")
        print(f"Currency: {config.preferred_currency.value}")
        print(f"Beneficiaries: {len(config.beneficiaries)}")
        print(f"Sources: {len(config.funding_sources)}")
        print(f"Tiers: {len(config.tiers)}")
        print(f"Goals: {len(config.goals)}")
        print()
        
        # Show details
        print("📊 Details:")
        for ben in config.beneficiaries:
            print(f"  Beneficiary: {ben.name} (@{ben.github_username})")
        
        for source in config.funding_sources:
            print(f"  Source: {source.platform.value} - {source.username}")
        
        for tier in config.tiers:
            print(f"  Tier: {tier.name} - {tier.amount}")
        
        for goal in config.goals:
            print(f"  Goal: {goal.name} - {goal.current_amount}/{goal.target_amount}")
        
        print()
        
        # Validate
        errors = FundingModelValidator.validate_configuration(config)
        if errors:
            print("❌ Validation errors:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ Configuration is valid!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_textx_parser() 