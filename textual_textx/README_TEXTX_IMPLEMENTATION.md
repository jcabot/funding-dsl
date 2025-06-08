# TextX-based Funding DSL Implementation

This directory contains a complete implementation of the Funding DSL using the TextX meta-language framework. TextX provides a different approach to grammar definition and parsing compared to ANTLR, offering more integrated model transformation capabilities.

## Overview

The TextX implementation provides:

- **Declarative Grammar**: Simple, readable grammar definition in `.tx` format
- **Automatic Model Generation**: TextX automatically creates Python objects from parsed text
- **Integrated Transformation**: Direct conversion from parsed models to metamodel instances
- **Error Handling**: Built-in syntax error reporting and validation
- **Extensibility**: Easy to extend and modify grammar rules

## Architecture

### Core Components

1. **Grammar Definition** (`funding_dsl.tx`)
   - TextX grammar file defining the DSL syntax
   - Declarative rule definitions
   - Built-in support for common patterns

2. **Parser Implementation** (`funding_dsl_textx_parser.py`)
   - Main parser class using TextX engine
   - Model transformation logic
   - Error handling and validation

3. **Package Structure** (`__init__.py`)
   - Clean package interface
   - Exports main parser functions
   - Consistent API design

## Grammar Features

### TextX vs ANTLR Syntax

**ANTLR Style:**
```antlr
fundingConfiguration
    : fundingBlock EOF
    ;

fundingBlock
    : FUNDING STRING '{' configurationContent '}'
    ;
```

**TextX Style:**
```textx
FundingConfiguration:
    'funding' name=STRING '{' 
        (description=DescriptionElement)?
        (currency=CurrencyElement)?
        // ... other elements
    '}'
;
```

### Key Differences

1. **Rule Definition**: TextX uses `:` instead of ANTLR's rule syntax
2. **Attribute Assignment**: Direct assignment with `name=STRING`
3. **Optional Elements**: Parentheses with `?` for optional elements
4. **Repetition**: `*=` for lists, `+=` for non-empty lists
5. **Built-in Types**: STRING, INT, FLOAT, BOOL are predefined

### Supported DSL Elements

- **Project Configuration**: Name, description, currency, amount limits
- **Beneficiaries**: Name, email, GitHub, website, description
- **Funding Sources**: All major platforms plus custom sources
- **Sponsorship Tiers**: Amount, benefits, limits, descriptions
- **Funding Goals**: Targets, progress, deadlines, descriptions

## Usage Examples

### Basic Parsing

```python
from textual_textx import parse_funding_dsl_text_textx

dsl_text = '''
funding "My Project" {
    description "A sample project"
    currency USD
    
    beneficiaries {
        beneficiary "Developer" {
            github "dev"
            email "dev@example.com"
        }
    }
    
    sources {
        github_sponsors "dev" {
            type both
            active true
        }
    }
}
'''

config = parse_funding_dsl_text_textx(dsl_text)
print(f"Project: {config.project_name}")
print(f"Beneficiaries: {len(config.beneficiaries)}")
```

### File Parsing

```python
from textual_textx import parse_funding_dsl_file_textx

config = parse_funding_dsl_file_textx('my_project.dsl')
```

### Advanced Usage

```python
from textual_textx import FundingDSLTextXParser

parser = FundingDSLTextXParser()
config = parser.parse_text(dsl_text)

# Validate the configuration
from metamodel.funding_metamodel import FundingModelValidator
errors = FundingModelValidator.validate_configuration(config)
if errors:
    print("Validation errors:", errors)
```

## File Structure

```
textual_textx/
├── __init__.py                              # Package initialization
├── funding_dsl.tx                           # TextX grammar definition
├── funding_dsl_textx_parser.py              # Main parser implementation
├── demo_textx.py                            # Comprehensive demo script
├── example_funding_clean.dsl                # Example DSL file (no comments)
├── example_funding_textx.dsl                # Example DSL file (with comments)
└── README_TEXTX_IMPLEMENTATION.md           # This documentation
```

## Testing

Comprehensive tests are available in `tests/textual_textx/`:

```bash
# Run all tests
python tests/textual_textx/test_textx_parser_fixed.py

# Run specific test
python -m unittest tests.textual_textx.test_textx_parser_fixed.TestTextXParser.test_complete_configuration
```

### Test Coverage

- ✅ Minimal configurations
- ✅ Complete configurations with all elements
- ✅ All currency types (USD, EUR, GBP, CAD, AUD)
- ✅ All platform types (GitHub, Patreon, Ko-fi, etc.)
- ✅ All funding types (one-time, recurring, both)
- ✅ Optional element handling
- ✅ Validation integration
- ✅ Error handling

## Comparison with ANTLR Implementation

| Feature | TextX | ANTLR |
|---------|-------|-------|
| Grammar Syntax | Declarative, Python-like | Traditional parser grammar |
| Model Generation | Automatic | Manual transformation required |
| Learning Curve | Easier for Python developers | Steeper, more general purpose |
| Performance | Good for most use cases | Optimized for high performance |
| Debugging | Built-in model inspection | Requires additional tooling |
| Extensibility | Easy grammar modifications | More complex but more powerful |

## Advantages of TextX Implementation

1. **Simpler Grammar**: More readable and maintainable grammar definition
2. **Automatic Model Creation**: No need for manual AST traversal
3. **Python Integration**: Seamless integration with Python ecosystem
4. **Rapid Development**: Faster iteration on grammar changes
5. **Built-in Features**: Comment handling, error reporting, model validation

## Performance Considerations

- **Parsing Speed**: Suitable for typical DSL files (< 1MB)
- **Memory Usage**: Efficient for moderate-sized configurations
- **Scalability**: Good for development and medium-scale production use
- **Optimization**: TextX provides caching and memoization options

## Error Handling

The TextX parser provides detailed error messages:

```python
try:
    config = parse_funding_dsl_text_textx(invalid_dsl)
except Exception as e:
    print(f"Parse error: {e}")
    # Output: Parse error: Expected 'funding' at line 1, column 1
```

## Extension Points

### Custom Validation

```python
class CustomValidator(FundingModelValidator):
    @staticmethod
    def validate_custom_rules(config):
        errors = []
        # Add custom validation logic
        return errors
```

### Grammar Extensions

To add new DSL features:

1. Modify `funding_dsl.tx` grammar
2. Update parser transformation logic
3. Add corresponding metamodel classes
4. Update tests and documentation

## Integration with Main Project

The TextX implementation integrates seamlessly with the main project:

- Uses the same metamodel classes
- Compatible with validation system
- Supports visitor pattern
- Works with export functionality

## Demo and Examples

Run the comprehensive demo:

```bash
python textual_textx/demo_textx.py
```

This demonstrates:
- Basic parsing capabilities
- Complex configuration handling
- Comparison with ANTLR parser
- Grammar feature showcase
- Validation integration

## Future Enhancements

Potential improvements:

1. **Advanced Comment Processing**: Extract and preserve comment metadata
2. **IDE Integration**: Language server protocol support
3. **Performance Optimization**: Caching and lazy loading
4. **Advanced Validation**: Schema-based validation
5. **Code Generation**: Generate platform-specific configs

## Conclusion

The TextX implementation provides a clean, maintainable alternative to the ANTLR-based parser. It's particularly well-suited for:

- Rapid prototyping of DSL features
- Python-centric development environments
- Educational purposes and DSL learning
- Projects where simplicity is preferred over maximum performance

Both implementations (TextX and ANTLR) are fully functional and can be used interchangeably, allowing developers to choose based on their specific needs and preferences. 