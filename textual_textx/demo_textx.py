#!/usr/bin/env python3
"""
Demo script for TextX-based Funding DSL Parser

This script demonstrates the capabilities of the TextX parser implementation
and compares it with the ANTLR-based parser.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from textual_textx import FundingDSLTextXParser, parse_funding_dsl_text_textx
from metamodel.funding_metamodel import FundingModelValidator


def demo_textx_parser():
    """Demonstrate TextX parser capabilities"""
    
    print("🚀 TextX-based Funding DSL Parser Demo")
    print("=" * 50)
    
    # Sample DSL text
    sample_dsl = '''
    funding "TextX Demo Project" {
        description "Demonstrating TextX grammar parsing capabilities"
        currency EUR
        min_amount 2.0
        max_amount 250.0
        
        beneficiaries {
            beneficiary "Demo User" {
                email "demo@example.com"
                github "demouser"
                website "https://demo.example.com"
                description "Demo project maintainer"
            }
        }
        
        sources {
            github_sponsors "demouser" {
                type both
                active true
            }
            
            patreon "demo-project" {
                type recurring
                active true
                config {
                    "tier_sync" "enabled"
                    "webhook_url" "https://api.demo.com/webhook"
                }
            }
        }
        
        tiers {
            tier "Supporter" {
                amount 10.0 EUR
                description "Basic support tier"
                benefits [
                    "Thank you message",
                    "Project updates"
                ]
            }
            
            tier "Sponsor" {
                amount 50.0 EUR
                description "Premium sponsorship"
                max_sponsors 20
                benefits [
                    "All Supporter benefits",
                    "Logo in README",
                    "Priority support"
                ]
            }
        }
        
        goals {
            goal "Hosting Costs" {
                target 100.0 EUR
                current 45.0 EUR
                description "Monthly server hosting expenses"
            }
            
            goal "Feature Development" {
                target 500.0 EUR
                current 120.0 EUR
                deadline "2024-08-01"
                description "Implement advanced features"
            }
        }
    }
    '''
    
    try:
        print("📝 Parsing DSL text...")
        config = parse_funding_dsl_text_textx(sample_dsl)
        
        print("✅ Parsing successful!")
        print()
        
        # Display configuration details
        print("📊 Configuration Details:")
        print(f"  Project Name: {config.project_name}")
        print(f"  Description: {config.description}")
        print(f"  Currency: {config.preferred_currency.value}")
        print(f"  Amount Range: {config.min_amount} - {config.max_amount}")
        print()
        
        # Display beneficiaries
        print("👥 Beneficiaries:")
        for ben in config.beneficiaries:
            print(f"  • {ben.name}")
            print(f"    Email: {ben.email}")
            print(f"    GitHub: @{ben.github_username}")
            print(f"    Website: {ben.website}")
            print(f"    Description: {ben.description}")
        print()
        
        # Display funding sources
        print("💰 Funding Sources:")
        for source in config.funding_sources:
            print(f"  • {source.platform.value}: {source.username}")
            print(f"    Type: {source.funding_type.value}")
            print(f"    Active: {source.is_active}")
            if source.platform_specific_config:
                print(f"    Config: {source.platform_specific_config}")
        print()
        
        # Display tiers
        print("🎯 Sponsorship Tiers:")
        for tier in config.tiers:
            print(f"  • {tier.name}: {tier.amount}")
            print(f"    Description: {tier.description}")
            if tier.max_sponsors:
                print(f"    Max Sponsors: {tier.max_sponsors}")
            if tier.benefits:
                print(f"    Benefits: {', '.join(tier.benefits)}")
        print()
        
        # Display goals
        print("🎯 Funding Goals:")
        for goal in config.goals:
            progress = (goal.current_amount.amount / goal.target_amount.amount) * 100
            print(f"  • {goal.name}")
            print(f"    Progress: {goal.current_amount} / {goal.target_amount} ({progress:.1f}%)")
            print(f"    Description: {goal.description}")
            if goal.deadline:
                print(f"    Deadline: {goal.deadline.strftime('%Y-%m-%d')}")
        print()
        
        # Validate configuration
        print("🔍 Validation:")
        errors = FundingModelValidator.validate_configuration(config)
        if errors:
            print("❌ Validation errors found:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ Configuration is valid!")
        print()
        
        # Demonstrate visitor pattern
        print("🔄 Using Visitor Pattern:")
        from metamodel.funding_metamodel import FundingConfigurationVisitor
        
        class SummaryVisitor(FundingConfigurationVisitor):
            def __init__(self):
                self.summary = {
                    'total_tiers': 0,
                    'total_goals': 0,
                    'total_target': 0.0,
                    'total_current': 0.0,
                    'active_sources': 0
                }
            
            def visit_tier(self, tier):
                self.summary['total_tiers'] += 1
            
            def visit_goal(self, goal):
                self.summary['total_goals'] += 1
                self.summary['total_target'] += goal.target_amount.amount
                self.summary['total_current'] += goal.current_amount.amount
            
            def visit_source(self, source):
                if source.is_active:
                    self.summary['active_sources'] += 1
        
        visitor = SummaryVisitor()
        config.accept(visitor)
        
        print(f"  Total Tiers: {visitor.summary['total_tiers']}")
        print(f"  Total Goals: {visitor.summary['total_goals']}")
        print(f"  Total Target Amount: {visitor.summary['total_target']} {config.preferred_currency.value}")
        print(f"  Total Current Amount: {visitor.summary['total_current']} {config.preferred_currency.value}")
        print(f"  Active Sources: {visitor.summary['active_sources']}")
        
        overall_progress = (visitor.summary['total_current'] / visitor.summary['total_target']) * 100
        print(f"  Overall Progress: {overall_progress:.1f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def compare_parsers():
    """Compare TextX parser with ANTLR parser"""
    
    print("\n" + "=" * 50)
    print("🔄 Parser Comparison")
    print("=" * 50)
    
    simple_dsl = '''
    funding "Comparison Test" {
        description "Testing both parsers"
        currency USD
        
        beneficiaries {
            beneficiary "Test User" {
                github "testuser"
            }
        }
        
        sources {
            github_sponsors "testuser" {
                type both
                active true
            }
        }
    }
    '''
    
    try:
        # Test TextX parser
        print("🔧 Testing TextX Parser...")
        textx_config = parse_funding_dsl_text_textx(simple_dsl)
        print(f"✅ TextX: {textx_config.project_name} - {len(textx_config.beneficiaries)} beneficiaries")
        
        # Test ANTLR parser (if available)
        try:
            from textual.funding_dsl_parser import parse_funding_dsl_text
            print("🔧 Testing ANTLR Parser...")
            antlr_config = parse_funding_dsl_text(simple_dsl)
            print(f"✅ ANTLR: {antlr_config.project_name} - {len(antlr_config.beneficiaries)} beneficiaries")
            
            # Compare results
            print("\n📊 Comparison Results:")
            print(f"  Project Names Match: {textx_config.project_name == antlr_config.project_name}")
            print(f"  Beneficiary Count Match: {len(textx_config.beneficiaries) == len(antlr_config.beneficiaries)}")
            print(f"  Source Count Match: {len(textx_config.funding_sources) == len(antlr_config.funding_sources)}")
            
        except ImportError:
            print("⚠️  ANTLR parser not available for comparison")
        
    except Exception as e:
        print(f"❌ Comparison error: {e}")


def demo_grammar_features():
    """Demonstrate specific TextX grammar features"""
    
    print("\n" + "=" * 50)
    print("📝 TextX Grammar Features Demo")
    print("=" * 50)
    
    # Test optional elements
    minimal_dsl = '''
    funding "Minimal Config" {
        currency USD
    }
    '''
    
    print("🧪 Testing minimal configuration...")
    try:
        config = parse_funding_dsl_text_textx(minimal_dsl)
        print(f"✅ Minimal config parsed: {config.project_name}")
    except Exception as e:
        print(f"❌ Minimal config failed: {e}")
    
    # Test complex configuration
    complex_dsl = '''
    funding "Complex Config" {
        description "Testing all features"
        currency GBP
        min_amount 1.0
        max_amount 1000.0
        
        beneficiaries {
            beneficiary "User 1" {
                email "user1@test.com"
                github "user1"
                website "https://user1.com"
                description "First user"
            }
            beneficiary "User 2" {
                github "user2"
            }
        }
        
        sources {
            github_sponsors "user1" {
                type both
                active true
                config {
                    "key1" "value1"
                    "key2" "value2"
                }
            }
            custom "Custom Source" {
                url "https://custom.com/donate"
                type one_time
                active false
            }
        }
        
        tiers {
            tier "Basic" {
                amount 5.0 GBP
                description "Basic tier"
                benefits ["Benefit 1", "Benefit 2"]
            }
            tier "Premium" {
                amount 25.0 GBP
                description "Premium tier"
                max_sponsors 10
                benefits ["All basic", "Premium feature"]
            }
        }
        
        goals {
            goal "Goal 1" {
                target 100.0 GBP
                current 50.0 GBP
                description "First goal"
            }
            goal "Goal 2" {
                target 500.0 GBP
                current 0.0 GBP
                deadline "2024-12-31"
                description "Second goal"
            }
        }
    }
    '''
    
    print("🧪 Testing complex configuration...")
    try:
        config = parse_funding_dsl_text_textx(complex_dsl)
        print(f"✅ Complex config parsed: {config.project_name}")
        print(f"  - {len(config.beneficiaries)} beneficiaries")
        print(f"  - {len(config.funding_sources)} sources")
        print(f"  - {len(config.tiers)} tiers")
        print(f"  - {len(config.goals)} goals")
        
        # Validate
        errors = FundingModelValidator.validate_configuration(config)
        if errors:
            print(f"  ⚠️  {len(errors)} validation errors")
        else:
            print("  ✅ All validations passed")
            
    except Exception as e:
        print(f"❌ Complex config failed: {e}")


if __name__ == "__main__":
    demo_textx_parser()
    compare_parsers()
    demo_grammar_features()
    
    print("\n" + "=" * 50)
    print("🎉 TextX Demo Complete!")
    print("=" * 50) 