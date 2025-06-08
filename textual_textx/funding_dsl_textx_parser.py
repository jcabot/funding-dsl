"""
TextX-based Funding DSL Parser
Uses TextX grammar to parse DSL files and convert to metamodel objects.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from textx import metamodel_from_file, TextXSyntaxError
from metamodel.funding_metamodel import (
    FundingConfiguration, Beneficiary, FundingSource, FundingTier, 
    FundingGoal, FundingAmount, FundingPlatform, FundingType, 
    CurrencyType, FundingModelValidator
)


class TextXParseError(Exception):
    """Raised when there's an error parsing the DSL file with TextX"""
    pass


class FundingDSLTextXParser:
    """TextX-based parser that converts DSL text to metamodel objects"""
    
    def __init__(self):
        # Load the TextX grammar
        self.grammar_file = Path(__file__).parent / "funding_dsl.tx"
        if not self.grammar_file.exists():
            raise TextXParseError(f"Grammar file not found: {self.grammar_file}")
        
        try:
            self.metamodel = metamodel_from_file(str(self.grammar_file))
        except Exception as e:
            raise TextXParseError(f"Error loading TextX grammar: {e}")
        
        # Mapping dictionaries for enum conversion
        self.platform_mapping = {
            'github_sponsors': FundingPlatform.GITHUB_SPONSORS,
            'patreon': FundingPlatform.PATREON,
            'ko_fi': FundingPlatform.KO_FI,
            'open_collective': FundingPlatform.OPEN_COLLECTIVE,
            'buy_me_a_coffee': FundingPlatform.BUY_ME_A_COFFEE,
            'liberapay': FundingPlatform.LIBERAPAY,
            'paypal': FundingPlatform.PAYPAL,
            'tidelift': FundingPlatform.TIDELIFT,
            'issuehunt': FundingPlatform.ISSUEHUNT,
            'community_bridge': FundingPlatform.COMMUNITY_BRIDGE,
            'polar': FundingPlatform.POLAR,
            'thanks_dev': FundingPlatform.THANKS_DEV,
            'custom': FundingPlatform.CUSTOM
        }
        
        self.funding_type_mapping = {
            'one_time': FundingType.ONE_TIME,
            'recurring': FundingType.RECURRING,
            'both': FundingType.BOTH
        }
        
        self.currency_mapping = {
            'USD': CurrencyType.USD,
            'EUR': CurrencyType.EUR,
            'GBP': CurrencyType.GBP,
            'CAD': CurrencyType.CAD,
            'AUD': CurrencyType.AUD
        }
    
    def parse_file(self, file_path: str) -> FundingConfiguration:
        """Parse a .funding file and return a FundingConfiguration object"""
        try:
            # Parse with TextX
            textx_model = self.metamodel.model_from_file(file_path)
            return self._transform_model(textx_model)
        except FileNotFoundError:
            raise TextXParseError(f"File not found: {file_path}")
        except TextXSyntaxError as e:
            raise TextXParseError(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            raise TextXParseError(f"Error parsing file {file_path}: {str(e)}")
    
    def parse_text(self, text: str) -> FundingConfiguration:
        """Parse DSL text and return a FundingConfiguration object"""
        try:
            # Parse with TextX
            textx_model = self.metamodel.model_from_str(text)
            return self._transform_model(textx_model)
        except TextXSyntaxError as e:
            raise TextXParseError(f"Syntax error: {e}")
        except Exception as e:
            raise TextXParseError(f"Parse error: {str(e)}")
    
    def _transform_model(self, textx_model) -> FundingConfiguration:
        """Transform TextX model object to our metamodel objects"""
        
        # Create the main configuration
        config = FundingConfiguration(
            project_name=self._clean_string(textx_model.name),
            description=self._get_optional_string_value(textx_model.description),
            preferred_currency=self._get_currency(textx_model.currency)
        )
        
        # Set amount limits
        if textx_model.min_amount:
            config.min_amount = FundingAmount(
                textx_model.min_amount.value, 
                config.preferred_currency
            )
        
        if textx_model.max_amount:
            config.max_amount = FundingAmount(
                textx_model.max_amount.value, 
                config.preferred_currency
            )
        
        # Transform beneficiaries
        if textx_model.beneficiaries:
            for ben_elem in textx_model.beneficiaries.beneficiaries:
                beneficiary = self._transform_beneficiary(ben_elem)
                config.add_beneficiary(beneficiary)
        
        # Transform funding sources
        if textx_model.sources:
            for source_elem in textx_model.sources.sources:
                source = self._transform_source(source_elem)
                config.add_funding_source(source)
        
        # Transform tiers
        if textx_model.tiers:
            for tier_elem in textx_model.tiers.tiers:
                tier = self._transform_tier(tier_elem)
                config.add_tier(tier)
        
        # Transform goals
        if textx_model.goals:
            for goal_elem in textx_model.goals.goals:
                goal = self._transform_goal(goal_elem)
                config.add_goal(goal)
        
        return config
    
    def _transform_beneficiary(self, ben_elem) -> Beneficiary:
        """Transform TextX beneficiary element to Beneficiary object"""
        return Beneficiary(
            name=self._clean_string(ben_elem.name),
            email=self._get_optional_string_value(ben_elem.email),
            github_username=self._get_optional_string_value(ben_elem.github),
            website=self._get_optional_string_value(ben_elem.website),
            description=self._get_optional_string_value(ben_elem.description)
        )
    
    def _transform_source(self, source_elem) -> FundingSource:
        """Transform TextX source element to FundingSource object"""
        
        # Handle platform sources vs custom sources
        if hasattr(source_elem, 'platform'):
            # Platform source
            platform = self.platform_mapping.get(source_elem.platform, FundingPlatform.CUSTOM)
            username = self._clean_string(source_elem.username)
            custom_url = None
        else:
            # Custom source
            platform = FundingPlatform.CUSTOM
            username = self._clean_string(source_elem.name)
            custom_url = self._get_optional_string_value(source_elem.url)
        
        # Get funding type
        funding_type = FundingType.BOTH  # default
        if source_elem.type:
            funding_type = self.funding_type_mapping.get(
                source_elem.type.value, FundingType.BOTH
            )
        
        # Get active status
        is_active = True  # default
        if source_elem.active:
            is_active = source_elem.active.value
        
        # Get platform config
        platform_config = {}
        if source_elem.config:
            for config_kv in source_elem.config.configs:
                key = self._clean_string(config_kv.key)
                value = self._clean_string(config_kv.value)
                platform_config[key] = value
        
        return FundingSource(
            platform=platform,
            username=username,
            funding_type=funding_type,
            is_active=is_active,
            custom_url=custom_url,
            platform_specific_config=platform_config
        )
    
    def _transform_tier(self, tier_elem) -> FundingTier:
        """Transform TextX tier element to FundingTier object"""
        
        # Transform amount
        amount = self._transform_amount(tier_elem.amount.amount)
        
        # Get benefits list
        benefits = []
        if tier_elem.benefits:
            benefits = [self._clean_string(benefit) for benefit in tier_elem.benefits.benefits]
        
        # Get max sponsors
        max_sponsors = None
        if tier_elem.max_sponsors:
            max_sponsors = tier_elem.max_sponsors.value
        
        return FundingTier(
            name=self._clean_string(tier_elem.name),
            amount=amount,
            description=self._get_optional_string_value(tier_elem.description),
            benefits=benefits,
            max_sponsors=max_sponsors
        )
    
    def _transform_goal(self, goal_elem) -> FundingGoal:
        """Transform TextX goal element to FundingGoal object"""
        
        # Transform amounts
        target_amount = self._transform_amount(goal_elem.target.amount)
        
        current_amount = FundingAmount(0.0, target_amount.currency)  # default
        if goal_elem.current:
            current_amount = self._transform_amount(goal_elem.current.amount)
        
        # Parse deadline
        deadline = None
        if goal_elem.deadline:
            deadline_str = self._clean_string(goal_elem.deadline.value)
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            except ValueError:
                pass  # Invalid date format, keep as None
        
        return FundingGoal(
            name=self._clean_string(goal_elem.name),
            target_amount=target_amount,
            current_amount=current_amount,
            description=self._get_optional_string_value(goal_elem.description),
            deadline=deadline
        )
    
    def _transform_amount(self, amount_elem) -> FundingAmount:
        """Transform TextX amount element to FundingAmount object"""
        currency = self.currency_mapping.get(amount_elem.currency, CurrencyType.USD)
        return FundingAmount(amount_elem.value, currency)
    
    def _get_currency(self, currency_elem) -> CurrencyType:
        """Get currency type from TextX element"""
        if currency_elem:
            return self.currency_mapping.get(currency_elem.value, CurrencyType.USD)
        return CurrencyType.USD
    
    def _get_optional_string_value(self, elem) -> Optional[str]:
        """Get string value from optional TextX element"""
        if elem:
            return self._clean_string(elem.value)
        return None
    
    def _clean_string(self, s: str) -> str:
        """Remove quotes from string literals"""
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        return s


def parse_funding_dsl_file_textx(file_path: str) -> FundingConfiguration:
    """Parse a funding DSL file using TextX and return a FundingConfiguration object"""
    parser = FundingDSLTextXParser()
    return parser.parse_file(file_path)


def parse_funding_dsl_text_textx(text: str) -> FundingConfiguration:
    """Parse funding DSL text using TextX and return a FundingConfiguration object"""
    parser = FundingDSLTextXParser()
    return parser.parse_text(text)


if __name__ == "__main__":
    # Test the TextX parser
    sample_dsl = '''
    funding "TestProject" {
        description "A test project for TextX parser"
        currency USD
        min_amount 5.0
        max_amount 500.0
        
        beneficiaries {
            beneficiary "Test User" {
                email "test@example.com"
                github "testuser"
                description "Test beneficiary"
            }
        }
        
        sources {
            github_sponsors "testuser" {
                type both
                active true
            }
        }
        
        tiers {
            tier "Basic Support" {
                amount 10.0 USD
                description "Basic monthly support"
                benefits ["Thank you message", "Progress updates"]
            }
        }
        
        goals {
            goal "Server Costs" {
                target 100.0 USD
                current 25.0 USD
                description "Monthly server expenses"
            }
        }
    }
    '''
    
    try:
        parser = FundingDSLTextXParser()
        config = parser.parse_text(sample_dsl)
        print("✅ TextX parsing successful!")
        print(f"Project: {config.project_name}")
        print(f"Description: {config.description}")
        print(f"Currency: {config.preferred_currency.value}")
        print(f"Beneficiaries: {len(config.beneficiaries)}")
        print(f"Sources: {len(config.funding_sources)}")
        print(f"Tiers: {len(config.tiers)}")
        print(f"Goals: {len(config.goals)}")
        
        # Validate the configuration
        errors = FundingModelValidator.validate_configuration(config)
        if errors:
            print("\nValidation errors:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("\n✅ Configuration is valid!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc() 