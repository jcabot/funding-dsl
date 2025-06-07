"""
Tests for the core Graphical Model Editor functionality (without GUI)
"""

import unittest
import tempfile
import os
import json
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from graphical.graphical_editor import (
    ProjectElement, BeneficiaryElement, FundingSourceElement, 
    FundingTierElement, FundingGoalElement
)
from metamodel.funding_metamodel import (
    FundingConfiguration, FundingPlatform, FundingType, CurrencyType
)


class MockCanvas:
    """Mock canvas for testing"""
    def __init__(self):
        self.items = []
        self.next_id = 1
        
    def create_rectangle(self, *args, **kwargs):
        id = self.next_id
        self.next_id += 1
        self.items.append(('rectangle', id, args, kwargs))
        return id
        
    def create_text(self, *args, **kwargs):
        id = self.next_id
        self.next_id += 1
        self.items.append(('text', id, args, kwargs))
        return id
        
    def move(self, id, dx, dy):
        pass
        
    def delete(self, id):
        pass
        
    def itemconfig(self, id, **kwargs):
        pass


class TestVisualElements(unittest.TestCase):
    """Test visual element classes"""
    
    def setUp(self):
        self.canvas = MockCanvas()
        
    def test_project_element_creation(self):
        """Test creating a project element"""
        element = ProjectElement(self.canvas, 100, 100)
        element.project_name = "Test Project"
        element.description = "A test project"
        element.preferred_currency = CurrencyType.USD
        
        element.draw()
        
        self.assertEqual(element.x, 100)
        self.assertEqual(element.y, 100)
        self.assertEqual(element.project_name, "Test Project")
        self.assertIsNotNone(element.canvas_id)
        self.assertIsNotNone(element.text_id)
        
    def test_beneficiary_element_creation(self):
        """Test creating a beneficiary element"""
        element = BeneficiaryElement(self.canvas, 200, 200)
        element.name = "John Doe"
        element.email = "john@example.com"
        element.github_username = "johndoe"
        
        element.draw()
        
        self.assertEqual(element.name, "John Doe")
        self.assertEqual(element.email, "john@example.com")
        self.assertEqual(element.github_username, "johndoe")
        
        # Test metamodel conversion
        beneficiary = element.to_metamodel_object()
        self.assertEqual(beneficiary.name, "John Doe")
        self.assertEqual(beneficiary.email, "john@example.com")
        self.assertEqual(beneficiary.github_username, "johndoe")
        
    def test_funding_source_element_creation(self):
        """Test creating a funding source element"""
        element = FundingSourceElement(self.canvas, 300, 300)
        element.platform = FundingPlatform.GITHUB_SPONSORS
        element.username = "testuser"
        element.funding_type = FundingType.RECURRING
        
        element.draw()
        
        self.assertEqual(element.platform, FundingPlatform.GITHUB_SPONSORS)
        self.assertEqual(element.username, "testuser")
        self.assertEqual(element.funding_type, FundingType.RECURRING)
        
        # Test metamodel conversion
        source = element.to_metamodel_object()
        self.assertEqual(source.platform, FundingPlatform.GITHUB_SPONSORS)
        self.assertEqual(source.username, "testuser")
        self.assertEqual(source.funding_type, FundingType.RECURRING)
        
    def test_funding_tier_element_creation(self):
        """Test creating a funding tier element"""
        element = FundingTierElement(self.canvas, 400, 400)
        element.name = "Supporter"
        element.amount = 25.0
        element.currency = CurrencyType.USD
        element.description = "Monthly support"
        element.benefits = ["Thanks", "Updates"]
        
        element.draw()
        
        self.assertEqual(element.name, "Supporter")
        self.assertEqual(element.amount, 25.0)
        self.assertEqual(element.currency, CurrencyType.USD)
        
        # Test metamodel conversion
        tier = element.to_metamodel_object()
        self.assertEqual(tier.name, "Supporter")
        self.assertEqual(tier.amount.value, 25.0)
        self.assertEqual(tier.amount.currency, CurrencyType.USD)
        self.assertEqual(tier.benefits, ["Thanks", "Updates"])
        
    def test_funding_goal_element_creation(self):
        """Test creating a funding goal element"""
        element = FundingGoalElement(self.canvas, 500, 500)
        element.name = "Server Costs"
        element.target_amount = 1000.0
        element.current_amount = 250.0
        element.currency = CurrencyType.USD
        
        element.draw()
        
        self.assertEqual(element.name, "Server Costs")
        self.assertEqual(element.target_amount, 1000.0)
        self.assertEqual(element.current_amount, 250.0)
        
        # Test metamodel conversion
        goal = element.to_metamodel_object()
        self.assertEqual(goal.name, "Server Costs")
        self.assertEqual(goal.target_amount.value, 1000.0)
        self.assertEqual(goal.current_amount.value, 250.0)
        self.assertEqual(goal.progress_percentage, 25.0)
        
    def test_element_movement(self):
        """Test moving elements"""
        element = BeneficiaryElement(self.canvas, 100, 100)
        element.draw()
        
        original_x, original_y = element.x, element.y
        element.move(50, 30)
        
        self.assertEqual(element.x, original_x + 50)
        self.assertEqual(element.y, original_y + 30)
        
    def test_point_containment(self):
        """Test point containment checking"""
        element = BeneficiaryElement(self.canvas, 100, 100)
        
        # Point inside element
        self.assertTrue(element.contains_point(150, 130))
        
        # Point outside element
        self.assertFalse(element.contains_point(50, 50))
        self.assertFalse(element.contains_point(250, 250))
        
    def test_selection_state(self):
        """Test selection state management"""
        element = BeneficiaryElement(self.canvas, 100, 100)
        element.draw()
        
        self.assertFalse(element.selected)
        
        element.set_selected(True)
        self.assertTrue(element.selected)
        
        element.set_selected(False)
        self.assertFalse(element.selected)


