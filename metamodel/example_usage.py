"""
Example usage of the Funding DSL Metamodel
Demonstrates how to create and use funding configuration objects.
"""

from .funding_metamodel import (
    FundingConfiguration, Beneficiary, FundingSource, FundingTier, 
    FundingGoal, FundingAmount, FundingPlatform, FundingType, 
    CurrencyType, FundingModelValidator
)
from datetime import datetime, timedelta
try:
    from .metamodel_visualizer import MetamodelVisualizer
    VISUALIZER_AVAILABLE = True
except ImportError:
    VISUALIZER_AVAILABLE = False


def create_example_funding_configuration():
    """Create a comprehensive example of a funding configuration"""
    
    # Create beneficiaries
    main_maintainer = Beneficiary(
        name="Alice Johnson",
        email="alice@example.com",
        github_username="alicej",
        website="https://alicej.dev",
        description="Lead maintainer and project founder"
    )
    
    co_maintainer = Beneficiary(
        name="Bob Smith", 
        github_username="bobsmith",
        description="Core contributor and documentation maintainer"
    )
    
    # Create funding sources
    github_sponsors = FundingSource(
        platform=FundingPlatform.GITHUB_SPONSORS,
        username="alicej",
        funding_type=FundingType.BOTH
    )
    
    patreon_source = FundingSource(
        platform=FundingPlatform.PATREON,
        username="alicej-dev",
        funding_type=FundingType.RECURRING
    )
    
    ko_fi_source = FundingSource(
        platform=FundingPlatform.KO_FI,
        username="alicej",
        funding_type=FundingType.ONE_TIME
    )
    
    # Create funding tiers
    coffee_tier = FundingTier(
        name="Buy me a coffee",
        amount=FundingAmount(5.0, CurrencyType.USD),
        description="Support with a small donation",
        benefits=["Thank you mention in README", "Priority issue responses"]
    )
    
    supporter_tier = FundingTier(
        name="Monthly Supporter", 
        amount=FundingAmount(25.0, CurrencyType.USD),
        description="Regular monthly support",
        benefits=[
            "All Coffee tier benefits",
            "Early access to new features",
            "Monthly progress updates",
            "Direct communication channel"
        ]
    )
    
    sponsor_tier = FundingTier(
        name="Project Sponsor",
        amount=FundingAmount(100.0, CurrencyType.USD),
        description="Major project sponsorship",
        benefits=[
            "All Supporter tier benefits", 
            "Logo placement in README",
            "Quarterly video calls",
            "Feature request priority",
            "Custom integration support"
        ],
        max_sponsors=5
    )
    
    # Create funding goals
    hosting_goal = FundingGoal(
        name="Server Hosting",
        target_amount=FundingAmount(200.0, CurrencyType.USD),
        description="Cover monthly server and infrastructure costs",
        current_amount=FundingAmount(150.0, CurrencyType.USD)
    )
    
    documentation_goal = FundingGoal(
        name="Documentation Overhaul",
        target_amount=FundingAmount(1000.0, CurrencyType.USD),
        description="Complete rewrite of project documentation with examples",
        deadline=datetime.now() + timedelta(days=90),
        current_amount=FundingAmount(250.0, CurrencyType.USD)
    )
    
    # Create the main funding configuration
    config = FundingConfiguration(
        project_name="AwesomeLib",
        description="A comprehensive library for awesome functionality",
        preferred_currency=CurrencyType.USD,
        min_amount=FundingAmount(1.0, CurrencyType.USD),
        max_amount=FundingAmount(1000.0, CurrencyType.USD)
    )
    
    # Add all components to the configuration
    config.add_beneficiary(main_maintainer)
    config.add_beneficiary(co_maintainer)
    
    config.add_funding_source(github_sponsors)
    config.add_funding_source(patreon_source)
    config.add_funding_source(ko_fi_source)
    
    config.add_tier(coffee_tier)
    config.add_tier(supporter_tier)
    config.add_tier(sponsor_tier)
    
    config.add_goal(hosting_goal)
    config.add_goal(documentation_goal)
    
    return config


