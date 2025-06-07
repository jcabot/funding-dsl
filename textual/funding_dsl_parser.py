"""
Funding DSL Parser - Converts textual DSL files to metamodel objects
Uses simplified parsing (would use ANTLR-generated parser in production).
"""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from metamodel.funding_metamodel import (
    FundingConfiguration, Beneficiary, FundingSource, FundingTier, 
    FundingGoal, FundingAmount, FundingPlatform, FundingType, 
    CurrencyType, FundingModelValidator
)


class ParseError(Exception):
    """Raised when there's an error parsing the DSL file"""
    pass


class FundingDSLParser:
    """Parser that converts DSL text to metamodel objects"""
    
    def __init__(self):
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
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_text(content)
        except FileNotFoundError:
            raise ParseError(f"File not found: {file_path}")
        except Exception as e:
            raise ParseError(f"Error reading file {file_path}: {str(e)}")
    
    def parse_text(self, text: str) -> FundingConfiguration:
        """Parse DSL text and return a FundingConfiguration object"""
        try:
            config_data = self._simple_parse(text)
            return self._build_configuration(config_data)
        except Exception as e:
            raise ParseError(f"Parse error: {str(e)}")
    
    def _simple_parse(self, text: str) -> Dict[str, Any]:
        """Simple parser for demonstration - would be replaced by ANTLR parser"""
        
        # Remove comments
        text = re.sub(r'//.*?$', '', text, flags=re.MULTILINE)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        
        # Extract project name
        funding_match = re.search(r'funding\s+"([^"]+)"\s*\{', text)
        if not funding_match:
            raise ParseError("No funding block found")
        
        project_name = funding_match.group(1)
        
        # Extract basic properties
        description = self._extract_string_property(text, 'description')
        currency = self._extract_keyword_property(text, 'currency')
        min_amount = self._extract_number_property(text, 'min_amount')
        max_amount = self._extract_number_property(text, 'max_amount')
        
        # Extract blocks
        beneficiaries = self._extract_beneficiaries(text)
        sources = self._extract_sources(text)
        tiers = self._extract_tiers(text)
        goals = self._extract_goals(text)
        
        return {
            'project_name': project_name,
            'description': description,
            'currency': currency,
            'min_amount': min_amount,
            'max_amount': max_amount,
            'beneficiaries': beneficiaries,
            'sources': sources,
            'tiers': tiers,
            'goals': goals
        }
    
    def _extract_string_property(self, text: str, property_name: str) -> Optional[str]:
        """Extract a string property value"""
        pattern = rf'{property_name}\s+"([^"]+)"'
        match = re.search(pattern, text)
        return match.group(1) if match else None
    
    def _extract_keyword_property(self, text: str, property_name: str) -> Optional[str]:
        """Extract a keyword property value"""
        pattern = rf'{property_name}\s+([A-Z]+)'
        match = re.search(pattern, text)
        return match.group(1) if match else None
    
    def _extract_number_property(self, text: str, property_name: str) -> Optional[float]:
        """Extract a numeric property value"""
        pattern = rf'{property_name}\s+([\d.]+)'
        match = re.search(pattern, text)
        return float(match.group(1)) if match else None
    
    def _extract_balanced_block(self, text: str, block_name: str) -> Optional[str]:
        """Extract a block with balanced braces"""
        pattern = rf'{block_name}\s*\{{'
        match = re.search(pattern, text)
        if not match:
            return None
        
        start_pos = match.end() - 1  # Position of opening brace
        return self._extract_balanced_content(text, start_pos)
    
    def _extract_balanced_content(self, text: str, start_pos: int) -> str:
        """Extract content between balanced braces starting at start_pos"""
        if start_pos >= len(text) or text[start_pos] != '{':
            return ""
        
        brace_count = 0
        pos = start_pos
        
        while pos < len(text):
            if text[pos] == '{':
                brace_count += 1
            elif text[pos] == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[start_pos + 1:pos]  # Content between braces
            pos += 1
        
        return ""  # Unbalanced braces
    
    def _extract_beneficiaries(self, text: str) -> List[Dict[str, Any]]:
        """Extract beneficiaries block"""
        beneficiaries = []
        
        # Find beneficiaries block using balanced braces
        beneficiaries_text = self._extract_balanced_block(text, 'beneficiaries')
        if not beneficiaries_text:
            return beneficiaries
        
        # Find individual beneficiaries
        beneficiary_pattern = r'beneficiary\s+"([^"]+)"\s*\{'
        pos = 0
        while True:
            match = re.search(beneficiary_pattern, beneficiaries_text[pos:])
            if not match:
                break
            
            name = match.group(1)
            start_pos = pos + match.end() - 1  # Position of opening brace
            props_text = self._extract_balanced_content(beneficiaries_text, start_pos)
            
            beneficiary = {
                'name': name,
                'email': self._extract_string_property(props_text, 'email'),
                'github': self._extract_string_property(props_text, 'github'),
                'website': self._extract_string_property(props_text, 'website'),
                'description': self._extract_string_property(props_text, 'description')
            }
            beneficiaries.append(beneficiary)
            
            pos = start_pos + len(props_text) + 2  # Move past this beneficiary
        
        return beneficiaries
    
    def _extract_sources(self, text: str) -> List[Dict[str, Any]]:
        """Extract sources block"""
        sources = []
        
        # Find sources block using balanced braces
        sources_text = self._extract_balanced_block(text, 'sources')
        if not sources_text:
            return sources
        
        # Find all sources (platform and custom)
        all_platforms = ['github_sponsors', 'patreon', 'ko_fi', 'open_collective', 'buy_me_a_coffee', 'liberapay', 'paypal', 'tidelift', 'issuehunt', 'community_bridge', 'polar', 'thanks_dev', 'custom']
        
        for platform in all_platforms:
            pattern = rf'{platform}\s+"([^"]+)"\s*\{{'
            pos = 0
            while True:
                match = re.search(pattern, sources_text[pos:])
                if not match:
                    break
                
                username = match.group(1)
                start_pos = pos + match.end() - 1  # Position of opening brace
                props_text = self._extract_balanced_content(sources_text, start_pos)
                
                source = {
                    'platform': platform,
                    'username': username,
                    'type': self._extract_keyword_property(props_text, 'type'),
                    'active': self._extract_boolean_property(props_text, 'active'),
                    'config': self._extract_config_block(props_text)
                }
                
                if platform == 'custom':
                    source['url'] = self._extract_string_property(props_text, 'url')
                
                sources.append(source)
                pos = start_pos + len(props_text) + 2  # Move past this source
        
        return sources
    
    def _extract_boolean_property(self, text: str, property_name: str) -> Optional[bool]:
        """Extract a boolean property value"""
        pattern = rf'{property_name}\s+(true|false)'
        match = re.search(pattern, text)
        if match:
            return match.group(1) == 'true'
        return None
    
    def _extract_config_block(self, text: str) -> Dict[str, str]:
        """Extract config block as key-value pairs"""
        config = {}
        config_match = re.search(r'config\s*\{(.*?)\}', text, re.DOTALL)
        if config_match:
            config_text = config_match.group(1)
            # Extract key-value pairs
            kv_pattern = r'"([^"]+)"\s+"([^"]+)"'
            for match in re.finditer(kv_pattern, config_text):
                key = match.group(1)
                value = match.group(2)
                config[key] = value
        return config
    
    def _extract_tiers(self, text: str) -> List[Dict[str, Any]]:
        """Extract tiers block"""
        tiers = []
        
        # Find tiers block using balanced braces
        tiers_text = self._extract_balanced_block(text, 'tiers')
        if not tiers_text:
            return tiers
        
        # Find individual tiers
        tier_pattern = r'tier\s+"([^"]+)"\s*\{'
        pos = 0
        while True:
            match = re.search(tier_pattern, tiers_text[pos:])
            if not match:
                break
            
            name = match.group(1)
            start_pos = pos + match.end() - 1  # Position of opening brace
            props_text = self._extract_balanced_content(tiers_text, start_pos)
            
            # Extract amount
            amount_match = re.search(r'amount\s+([\d.]+)\s+([A-Z]+)', props_text)
            amount_value = float(amount_match.group(1)) if amount_match else 0.0
            amount_currency = amount_match.group(2) if amount_match else 'USD'
            
            tier = {
                'name': name,
                'amount': {'value': amount_value, 'currency': amount_currency},
                'description': self._extract_string_property(props_text, 'description'),
                'max_sponsors': self._extract_number_property(props_text, 'max_sponsors'),
                'benefits': self._extract_string_list(props_text, 'benefits')
            }
            tiers.append(tier)
            
            pos = start_pos + len(props_text) + 2  # Move past this tier
        
        return tiers
    
    def _extract_goals(self, text: str) -> List[Dict[str, Any]]:
        """Extract goals block"""
        goals = []
        
        # Find goals block using balanced braces
        goals_text = self._extract_balanced_block(text, 'goals')
        if not goals_text:
            return goals
        
        # Find individual goals
        goal_pattern = r'goal\s+"([^"]+)"\s*\{'
        pos = 0
        while True:
            match = re.search(goal_pattern, goals_text[pos:])
            if not match:
                break
            
            name = match.group(1)
            start_pos = pos + match.end() - 1  # Position of opening brace
            props_text = self._extract_balanced_content(goals_text, start_pos)
            
            # Extract target amount
            target_match = re.search(r'target\s+([\d.]+)\s+([A-Z]+)', props_text)
            target_value = float(target_match.group(1)) if target_match else 0.0
            target_currency = target_match.group(2) if target_match else 'USD'
            
            # Extract current amount
            current_match = re.search(r'current\s+([\d.]+)\s+([A-Z]+)', props_text)
            current_value = float(current_match.group(1)) if current_match else 0.0
            current_currency = current_match.group(2) if current_match else 'USD'
            
            goal = {
                'name': name,
                'target_amount': {'value': target_value, 'currency': target_currency},
                'current_amount': {'value': current_value, 'currency': current_currency},
                'description': self._extract_string_property(props_text, 'description'),
                'deadline': self._extract_string_property(props_text, 'deadline')
            }
            goals.append(goal)
            
            pos = start_pos + len(props_text) + 2  # Move past this goal
        
        return goals
    
    def _extract_string_list(self, text: str, property_name: str) -> List[str]:
        """Extract a string list property"""
        pattern = rf'{property_name}\s*\[(.*?)\]'
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return []
        
        list_text = match.group(1)
        # Extract quoted strings
        string_pattern = r'"([^"]+)"'
        return [m.group(1) for m in re.finditer(string_pattern, list_text)]
    
    def _build_configuration(self, config_data: Dict[str, Any]) -> FundingConfiguration:
        """Build FundingConfiguration object from parsed data"""
        
        # Create the main configuration
        config = FundingConfiguration(
            project_name=config_data['project_name'],
            description=config_data.get('description'),
            preferred_currency=self.currency_mapping.get(
                config_data.get('currency', 'USD'), CurrencyType.USD
            )
        )
        
        # Set amount limits
        if config_data.get('min_amount'):
            config.min_amount = FundingAmount(
                config_data['min_amount'], 
                config.preferred_currency
            )
        
        if config_data.get('max_amount'):
            config.max_amount = FundingAmount(
                config_data['max_amount'], 
                config.preferred_currency
            )
        
        # Add beneficiaries
        for ben_data in config_data.get('beneficiaries', []):
            beneficiary = Beneficiary(
                name=ben_data['name'],
                email=ben_data.get('email'),
                github_username=ben_data.get('github'),
                website=ben_data.get('website'),
                description=ben_data.get('description')
            )
            config.add_beneficiary(beneficiary)
        
        # Add funding sources
        for source_data in config_data.get('sources', []):
            platform = self.platform_mapping.get(
                source_data['platform'], FundingPlatform.CUSTOM
            )
            funding_type = self.funding_type_mapping.get(
                source_data.get('type', 'both'), FundingType.BOTH
            )
            
            source = FundingSource(
                platform=platform,
                username=source_data['username'],
                funding_type=funding_type,
                is_active=source_data.get('active', True),
                custom_url=source_data.get('url'),
                platform_specific_config=source_data.get('config', {})
            )
            config.add_funding_source(source)
        
        # Add tiers
        for tier_data in config_data.get('tiers', []):
            amount_data = tier_data['amount']
            amount = FundingAmount(
                amount_data['value'],
                self.currency_mapping.get(amount_data['currency'], CurrencyType.USD)
            )
            
            tier = FundingTier(
                name=tier_data['name'],
                amount=amount,
                description=tier_data.get('description'),
                benefits=tier_data.get('benefits', []),
                max_sponsors=int(tier_data['max_sponsors']) if tier_data.get('max_sponsors') else None
            )
            config.add_tier(tier)
        
        # Add goals
        for goal_data in config_data.get('goals', []):
            target_data = goal_data['target_amount']
            target_amount = FundingAmount(
                target_data['value'],
                self.currency_mapping.get(target_data['currency'], CurrencyType.USD)
            )
            
            current_data = goal_data['current_amount']
            current_amount = FundingAmount(
                current_data['value'],
                self.currency_mapping.get(current_data['currency'], CurrencyType.USD)
            )
            
            deadline = None
            if goal_data.get('deadline'):
                try:
                    deadline = datetime.strptime(goal_data['deadline'], '%Y-%m-%d')
                except ValueError:
                    pass  # Invalid date format, skip
            
            goal = FundingGoal(
                name=goal_data['name'],
                target_amount=target_amount,
                current_amount=current_amount,
                description=goal_data.get('description'),
                deadline=deadline
            )
            config.add_goal(goal)
        
        return config


def parse_funding_dsl_file(file_path: str) -> FundingConfiguration:
    """Parse a funding DSL file and return a FundingConfiguration object"""
    parser = FundingDSLParser()
    return parser.parse_file(file_path)


def parse_funding_dsl_text(text: str) -> FundingConfiguration:
    """Parse funding DSL text and return a FundingConfiguration object"""
    parser = FundingDSLParser()
    return parser.parse_text(text)


if __name__ == "__main__":
    # Test the parser with the example file
    try:
        config = parse_funding_dsl_file("examples/example_funding.dsl")
        print("✅ Successfully parsed funding DSL file!")
        print(f"Project: {config.project_name}")
        print(f"Description: {config.description}")
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