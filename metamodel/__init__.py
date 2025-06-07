"""
Metamodel - Python classes representing the abstract syntax of the Funding DSL.

This module contains the core metamodel classes that define the structure and
relationships of funding configurations.
"""

from .funding_metamodel import (
    FundingConfiguration,
    Beneficiary,
    FundingSource,
    FundingTier,
    FundingGoal,
    FundingAmount,
    FundingPlatform,
    FundingType,
    CurrencyType,
    FundingModelVisitor,
    FundingModelValidator
)

__all__ = [
    'FundingConfiguration',
    'Beneficiary', 
    'FundingSource',
    'FundingTier',
    'FundingGoal',
    'FundingAmount',
    'FundingPlatform',
    'FundingType',
    'CurrencyType',
    'FundingModelVisitor',
    'FundingModelValidator'
] 