def demonstrate_metamodel_features():
    """Demonstrate various features of the metamodel"""
    
    print("=== Funding DSL Metamodel Example ===\n")
    
    # Create example configuration
    config = create_example_funding_configuration()
    
    print(f"Project: {config}")
    print(f"Description: {config.description}")
    print(f"Preferred Currency: {config.preferred_currency.value}")
    print()
    
    # Display beneficiaries
    print("Beneficiaries:")
    for beneficiary in config.beneficiaries:
        print(f"  - {beneficiary.name} (@{beneficiary.github_username or 'N/A'})")
        if beneficiary.description:
            print(f"    {beneficiary.description}")
    print()
    
    # Display active funding sources
    print("Active Funding Sources:")
    for source in config.get_active_sources():
        print(f"  - {source.platform.value}: {source.username} ({source.funding_type.value})")
    print()
    
    # Display active tiers
    print("Available Sponsorship Tiers:")
    for tier in config.get_active_tiers():
        print(f"  - {tier.name}: {tier.amount}")
        print(f"    {tier.description}")
        if tier.benefits:
            print("    Benefits:")
            for benefit in tier.benefits:
                print(f"      • {benefit}")
        if tier.max_sponsors:
            print(f"    Max sponsors: {tier.max_sponsors}")
        print()
    
    # Display funding goals
    print("Funding Goals:")
    for goal in config.goals:
        print(f"  - {goal.name}: {goal.current_amount}/{goal.target_amount}")
        print(f"    Progress: {goal.progress_percentage:.1f}%")
        if goal.description:
            print(f"    {goal.description}")
        if goal.deadline:
            print(f"    Deadline: {goal.deadline.strftime('%Y-%m-%d')}")
        print()
    
    # Validate the configuration
    print("Configuration Validation:")
    errors = FundingModelValidator.validate_configuration(config)
    if errors:
        print("  Validation errors found:")
        for error in errors:
            print(f"    - {error}")
    else:
        print("  ✓ Configuration is valid!")
    print()
    
    # Demonstrate utility methods
    print("Utility Methods:")
    print(f"  - Active sources count: {len(config.get_active_sources())}")
    print(f"  - Active tiers count: {len(config.get_active_tiers())}")
    print(f"  - Unreached goals count: {len(config.get_unreached_goals())}")
    
    return config


def generate_visualizations():
    """Generate and display visualizations"""
    
    print("\n=== Generating Visualizations ===\n")
    
    if VISUALIZER_AVAILABLE:
        # Create visualizer
        visualizer = MetamodelVisualizer()
        
        # Generate class diagram
        print("Class Diagram GraphViz Source:")
        print("-" * 40)
        class_diagram = visualizer.generate_class_diagram()
        print(class_diagram[:500] + "..." if len(class_diagram) > 500 else class_diagram)
        print()
        
        # Generate concept map  
        print("Concept Map GraphViz Source:")
        print("-" * 40)
        concept_map = visualizer.generate_concept_map()
        print(concept_map[:500] + "..." if len(concept_map) > 500 else concept_map)
        print()
        
        print("Note: Install graphviz and run 'python metamodel_visualizer.py' to see full diagrams")
    else:
        print("Graphviz not available. Install with: pip install graphviz")


if __name__ == "__main__":
    # Run the demonstration
    config = demonstrate_metamodel_features()
    
    # Generate visualizations
    generate_visualizations()
    
    print("\n=== Summary ===")
    print("The Funding DSL Metamodel provides:")
    print("• Rich modeling of funding configurations")
    print("• Support for multiple platforms and currencies") 
    print("• Flexible tier and goal management")
    print("• Built-in validation and utility methods")
    print("• Extensible design with visitor pattern")
    print("\nReady for step 2: Creating the concrete textual syntax!") 