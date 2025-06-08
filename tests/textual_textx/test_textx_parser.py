#!/usr/bin/env python3
"""
Comprehensive tests for TextX-based Funding DSL Parser
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from textual_textx import (
    FundingDSLTextXParser, 
    parse_funding_dsl_text_textx, 
    parse_funding_dsl_file_textx
)
from metamodel.funding_metamodel import (
    FundingConfiguration, FundingPlatform, FundingType, 
    CurrencyType, FundingModelValidator
)


class TestTextXParser(unittest.TestCase):
    """Test cases for TextX parser functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = FundingDSLTextXParser()
    
    def test_minimal_configuration(self):
        """Test parsing minimal configuration"""
        dsl = '''
        funding "Minimal Project" {
            currency USD
        }
        '''
        
        config = parse_funding_dsl_text_textx(dsl)
        
        self.assertEqual(config.project_name, "Minimal Project")
        self.assertEqual(config.preferred_currency, CurrencyType.USD)
        self.assertIsNone(config.description)
        self.assertEqual(len(config.beneficiaries), 0)
        self.assertEqual(len(config.funding_sources), 0)
        self.assertEqual(len(config.tiers), 0)
        self.assertEqual(len(config.goals), 0)
    
    def test_complete_configuration(self):
        """Test parsing complete configuration with all elements"""
        dsl = '''
        funding "Complete Project" {
            description "A complete test project"
            currency EUR
            min_amount 1.0
            max_amount 1000.0
            
            beneficiaries {
                beneficiary "Alice" {
                    email "alice@test.com"
                    github "alice"
                    website "https://alice.dev"
                    description "Lead developer"
                }
                
                beneficiary "Bob" {
                    github "bob"
                }
            }
            
            sources {
                github_sponsors "alice" {
                    type both
                    active true
                }
                
                patreon "project" {
                    type recurring
                    active true
                    config {
                        "tier_sync" "enabled"
                        "webhook" "https://api.test.com"
                    }
                }
                
                custom "PayPal" {
                    url "https://paypal.me/alice"
                    type one_time
                    active false
                }
            }
            
            tiers {
                tier "Basic" {
                    amount 5.0 EUR
                    description "Basic support"
                    benefits ["Thanks", "Updates"]
                }
                
                tier "Premium" {
                    amount 25.0 EUR
                    description "Premium support"
                    max_sponsors 10
                    benefits ["All basic", "Logo", "Support"]
                }
            }
            
            goals {
                goal "Hosting" {
                    target 100.0 EUR
                    current 50.0 EUR
                    description "Server costs"
                }
                
                goal "Development" {
                    target 500.0 EUR
                    current 0.0 EUR
                    deadline "2024-12-31"
                    description "Feature development"
                }
            }
        }
        '''
        
        config = parse_funding_dsl_text_textx(dsl)
        
        # Test basic configuration
        self.assertEqual(config.project_name, "Complete Project")
        self.assertEqual(config.description, "A complete test project")
        self.assertEqual(config.preferred_currency, CurrencyType.EUR)
        self.assertEqual(config.min_amount.value, 1.0)
        self.assertEqual(config.max_amount.value, 1000.0)
        
        # Test beneficiaries
        self.assertEqual(len(config.beneficiaries), 2)
        alice = config.beneficiaries[0]
        self.assertEqual(alice.name, "Alice")
        self.assertEqual(alice.email, "alice@test.com")
        self.assertEqual(alice.github_username, "alice")
        self.assertEqual(alice.website, "https://alice.dev")
        
        bob = config.beneficiaries[1]
        self.assertEqual(bob.name, "Bob")
        self.assertEqual(bob.github_username, "bob")
        self.assertIsNone(bob.email)
        
        # Test sources
        self.assertEqual(len(config.funding_sources), 3)
        
        github_source = config.funding_sources[0]
        self.assertEqual(github_source.platform, FundingPlatform.GITHUB_SPONSORS)
        self.assertEqual(github_source.username, "alice")
        self.assertEqual(github_source.funding_type, FundingType.BOTH)
        self.assertTrue(github_source.is_active)
        
        patreon_source = config.funding_sources[1]
        self.assertEqual(patreon_source.platform, FundingPlatform.PATREON)
        self.assertEqual(patreon_source.username, "project")
        self.assertEqual(patreon_source.funding_type, FundingType.RECURRING)
        self.assertTrue(patreon_source.is_active)
        self.assertEqual(patreon_source.platform_specific_config["tier_sync"], "enabled")
        
        custom_source = config.funding_sources[2]
        self.assertEqual(custom_source.platform, FundingPlatform.CUSTOM)
        self.assertEqual(custom_source.username, "PayPal")
        self.assertEqual(custom_source.custom_url, "https://paypal.me/alice")
        self.assertEqual(custom_source.funding_type, FundingType.ONE_TIME)
        self.assertFalse(custom_source.is_active)
        
        # Test tiers
        self.assertEqual(len(config.tiers), 2)
        
        basic_tier = config.tiers[0]
        self.assertEqual(basic_tier.name, "Basic")
        self.assertEqual(basic_tier.amount.value, 5.0)
        self.assertEqual(basic_tier.amount.currency, CurrencyType.EUR)
        self.assertEqual(basic_tier.benefits, ["Thanks", "Updates"])
        self.assertIsNone(basic_tier.max_sponsors)
        
        premium_tier = config.tiers[1]
        self.assertEqual(premium_tier.name, "Premium")
        self.assertEqual(premium_tier.amount.value, 25.0)
        self.assertEqual(premium_tier.max_sponsors, 10)
        self.assertEqual(premium_tier.benefits, ["All basic", "Logo", "Support"])
        
        # Test goals
        self.assertEqual(len(config.goals), 2)
        
        hosting_goal = config.goals[0]
        self.assertEqual(hosting_goal.name, "Hosting")
        self.assertEqual(hosting_goal.target_amount.amount, 100.0)
        self.assertEqual(hosting_goal.current_amount.amount, 50.0)
        self.assertIsNone(hosting_goal.deadline)
        
        dev_goal = config.goals[1]
        self.assertEqual(dev_goal.name, "Development")
        self.assertEqual(dev_goal.target_amount.amount, 500.0)
        self.assertEqual(dev_goal.current_amount.amount, 0.0)
        self.assertIsNotNone(dev_goal.deadline)
    
    def test_currency_types(self):
        """Test all supported currency types"""
        currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']
        
        for currency in currencies:
            dsl = f'''
            funding "Currency Test" {{
                currency {currency}
            }}
            '''
            
            config = parse_funding_dsl_text_textx(dsl)
            expected_currency = getattr(CurrencyType, currency)
            self.assertEqual(config.preferred_currency, expected_currency)
    
    def test_platform_types(self):
        """Test all supported platform types"""
        platforms = [
            'github_sponsors', 'patreon', 'ko_fi', 'open_collective',
            'buy_me_a_coffee', 'liberapay', 'paypal', 'tidelift',
            'issuehunt', 'community_bridge', 'polar', 'thanks_dev'
        ]
        
        for platform in platforms:
            dsl = f'''
            funding "Platform Test" {{
                currency USD
                sources {{
                    {platform} "testuser" {{
                        type both
                        active true
                    }}
                }}
            }}
            '''
            
            config = parse_funding_dsl_text_textx(dsl)
            self.assertEqual(len(config.funding_sources), 1)
            
            source = config.funding_sources[0]
            expected_platform = getattr(FundingPlatform, platform.upper())
            self.assertEqual(source.platform, expected_platform)
    
    def test_funding_types(self):
        """Test all supported funding types"""
        funding_types = ['one_time', 'recurring', 'both']
        
        for funding_type in funding_types:
            dsl = f'''
            funding "Funding Type Test" {{
                currency USD
                sources {{
                    github_sponsors "testuser" {{
                        type {funding_type}
                        active true
                    }}
                }}
            }}
            '''
            
            config = parse_funding_dsl_text_textx(dsl)
            source = config.funding_sources[0]
            expected_type = getattr(FundingType, funding_type.upper())
            self.assertEqual(source.funding_type, expected_type)
    
    def test_validation_integration(self):
        """Test integration with validation system"""
        # Valid configuration
        valid_dsl = '''
        funding "Valid Project" {
            currency USD
            min_amount 1.0
            max_amount 100.0
            
            beneficiaries {
                beneficiary "User" {
                    github "user"
                }
            }
            
            sources {
                github_sponsors "user" {
                    type both
                    active true
                }
            }
        }
        '''
        
        config = parse_funding_dsl_text_textx(valid_dsl)
        errors = FundingModelValidator.validate_configuration(config)
        self.assertEqual(len(errors), 0)
        
        # Invalid configuration (min > max)
        invalid_dsl = '''
        funding "Invalid Project" {
            currency USD
            min_amount 100.0
            max_amount 10.0
        }
        '''
        
        config = parse_funding_dsl_text_textx(invalid_dsl)
        errors = FundingModelValidator.validate_configuration(config)
        self.assertGreater(len(errors), 0)
    
    def test_optional_elements(self):
        """Test that optional elements work correctly"""
        # Test beneficiary with only required fields
        dsl = '''
        funding "Optional Test" {
            currency USD
            
            beneficiaries {
                beneficiary "Minimal User" {
                    github "minimal"
                }
            }
            
            sources {
                github_sponsors "minimal" {
                    active true
                }
            }
            
            tiers {
                tier "Basic" {
                    amount 5.0 USD
                }
            }
            
            goals {
                goal "Simple Goal" {
                    target 100.0 USD
                }
            }
        }
        '''
        
        config = parse_funding_dsl_text_textx(dsl)
        
        # Check that optional fields are None/default
        beneficiary = config.beneficiaries[0]
        self.assertIsNone(beneficiary.email)
        self.assertIsNone(beneficiary.website)
        self.assertIsNone(beneficiary.description)
        
        source = config.funding_sources[0]
        self.assertEqual(source.funding_type, FundingType.BOTH)  # default
        
        tier = config.tiers[0]
        self.assertIsNone(tier.description)
        self.assertIsNone(tier.max_sponsors)
        self.assertEqual(tier.benefits, [])
        
        goal = config.goals[0]
        self.assertEqual(goal.current_amount.amount, 0.0)  # default
        self.assertIsNone(goal.deadline)
        self.assertIsNone(goal.description)


if __name__ == '__main__':
    # Create test directory if it doesn't exist
    test_dir = Path(__file__).parent
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2) 