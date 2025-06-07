#!/usr/bin/env python3

print("=== File Parsing Test ===")

try:
    print("1. Importing modules...")
    from textual.funding_dsl_parser import parse_funding_dsl_file
    from metamodel.funding_metamodel import FundingModelValidator
    print("   ✅ Imports successful")
    
    print("2. Reading and parsing file...")
    config = parse_funding_dsl_file("examples/example_funding.dsl")
    print("   ✅ File parsed successfully!")
    
    print("3. Checking basic properties...")
    print(f"   Project: {config.project_name}")
    print(f"   Description: {config.description}")
    print(f"   Currency: {config.preferred_currency}")
    print(f"   Min amount: {config.min_amount}")
    print(f"   Max amount: {config.max_amount}")
    
    print("4. Checking collections...")
    print(f"   Beneficiaries: {len(config.beneficiaries)}")
    for i, ben in enumerate(config.beneficiaries):
        print(f"     {i+1}. {ben.name} (@{ben.github_username})")
    
    print(f"   Sources: {len(config.funding_sources)}")
    for i, source in enumerate(config.funding_sources):
        print(f"     {i+1}. {source.platform.value}: {source.username}")
    
    print(f"   Tiers: {len(config.tiers)}")
    for i, tier in enumerate(config.tiers):
        print(f"     {i+1}. {tier.name}: {tier.amount}")
    
    print(f"   Goals: {len(config.goals)}")
    for i, goal in enumerate(config.goals):
        print(f"     {i+1}. {goal.name}: {goal.progress_percentage:.1f}%")
    
    print("5. Validating configuration...")
    errors = FundingModelValidator.validate_configuration(config)
    if errors:
        print("   ❌ Validation errors:")
        for error in errors:
            print(f"     - {error}")
    else:
        print("   ✅ Configuration is valid!")
    
    print("=== Test Completed Successfully ===")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("=== Test Failed ===") 