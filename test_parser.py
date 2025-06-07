"""
Test the funding DSL parser step by step
"""

from funding_dsl_parser import parse_funding_dsl_file, FundingDSLParser
from funding_metamodel import FundingModelValidator

def test_parser():
    print("Testing Funding DSL Parser...")
    
    try:
        # Test parsing
        config = parse_funding_dsl_file("examples/example_funding.dsl")
        
        print(f"✅ Successfully parsed funding DSL file!")
        print(f"Project: '{config.project_name}'")
        print(f"Description: '{config.description}'")
        print(f"Currency: {config.preferred_currency}")
        print(f"Min amount: {config.min_amount}")
        print(f"Max amount: {config.max_amount}")
        print()
        
        print(f"Beneficiaries ({len(config.beneficiaries)}):")
        for i, ben in enumerate(config.beneficiaries):
            print(f"  {i+1}. {ben.name}")
            if ben.github_username:
                print(f"     GitHub: @{ben.github_username}")
            if ben.email:
                print(f"     Email: {ben.email}")
        print()
        
        print(f"Funding Sources ({len(config.funding_sources)}):")
        for i, source in enumerate(config.funding_sources):
            print(f"  {i+1}. {source.platform.value}: {source.username}")
            print(f"     Type: {source.funding_type.value}")
            print(f"     Active: {source.is_active}")
        print()
        
        print(f"Sponsorship Tiers ({len(config.tiers)}):")
        for i, tier in enumerate(config.tiers):
            print(f"  {i+1}. {tier.name}: {tier.amount}")
            if tier.description:
                print(f"     {tier.description}")
            if tier.benefits:
                print(f"     Benefits: {len(tier.benefits)} items")
        print()
        
        print(f"Funding Goals ({len(config.goals)}):")
        for i, goal in enumerate(config.goals):
            print(f"  {i+1}. {goal.name}: {goal.current_amount}/{goal.target_amount}")
            print(f"     Progress: {goal.progress_percentage:.1f}%")
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
    test_parser() 