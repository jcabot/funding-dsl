"""
Tests for the Graphical Model Editor
"""

import unittest
import tempfile
import os
import json
import sys
from unittest.mock import Mock, patch

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from graphical.graphical_editor import (
    GraphicalFundingEditor, ProjectElement, BeneficiaryElement,
    FundingSourceElement, FundingTierElement, FundingGoalElement
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


class TestGraphicalEditor(unittest.TestCase):
    """Test the main graphical editor functionality"""
    
    @patch('tkinter.Tk')
    @patch('tkinter.Canvas')
    def setUp(self, mock_canvas, mock_tk):
        """Set up test environment with mocked tkinter"""
        self.mock_root = Mock()
        self.mock_canvas = MockCanvas()
        
        mock_tk.return_value = self.mock_root
        mock_canvas.return_value = self.mock_canvas
        
        # Create editor with mocked dependencies
        self.editor = GraphicalFundingEditor()
        self.editor.canvas = self.mock_canvas
        
    def test_add_project_element(self):
        """Test adding a project element"""
        initial_count = len(self.editor.elements)
        
        self.editor.add_project()
        
        self.assertEqual(len(self.editor.elements), initial_count + 1)
        self.assertIsNotNone(self.editor.project_element)
        self.assertIsInstance(self.editor.project_element, ProjectElement)
        
    def test_add_multiple_elements(self):
        """Test adding multiple different elements"""
        initial_count = len(self.editor.elements)
        
        self.editor.add_project()
        self.editor.add_beneficiary()
        self.editor.add_funding_source()
        self.editor.add_funding_tier()
        self.editor.add_funding_goal()
        
        self.assertEqual(len(self.editor.elements), initial_count + 5)
        
        # Check element types
        element_types = [type(elem).__name__ for elem in self.editor.elements]
        self.assertIn('ProjectElement', element_types)
        self.assertIn('BeneficiaryElement', element_types)
        self.assertIn('FundingSourceElement', element_types)
        self.assertIn('FundingTierElement', element_types)
        self.assertIn('FundingGoalElement', element_types)
        
    def test_create_funding_configuration(self):
        """Test creating a funding configuration from visual elements"""
        # Add required project element
        self.editor.add_project()
        self.editor.project_element.project_name = "Test Project"
        self.editor.project_element.description = "A test project"
        
        # Add other elements
        self.editor.add_beneficiary()
        self.editor.elements[-1].name = "John Doe"
        
        self.editor.add_funding_source()
        self.editor.elements[-1].platform = FundingPlatform.GITHUB_SPONSORS
        self.editor.elements[-1].username = "johndoe"
        
        self.editor.add_funding_tier()  
        self.editor.elements[-1].name = "Supporter"
        self.editor.elements[-1].amount = 25.0
        
        self.editor.add_funding_goal()
        self.editor.elements[-1].name = "Server Costs"
        self.editor.elements[-1].target_amount = 1000.0
        
        # Create configuration
        config = self.editor.create_funding_configuration()
        
        self.assertIsInstance(config, FundingConfiguration)
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
        
    def test_serialization_deserialization(self):
        """Test model serialization and deserialization"""
        # Add elements
        self.editor.add_project()
        self.editor.project_element.project_name = "Test Project"
        
        self.editor.add_beneficiary()
        self.editor.elements[-1].name = "Alice Smith"
        self.editor.elements[-1].email = "alice@example.com"
        
        # Serialize
        model_data = self.editor.serialize_model()
        
        self.assertIsInstance(model_data, dict)
        self.assertIn('elements', model_data)
        self.assertEqual(len(model_data['elements']), 2)
        
        # Clear and deserialize
        self.editor.elements.clear()
        self.editor.project_element = None
        
        self.editor.deserialize_model(model_data)
        
        self.assertEqual(len(self.editor.elements), 2)
        self.assertIsNotNone(self.editor.project_element)
        
        # Find beneficiary element
        beneficiary_element = None
        for elem in self.editor.elements:
            if isinstance(elem, BeneficiaryElement):
                beneficiary_element = elem
                break
                
        self.assertIsNotNone(beneficiary_element)
        self.assertEqual(beneficiary_element.name, "Alice Smith")
        self.assertEqual(beneficiary_element.email, "alice@example.com")
        
    def test_model_save_load_flow(self):
        """Test the complete save/load workflow"""
        # Create a test model
        self.editor.add_project()
        self.editor.project_element.project_name = "SaveTest Project"
        
        self.editor.add_beneficiary()
        self.editor.elements[-1].name = "Test Beneficiary"
        
        # Test serialization
        model_data = self.editor.serialize_model()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fmodel', delete=False) as f:
            json.dump(model_data, f, indent=2)
            temp_filename = f.name
            
        try:
            # Load from file
            with open(temp_filename, 'r') as f:
                loaded_data = json.load(f)
                
            # Clear current model
            self.editor.elements.clear()
            self.editor.project_element = None
            
            # Deserialize
            self.editor.deserialize_model(loaded_data)
            
            # Verify
            self.assertIsNotNone(self.editor.project_element)
            self.assertEqual(self.editor.project_element.project_name, "SaveTest Project")
            self.assertEqual(len(self.editor.elements), 2)
            
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
                
    def test_element_deletion(self):
        """Test element deletion"""
        # Add elements
        self.editor.add_project()
        self.editor.add_beneficiary()
        
        initial_count = len(self.editor.elements)
        beneficiary_element = self.editor.elements[-1]
        
        # Delete beneficiary
        self.editor.delete_element(beneficiary_element)
        
        self.assertEqual(len(self.editor.elements), initial_count - 1)
        self.assertNotIn(beneficiary_element, self.editor.elements)
        
        # Delete project (should clear project_element reference)
        project_element = self.editor.project_element
        self.editor.delete_element(project_element)
        
        self.assertIsNone(self.editor.project_element)
        self.assertNotIn(project_element, self.editor.elements)
        
    def test_clear_canvas(self):
        """Test clearing all elements"""
        # Add elements
        self.editor.add_project()
        self.editor.add_beneficiary()
        self.editor.add_funding_source()
        
        self.assertGreater(len(self.editor.elements), 0)
        self.assertIsNotNone(self.editor.project_element)
        
        # Clear canvas
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.editor.clear_canvas()
        
        self.assertEqual(len(self.editor.elements), 0)
        self.assertIsNone(self.editor.project_element)
        self.assertIsNone(self.editor.selected_element)


if __name__ == '__main__':
    unittest.main() 