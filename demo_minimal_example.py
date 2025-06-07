#!/usr/bin/env python3
"""
Demonstration of Minimal Funding Example
Shows how our DSL represents the same information as GitHub's funding.yml
"""

def demonstrate_minimal_example():
    print("🎯 Minimal Funding Configuration Demonstration")
    print("=" * 55)
    print()
    
    # Import our modules
    from textual.funding_dsl_parser import FundingDSLParser
    from metamodel.funding_metamodel import FundingModelValidator
    
    print("📋 GitHub funding.yml Example:")
    print("-" * 30)
    print("""github: [octocat, surftocat]
patreon: octocat
tidelift: npm/octo-package
custom: ["https://www.paypal.me/octocat", octocat.com]""")
    print()
    
    print("🔧 Parsing equivalent DSL configuration...")
    parser = FundingDSLParser()
    config = parser.parse_file('examples/minimal_funding.dsl')
    print("✅ Parsing successful!")
    print()
    
    print("📊 Parsed Configuration:")
    print("-" * 30)
    print(f"Project: {config.project_name}")
    print(f"Description: {config.description}")
    print(f"Currency: {config.preferred_currency.value}")
    print()
    
    print(f"👥 Beneficiaries ({len(config.beneficiaries)}):")
    for ben in config.beneficiaries:
        print(f"  • {ben.name}")
        if ben.github_username:
            print(f"    GitHub: @{ben.github_username}")
    print()
    
    print(f"💰 Funding Sources ({len(config.funding_sources)}):")
    for source in config.funding_sources:
        print(f"  • {source.platform.value}: {source.username}")
        if source.custom_url:
            print(f"    URL: {source.custom_url}")
        if source.platform_specific_config:
            for key, value in source.platform_specific_config.items():
                print(f"    {key}: {value}")
    print()
    
    print("🔍 Equivalent GitHub funding.yml would be:")
    print("-" * 40)
    
    # Group by platform
    github_users = []
    patreon_users = []
    custom_urls = []
    tidelift_packages = []
    
    for source in config.funding_sources:
        if source.platform.value == 'GITHUB_SPONSORS':
            github_users.append(source.username)
        elif source.platform.value == 'PATREON':
            patreon_users.append(source.username)
        elif source.platform.value == 'CUSTOM':
            if 'tidelift' in source.username:
                package = source.platform_specific_config.get('package', '')
                if package:
                    tidelift_packages.append(package)
            else:
                custom_urls.append(source.custom_url)
    
    # Generate equivalent YAML
    if github_users:
        if len(github_users) == 1:
            print(f"github: {github_users[0]}")
        else:
            print(f"github: {github_users}")
    
    if patreon_users:
        for user in patreon_users:
            print(f"patreon: {user}")
    
    if tidelift_packages:
        for package in tidelift_packages:
            print(f"tidelift: {package}")
    
    if custom_urls:
        if len(custom_urls) == 1:
            print(f'custom: "{custom_urls[0]}"')
        else:
            print(f"custom: {custom_urls}")
    
    print()
    
    print("✅ Validation:")
    errors = FundingModelValidator.validate_configuration(config)
    if errors:
        print("❌ Validation errors found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration is completely valid!")
    print()
    
    print("🌟 Benefits of DSL Approach:")
    print("  ✅ Richer metadata (beneficiaries, descriptions)")
    print("  ✅ Structured configuration with validation")
    print("  ✅ Support for complex funding scenarios")
    print("  ✅ Platform-specific configuration options")
    print("  ✅ Human-readable and machine-processable")
    print("  ✅ Can generate multiple output formats")

if __name__ == "__main__":
    demonstrate_minimal_example() 