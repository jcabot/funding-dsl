#!/usr/bin/env python3
"""
Step 2 Demonstration - Textual Syntax and Parser
Shows the complete functionality of the Funding DSL parser.
"""

def demonstrate_step2():
    print("🚀 Funding DSL - Step 2 Demonstration")
    print("=" * 50)
    
    # Import our modules
    from textual.funding_dsl_parser import FundingDSLParser
    from metamodel.funding_metamodel import FundingModelValidator
    
    # Create a sample DSL configuration
    sample_dsl = '''
    // Sample Funding Configuration
    funding "MyAwesomeProject" {
        description "An innovative open source project"
        currency USD
        min_amount 5.00
        max_amount 500.00
        
        beneficiaries {
            beneficiary "Jane Developer" {
                email "jane@example.com"
                github "janedev"
                description "Project lead and main developer"
            }
        }
        
        sources {
            github_sponsors "janedev" {
                type both
                active true
            }
            
            ko_fi "janedev" {
                type one_time
            }
        }
        
        tiers {
            tier "Coffee Supporter" {
                amount 5.00 USD
                description "Buy me a coffee"
                benefits [
                    "Thank you message",
                    "Name in contributors list"
                ]
            }
            
            tier "Monthly Backer" {
                amount 25.00 USD
                description "Monthly support"
                benefits [
                    "All Coffee tier benefits",
                    "Early access to features",
                    "Monthly updates"
                ]
            }
        }
        
        goals {
            goal "Server Costs" {
                target 100.00 USD
                current 45.00 USD
                description "Cover monthly hosting expenses"
            }
        }
    }
    '''
    
    print("📝 Sample DSL Configuration:")
    print("-" * 30)
    print(sample_dsl.strip())
    print()
    
    print("🔧 Parsing DSL...")
    parser = FundingDSLParser()
    config = parser.parse_text(sample_dsl)
    print("✅ Parsing successful!")
    print()
    
    print("📊 Parsed Configuration:")
    print("-" * 30)
    print(f"Project: {config.project_name}")
    print(f"Description: {config.description}")
    print(f"Currency: {config.preferred_currency.value}")
    print(f"Amount range: {config.min_amount} - {config.max_amount}")
    print()
    
    print(f"👥 Beneficiaries ({len(config.beneficiaries)}):")
    for ben in config.beneficiaries:
        print(f"  • {ben.name} (@{ben.github_username})")
        print(f"    {ben.description}")
    print()
    
    print(f"💰 Funding Sources ({len(config.funding_sources)}):")
    for source in config.funding_sources:
        print(f"  • {source.platform.value}: {source.username}")
        print(f"    Type: {source.funding_type.value}, Active: {source.is_active}")
    print()
    
    print(f"🎯 Sponsorship Tiers ({len(config.tiers)}):")
    for tier in config.tiers:
        print(f"  • {tier.name}: {tier.amount}")
        print(f"    {tier.description}")
        print(f"    Benefits: {len(tier.benefits)} items")
    print()
    
    print(f"📈 Funding Goals ({len(config.goals)}):")
    for goal in config.goals:
        print(f"  • {goal.name}: {goal.current_amount}/{goal.target_amount}")
        print(f"    Progress: {goal.progress_percentage:.1f}%")
        print(f"    {goal.description}")
    print()
    
    print("✅ Validation:")
    errors = FundingModelValidator.validate_configuration(config)
    if errors:
        print("❌ Validation errors found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration is completely valid!")
    print()
    
    print("🎉 Step 2 Features Demonstrated:")
    print("  ✅ User-friendly textual syntax")
    print("  ✅ Complete ANTLR grammar")
    print("  ✅ Robust Python parser")
    print("  ✅ Seamless metamodel integration")
    print("  ✅ Error handling and validation")
    print("  ✅ Support for all funding features")
    print()
    
    print("🔄 Ready for Step 3: Graphical notation and modeling environment!")

if __name__ == "__main__":
    demonstrate_step2() 