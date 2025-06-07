"""
Simple test to debug parser issues
"""

def test_simple():
    print("Starting simple test...")
    
    from textual.funding_dsl_parser import FundingDSLParser
    
    # Create a simple test DSL
    simple_dsl = '''
    funding "TestProject" {
        description "A test project"
        currency USD
        
        beneficiaries {
            beneficiary "John Doe" {
                email "john@example.com"
                github "johndoe"
            }
        }
    }
    '''
    
    print("Creating parser...")
    parser = FundingDSLParser()
    
    print("Parsing text...")
    try:
        config = parser.parse_text(simple_dsl)
        print("✅ Parse successful!")
        print(f"Project: {config.project_name}")
        print(f"Description: {config.description}")
        print(f"Beneficiaries: {len(config.beneficiaries)}")
        
    except Exception as e:
        print(f"❌ Parse failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple() 