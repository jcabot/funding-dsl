"""
Textual Syntax and Parser - ANTLR grammar and Python parser for the Funding DSL.

This module contains the textual syntax definition and parser implementation
that converts DSL text files into metamodel objects.
"""

from .funding_dsl_parser import FundingDSLParser

__all__ = [
    'FundingDSLParser'
] 