"""
Tests for export functionality
"""

import json
import yaml
import tempfile
import os
from textual.funding_dsl_parser import FundingDSLParser
from export.funding_exporter import FundingExporter, export_funding_config


def test_github_yml_export():
    """Test GitHub funding.yml export"""
    print("Testing GitHub funding.yml export...")
    
    # Parse minimal example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Export to GitHub format
    exporter = FundingExporter(config)
    yml_content = exporter.to_github_funding_yml()
    
    # Verify content
    assert "github:" in yml_content
    assert "patreon:" in yml_content
    assert "tidelift:" in yml_content
    assert "custom:" in yml_content
    assert config.project_name in yml_content
    
    # Parse YAML to verify structure
    lines = yml_content.split('\n')
    yaml_start = 0
    for i, line in enumerate(lines):
        if not line.startswith('#') and line.strip():
            yaml_start = i
            break
    
    yaml_content = '\n'.join(lines[yaml_start:])
    parsed_yaml = yaml.safe_load(yaml_content)
    
    assert 'github' in parsed_yaml
    assert isinstance(parsed_yaml['github'], list)
    assert 'octocat' in parsed_yaml['github']
    assert 'surftocat' in parsed_yaml['github']
    
    print("✅ GitHub funding.yml export test passed")


def test_json_export():
    """Test JSON export"""
    print("Testing JSON export...")
    
    # Parse comprehensive example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/example_funding.dsl')
    
    # Export to JSON
    exporter = FundingExporter(config)
    json_content = exporter.to_json()
    
    # Parse JSON to verify structure
    data = json.loads(json_content)
    
    # Verify structure
    assert 'project' in data
    assert 'beneficiaries' in data
    assert 'funding_sources' in data
    assert 'tiers' in data
    assert 'goals' in data
    assert 'metadata' in data
    
    # Verify project info
    assert data['project']['name'] == config.project_name
    assert data['project']['description'] == config.description
    
    # Verify metadata
    assert data['metadata']['generator'] == 'funding-dsl-exporter'
    assert 'generated_at' in data['metadata']
    
    print("✅ JSON export test passed")


def test_markdown_export():
    """Test Markdown export"""
    print("Testing Markdown export...")
    
    # Parse comprehensive example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/example_funding.dsl')
    
    # Export to Markdown
    exporter = FundingExporter(config)
    md_content = exporter.to_markdown()
    
    # Verify content
    assert f"# {config.project_name}" in md_content
    assert "## 👥 Beneficiaries" in md_content
    assert "## 💰 How to Support" in md_content
    assert "## 🎯 Sponsorship Tiers" in md_content
    assert "## 📈 Funding Goals" in md_content
    
    # Check for specific elements
    if config.beneficiaries:
        assert config.beneficiaries[0].name in md_content
    
    if config.tiers:
        assert config.tiers[0].name in md_content
    
    print("✅ Markdown export test passed")


def test_csv_export():
    """Test CSV export"""
    print("Testing CSV export...")
    
    # Parse minimal example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Export to CSV
    exporter = FundingExporter(config)
    csv_content = exporter.to_csv()
    
    # Verify content
    lines = csv_content.strip().split('\n')
    assert len(lines) > 1  # Header + at least one data row
    
    # Verify header
    header = lines[0]
    assert 'Platform' in header
    assert 'Username' in header
    assert 'Funding Type' in header
    assert 'Active' in header
    
    # Verify data rows
    for line in lines[1:]:
        assert line.strip()  # Non-empty
        fields = line.split(',')
        assert len(fields) >= 4  # At least 4 fields
    
    print("✅ CSV export test passed")


def test_file_export():
    """Test file export functionality"""
    print("Testing file export...")
    
    # Parse minimal example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Test export to temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test each format
        formats = ['github_yml', 'json', 'markdown', 'csv']
        
        for format_name in formats:
            output_file = os.path.join(temp_dir, f"test.{format_name}")
            
            # Export to file
            content = export_funding_config(config, format_name, output_file)
            
            # Verify file was created
            assert os.path.exists(output_file)
            
            # Verify file content
            with open(output_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            assert file_content == content
            assert len(file_content) > 0
    
    print("✅ File export test passed")


def test_validation_integration():
    """Test export with validation"""
    print("Testing export with validation...")
    
    # Parse example
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    
    # Validate before export
    from metamodel.funding_metamodel import FundingModelValidator
    errors = FundingModelValidator.validate_configuration(config)
    
    # Should be valid
    assert not errors, f"Configuration should be valid, but got errors: {errors}"
    
    # Export should work
    exporter = FundingExporter(config)
    yml_content = exporter.to_github_funding_yml()
    
    assert yml_content
    assert config.project_name in yml_content
    
    print("✅ Validation integration test passed")


def run_all_tests():
    """Run all export tests"""
    print("🧪 Running Export Functionality Tests")
    print("=" * 40)
    print()
    
    tests = [
        test_github_yml_export,
        test_json_export,
        test_markdown_export,
        test_csv_export,
        test_file_export,
        test_validation_integration
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
        print("🎉 All export tests passed!")
        return True
    else:
        print(f"😞 {total - passed} tests failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1) 