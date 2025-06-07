"""
Tests for Step 3: Graphical Notation and Visualization functionality
"""

from textual.funding_dsl_parser import FundingDSLParser
from graphical.funding_visualizer import FundingVisualizer, visualize_funding_config
from graphical.interactive_diagrams import (
    InteractiveDiagramGenerator, 
    display_configuration_summary,
    create_funding_diagrams
)


def test_ascii_visualization():
    """Test ASCII art generation"""
    print("Testing ASCII visualization...")
    
    # Parse minimal example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Generate ASCII art
    visualizer = FundingVisualizer(config)
    ascii_art = visualizer.generate_ascii_overview()
    
    # Verify content
    assert config.project_name in ascii_art
    assert "Beneficiaries:" in ascii_art
    assert "Funding Sources:" in ascii_art
    assert "╔" in ascii_art  # Check for box drawing characters
    assert "╚" in ascii_art
    
    print("✅ ASCII visualization test passed")


def test_mermaid_flowchart():
    """Test Mermaid flowchart generation"""
    print("Testing Mermaid flowchart...")
    
    # Parse comprehensive example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/example_funding.dsl')
    
    # Generate flowchart
    visualizer = FundingVisualizer(config)
    flowchart = visualizer.generate_mermaid_flowchart()
    
    # Verify structure
    assert "flowchart TD" in flowchart
    assert "PROJECT" in flowchart
    assert config.project_name in flowchart
    assert "BEN1" in flowchart or "BEN2" in flowchart  # Beneficiary nodes
    assert "-->" in flowchart  # Connections
    
    # Check for emojis and styling
    assert "🧑‍💻" in flowchart or "💰" in flowchart
    
    print("✅ Mermaid flowchart test passed")


def test_mermaid_pie_chart():
    """Test Mermaid pie chart generation"""
    print("Testing Mermaid pie chart...")
    
    # Parse minimal example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Generate pie chart
    visualizer = FundingVisualizer(config)
    pie_chart = visualizer.generate_mermaid_pie_chart()
    
    # Verify structure
    assert 'pie title' in pie_chart
    assert config.project_name in pie_chart
    assert '"' in pie_chart  # Platform names in quotes
    assert ':' in pie_chart  # Value separators
    
    print("✅ Mermaid pie chart test passed")


def test_mermaid_timeline():
    """Test Mermaid timeline generation"""
    print("Testing Mermaid timeline...")
    
    # Parse comprehensive example (has goals)
    parser = FundingDSLParser()
    config = parser.parse_file('examples/example_funding.dsl')
    
    # Generate timeline
    visualizer = FundingVisualizer(config)
    timeline = visualizer.generate_mermaid_timeline()
    
    # Verify structure
    assert "timeline" in timeline
    assert "title" in timeline
    assert config.project_name in timeline
    
    # Check for goals if they exist
    if config.goals:
        assert "section" in timeline
        goal_found = any(goal.name in timeline for goal in config.goals)
        assert goal_found, "At least one goal should appear in timeline"
    
    print("✅ Mermaid timeline test passed")


def test_mermaid_class_diagram():
    """Test Mermaid class diagram generation"""
    print("Testing Mermaid class diagram...")
    
    # Parse comprehensive example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/example_funding.dsl')
    
    # Generate class diagram
    visualizer = FundingVisualizer(config)
    class_diagram = visualizer.generate_mermaid_class_diagram()
    
    # Verify structure
    assert "classDiagram" in class_diagram
    assert "FundingConfiguration" in class_diagram
    assert "class " in class_diagram
    assert "+string" in class_diagram or "+boolean" in class_diagram
    assert "||--o{" in class_diagram  # Relationship notation
    
    print("✅ Mermaid class diagram test passed")


def test_interactive_diagram_generator():
    """Test interactive diagram generator"""
    print("Testing interactive diagram generator...")
    
    # Parse minimal example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Create generator
    generator = InteractiveDiagramGenerator(config)
    
    # Test analysis
    analysis = generator.analyze_configuration()
    
    # Verify analysis structure
    assert 'project_name' in analysis
    assert 'beneficiaries_count' in analysis
    assert 'platform_distribution' in analysis
    assert analysis['project_name'] == config.project_name
    assert analysis['beneficiaries_count'] == len(config.beneficiaries)
    
    # Test diagram creation
    flowchart = generator.create_funding_flow_diagram()
    assert "flowchart TD" in flowchart
    
    pie_chart = generator.create_platform_distribution_chart()
    assert "pie title" in pie_chart
    
    print("✅ Interactive diagram generator test passed")


def test_configuration_summary():
    """Test configuration summary generation"""
    print("Testing configuration summary...")
    
    # Parse minimal example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Generate summary
    summary = display_configuration_summary(config)
    
    # Verify content
    assert config.project_name in summary
    assert "FUNDING CONFIGURATION VISUAL SUMMARY" in summary
    assert "CONFIGURATION ANALYSIS" in summary
    assert "RECOMMENDATIONS" in summary
    assert "Beneficiaries:" in summary
    assert "Funding Sources:" in summary
    
    print("✅ Configuration summary test passed")


def test_convenience_functions():
    """Test convenience functions"""
    print("Testing convenience functions...")
    
    # Parse minimal example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Test visualize_funding_config function
    flowchart = visualize_funding_config(config, 'flowchart')
    assert "flowchart TD" in flowchart
    
    pie_chart = visualize_funding_config(config, 'pie')
    assert "pie title" in pie_chart
    
    ascii_art = visualize_funding_config(config, 'ascii')
    assert config.project_name in ascii_art
    
    # Test create_funding_diagrams function
    diagrams = create_funding_diagrams(config)
    assert isinstance(diagrams, dict)
    assert 'funding_flow' in diagrams
    assert 'platform_distribution' in diagrams
    assert 'timeline' in diagrams
    assert 'structure' in diagrams
    
    print("✅ Convenience functions test passed")


def test_funding_matrix():
    """Test funding matrix generation"""
    print("Testing funding matrix...")
    
    # Parse comprehensive example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/example_funding.dsl')
    
    # Generate matrix
    visualizer = FundingVisualizer(config)
    matrix = visualizer.generate_funding_matrix()
    
    # Verify structure
    assert "Funding Sources Matrix" in matrix
    assert "Platform" in matrix
    assert "=" in matrix  # Header separator
    assert "-" in matrix  # Line separator
    
    print("✅ Funding matrix test passed")


def run_all_visualization_tests():
    """Run all visualization tests"""
    print("🎨 Running Step 3: Visualization Tests")
    print("=" * 45)
    print()
    
    tests = [
        test_ascii_visualization,
        test_mermaid_flowchart,
        test_mermaid_pie_chart,
        test_mermaid_timeline,
        test_mermaid_class_diagram,
        test_interactive_diagram_generator,
        test_configuration_summary,
        test_convenience_functions,
        test_funding_matrix
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All visualization tests passed!")
        return True
    else:
        print(f"😞 {total - passed} tests failed")
        return False


if __name__ == "__main__":
    success = run_all_visualization_tests()
    exit(0 if success else 1) 