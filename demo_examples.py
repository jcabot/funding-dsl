#!/usr/bin/env python3
"""
Comprehensive Examples Demonstration
Shows both minimal and comprehensive funding configurations.
"""

def demonstrate_examples():
    print("🚀 Funding DSL Examples Demonstration")
    print("=" * 45)
    print()
    
    # Import our modules
    from textual.funding_dsl_parser import FundingDSLParser
    from metamodel.funding_metamodel import FundingModelValidator
    
    parser = FundingDSLParser()
    
    # Demonstrate minimal example
    print("1️⃣ MINIMAL EXAMPLE (GitHub funding.yml equivalent)")
    print("-" * 50)
    print("Equivalent to:")
    print("github: [octocat, surftocat]")
    print("patreon: octocat")
    print("tidelift: npm/octo-package")
    print('custom: ["https://www.paypal.me/octocat", octocat.com]')
    print()
    
    try:
        minimal_config = parser.parse_file('examples/minimal_funding.dsl')
        print(f"✅ Parsed: {minimal_config.project_name}")
        print(f"   Beneficiaries: {len(minimal_config.beneficiaries)}")
        print(f"   Funding Sources: {len(minimal_config.funding_sources)}")
        print(f"   Validation: {'✅ Valid' if not FundingModelValidator.validate_configuration(minimal_config) else '❌ Invalid'}")
    except Exception as e:
        print(f"❌ Error parsing minimal example: {e}")
    
    print()
    print("-" * 50)
    print()
    
    # Demonstrate comprehensive example
    print("2️⃣ COMPREHENSIVE EXAMPLE (Full DSL features)")
    print("-" * 50)
    print("Advanced features: tiers, goals, complex metadata")
    print()
    
    try:
        comprehensive_config = parser.parse_file('examples/example_funding.dsl')
        print(f"✅ Parsed: {comprehensive_config.project_name}")
        print(f"   Description: {comprehensive_config.description}")
        print(f"   Beneficiaries: {len(comprehensive_config.beneficiaries)}")
        print(f"   Funding Sources: {len(comprehensive_config.funding_sources)}")
        print(f"   Sponsorship Tiers: {len(comprehensive_config.tiers)}")
        print(f"   Funding Goals: {len(comprehensive_config.goals)}")
        
        # Show tier details
        if comprehensive_config.tiers:
            print("\n   💎 Available Tiers:")
            for tier in comprehensive_config.tiers[:2]:  # Show first 2
                print(f"     • {tier.name}: {tier.amount}")
        
        # Show goal progress
        if comprehensive_config.goals:
            print("\n   🎯 Funding Goals:")
            for goal in comprehensive_config.goals[:2]:  # Show first 2
                print(f"     • {goal.name}: {goal.progress_percentage:.1f}% complete")
        
        errors = FundingModelValidator.validate_configuration(comprehensive_config)
        print(f"\n   Validation: {'✅ Valid' if not errors else '❌ Invalid'}")
        
    except Exception as e:
        print(f"❌ Error parsing comprehensive example: {e}")
    
    print()
    print("-" * 50)
    print()
    
    print("🎯 DSL Benefits Demonstrated:")
    print("  📋 GitHub compatibility - Can represent funding.yml equivalents")
    print("  🏗️  Rich structure - Beneficiaries, tiers, goals, metadata")
    print("  ✅ Validation - Built-in consistency checking")
    print("  🔧 Extensible - Platform-specific configuration support")
    print("  📖 Human-readable - Clear, domain-specific syntax")
    print("  🔄 Bidirectional - Parse text ↔ Generate outputs")
    print()
    
    print("📚 Related Research:")
    print("  This approach follows TCS (Textual Concrete Syntax) principles")
    print("  for bridging metamodels and textual representations in DSLs.")
    print("  Reference: https://staffwww.dcs.shef.ac.uk/people/A.Simons/remodel/papers/Jouault_TextualConcreteSyntaxes.pdf")

if __name__ == "__main__":
    demonstrate_examples() 