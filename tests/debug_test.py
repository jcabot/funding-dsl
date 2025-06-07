#!/usr/bin/env python3

print("=== Debug Test Starting ===")

try:
    print("1. Importing modules...")
    from textual.funding_dsl_parser import FundingDSLParser
    from metamodel.funding_metamodel import FundingConfiguration
    print("   ✅ Imports successful")
    
    print("2. Creating simple DSL text...")
    simple_dsl = '''funding "TestProject" {
    description "A test project"
    currency USD
}'''
    print(f"   DSL text: {repr(simple_dsl[:50])}...")
    
    print("3. Creating parser...")
    parser = FundingDSLParser()
    print("   ✅ Parser created")
    
    print("4. Parsing text...")
    config = parser.parse_text(simple_dsl)
    print("   ✅ Parse successful!")
    
    print("5. Checking results...")
    print(f"   Project name: {config.project_name}")
    print(f"   Description: {config.description}")
    print(f"   Currency: {config.preferred_currency}")
    
    print("=== Test Completed Successfully ===")
    
except Exception as e:
    print(f"❌ Error at step: {e}")
    import traceback
    traceback.print_exc()
    print("=== Test Failed ===") 