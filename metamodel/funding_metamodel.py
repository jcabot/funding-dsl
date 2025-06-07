"""
Funding DSL Metamodel - Abstract Syntax Tree Classes
Represents the core concepts and relationships in a funding/sponsorship management system.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class FundingPlatform(Enum):
    """Enumeration of supported funding platforms"""
    GITHUB_SPONSORS = "github"
    PATREON = "patreon"
    OPEN_COLLECTIVE = "open_collective"
    KO_FI = "ko_fi"
    BUY_ME_A_COFFEE = "buy_me_a_coffee"
    LIBERAPAY = "liberapay"
    PAYPAL = "paypal"
    TIDELIFT = "tidelift"
    ISSUEHUNT = "issuehunt"
    COMMUNITY_BRIDGE = "community_bridge"
    POLAR = "polar"
    THANKS_DEV = "thanks_dev"
    CUSTOM = "custom"


class FundingType(Enum):
    """Types of funding arrangements"""
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    BOTH = "both"


class CurrencyType(Enum):
    """Supported currencies"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"


@dataclass
class FundingAmount:
    """Represents a monetary amount with currency"""
    value: float
    currency: CurrencyType = CurrencyType.USD
    
    def __str__(self) -> str:
        return f"{self.value} {self.currency.value}"


@dataclass
class Beneficiary:
    """Represents an individual or organization that receives funding"""
    name: str
    email: Optional[str] = None
    github_username: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    
    def __str__(self) -> str:
        return self.name


@dataclass
class FundingTier:
    """Represents a sponsorship tier with specific benefits"""
    name: str
    amount: FundingAmount
    description: Optional[str] = None
    benefits: List[str] = field(default_factory=list)
    max_sponsors: Optional[int] = None
    is_active: bool = True
    
    def __str__(self) -> str:
        return f"{self.name} ({self.amount})"


@dataclass
class FundingGoal:
    """Represents a funding milestone or target"""
    name: str
    target_amount: FundingAmount
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    current_amount: FundingAmount = field(default_factory=lambda: FundingAmount(0))
    is_reached: bool = False
    
    @property
    def progress_percentage(self) -> float:
        """Calculate the progress percentage towards the goal"""
        if self.target_amount.value == 0:
            return 0.0
        return min((self.current_amount.value / self.target_amount.value) * 100, 100.0)
    
    def __str__(self) -> str:
        return f"{self.name}: {self.current_amount}/{self.target_amount}"


@dataclass
class FundingSource:
    """Represents a specific funding platform configuration"""
    platform: FundingPlatform
    username: str
    funding_type: FundingType = FundingType.BOTH
    is_active: bool = True
    custom_url: Optional[str] = None  # For custom platforms
    platform_specific_config: Dict[str, str] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return f"{self.platform.value}: {self.username}"


@dataclass
class FundingConfiguration:
    """Main configuration for a project's funding setup"""
    project_name: str
    description: Optional[str] = None
    beneficiaries: List[Beneficiary] = field(default_factory=list)
    funding_sources: List[FundingSource] = field(default_factory=list)
    tiers: List[FundingTier] = field(default_factory=list)
    goals: List[FundingGoal] = field(default_factory=list)
    preferred_currency: CurrencyType = CurrencyType.USD
    min_amount: Optional[FundingAmount] = None
    max_amount: Optional[FundingAmount] = None
    
    def get_active_sources(self) -> List[FundingSource]:
        """Get all active funding sources"""
        return [source for source in self.funding_sources if source.is_active]
    
    def get_active_tiers(self) -> List[FundingTier]:
        """Get all active funding tiers"""
        return [tier for tier in self.tiers if tier.is_active]
    
    def get_unreached_goals(self) -> List[FundingGoal]:
        """Get all goals that haven't been reached yet"""
        return [goal for goal in self.goals if not goal.is_reached]
    
    def add_beneficiary(self, beneficiary: Beneficiary) -> None:
        """Add a beneficiary to the configuration"""
        self.beneficiaries.append(beneficiary)
    
    def add_funding_source(self, source: FundingSource) -> None:
        """Add a funding source to the configuration"""
        self.funding_sources.append(source)
    
    def add_tier(self, tier: FundingTier) -> None:
        """Add a funding tier to the configuration"""
        self.tiers.append(tier)
    
    def add_goal(self, goal: FundingGoal) -> None:
        """Add a funding goal to the configuration"""
        self.goals.append(goal)
    
    def __str__(self) -> str:
        return f"Funding Configuration for {self.project_name}"


class FundingModelVisitor(ABC):
    """Abstract visitor pattern for traversing the funding model"""
    
    @abstractmethod
    def visit_configuration(self, config: FundingConfiguration) -> None:
        pass
    
    @abstractmethod
    def visit_beneficiary(self, beneficiary: Beneficiary) -> None:
        pass
    
    @abstractmethod
    def visit_funding_source(self, source: FundingSource) -> None:
        pass
    
    @abstractmethod
    def visit_tier(self, tier: FundingTier) -> None:
        pass
    
    @abstractmethod
    def visit_goal(self, goal: FundingGoal) -> None:
        pass


class FundingModelValidator:
    """Validates funding model instances for consistency and completeness"""
    
    @staticmethod
    def validate_configuration(config: FundingConfiguration) -> List[str]:
        """Validate a funding configuration and return list of validation errors"""
        errors = []
        
        if not config.project_name:
            errors.append("Project name is required")
        
        if not config.beneficiaries:
            errors.append("At least one beneficiary is required")
        
        if not config.funding_sources:
            errors.append("At least one funding source is required")
        
        # Validate funding sources
        for source in config.funding_sources:
            if not source.username:
                errors.append(f"Username is required for {source.platform.value}")
            
            if source.platform == FundingPlatform.CUSTOM and not source.custom_url:
                errors.append("Custom URL is required for custom platforms")
            
            # Validate Tidelift format: platform-name/package-name
            if source.platform == FundingPlatform.TIDELIFT:
                if '/' not in source.username:
                    errors.append("Tidelift username must be in format 'platform-name/package-name' (e.g., 'npm/package-name')")
                else:
                    platform_name = source.username.split('/')[0]
                    valid_platforms = ['npm', 'pypi', 'rubygems', 'maven', 'packagist', 'nuget']
                    if platform_name not in valid_platforms:
                        errors.append(f"Tidelift platform name must be one of: {', '.join(valid_platforms)}")
            
            # Validate thanks.dev format: u/gh/username
            if source.platform == FundingPlatform.THANKS_DEV:
                if not source.username.startswith('u/gh/'):
                    errors.append("Thanks.dev username must be in format 'u/gh/username'")
        
        # Validate tiers have unique names
        tier_names = [tier.name for tier in config.tiers]
        if len(tier_names) != len(set(tier_names)):
            errors.append("Funding tier names must be unique")
        
        # Validate goals have unique names
        goal_names = [goal.name for goal in config.goals]
        if len(goal_names) != len(set(goal_names)):
            errors.append("Funding goal names must be unique")
        
        return errors
    
    @staticmethod
    def is_valid_configuration(config: FundingConfiguration) -> bool:
        """Check if a configuration is valid"""
        return len(FundingModelValidator.validate_configuration(config)) == 0 