class TestModelCreation(unittest.TestCase):
    """Test creating funding configurations from visual elements"""
    
    def setUp(self):
        self.canvas = MockCanvas()
        
    def test_create_funding_configuration(self):
        """Test creating a funding configuration from visual elements"""
        # Create visual elements
        project = ProjectElement(self.canvas, 100, 100)
        project.project_name = "Test Project"
        project.description = "A test project"
        
        beneficiary = BeneficiaryElement(self.canvas, 200, 200)
        beneficiary.name = "John Doe"
        beneficiary.email = "john@example.com"
        
        source = FundingSourceElement(self.canvas, 300, 300)
        source.platform = FundingPlatform.GITHUB_SPONSORS
        source.username = "johndoe"
        
        tier = FundingTierElement(self.canvas, 400, 400)
        tier.name = "Supporter"
        tier.amount = 25.0
        
        goal = FundingGoalElement(self.canvas, 500, 500)
        goal.name = "Server Costs"
        goal.target_amount = 1000.0
        goal.current_amount = 250.0
        
        # Create configuration manually (simulating what the editor would do)
        config = FundingConfiguration(
            project_name=project.project_name,
            description=project.description,
            preferred_currency=project.preferred_currency
        )
        
        config.add_beneficiary(beneficiary.to_metamodel_object())
        config.add_funding_source(source.to_metamodel_object())
        config.add_tier(tier.to_metamodel_object())
        config.add_goal(goal.to_metamodel_object())
        
        # Verify configuration
        self.assertEqual(config.project_name, "Test Project")
        self.assertEqual(len(config.beneficiaries), 1)
        self.assertEqual(len(config.funding_sources), 1)
        self.assertEqual(len(config.tiers), 1)
        self.assertEqual(len(config.goals), 1)
        
        # Verify specific elements
        self.assertEqual(config.beneficiaries[0].name, "John Doe")
        self.assertEqual(config.funding_sources[0].platform, FundingPlatform.GITHUB_SPONSORS)
        self.assertEqual(config.tiers[0].name, "Supporter")
        self.assertEqual(config.goals[0].name, "Server Costs")
        
    def test_element_serialization(self):
        """Test serializing individual elements"""
        element = BeneficiaryElement(self.canvas, 100, 100)
        element.name = "Alice Smith"
        element.email = "alice@example.com"
        element.github_username = "alicesmith"
        
        # Test the properties that would be serialized
        properties = {}
        for attr in ['name', 'email', 'github_username', 'website', 'description']:
            properties[attr] = getattr(element, attr)
            
        self.assertEqual(properties['name'], "Alice Smith")
        self.assertEqual(properties['email'], "alice@example.com")
        self.assertEqual(properties['github_username'], "alicesmith")
        
    def test_enum_conversion(self):
        """Test enum value conversion for serialization/deserialization"""
        source = FundingSourceElement(self.canvas, 100, 100)
        source.platform = FundingPlatform.PATREON
        source.funding_type = FundingType.ONE_TIME
        
        # Test enum value extraction
        platform_value = source.platform.value
        type_value = source.funding_type.value
        
        self.assertEqual(platform_value, "patreon")
        self.assertEqual(type_value, "one_time")
        
        # Test enum reconstruction
        reconstructed_platform = FundingPlatform(platform_value)
        reconstructed_type = FundingType(type_value)
        
        self.assertEqual(reconstructed_platform, FundingPlatform.PATREON)
        self.assertEqual(reconstructed_type, FundingType.ONE_TIME)


if __name__ == '__main__':
    print("Testing Graphical Editor Core Functionality...")
    unittest.main(verbosity=2)