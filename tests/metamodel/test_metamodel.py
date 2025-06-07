"""
Simple test to verify the Funding DSL metamodel works correctly
"""

from metamodel.funding_metamodel import (
    FundingConfiguration, Beneficiary, FundingSource, FundingTier, 
    FundingGoal, FundingAmount, FundingPlatform, FundingType, 
    CurrencyType, FundingModelValidator
)

def test_metamodel():
    print("Testing Funding DSL Metamodel...")
    
    # Test basic objects
    amount = FundingAmount(25.0, CurrencyType.USD)
    print(f"Amount: {amount}")
    
    beneficiary = Beneficiary(
        name="John Doe",
        github_username="johndoe",
        email="john@example.com"
    )
    print(f"Beneficiary: {beneficiary}")
    
    source = FundingSource(
        platform=FundingPlatform.GITHUB_SPONSORS,
        username="johndoe",
        funding_type=FundingType.BOTH
    )
    print(f"Source: {source}")
    
    tier = FundingTier(
        name="Supporter",
        amount=amount,
        description="Monthly supporter",
        benefits=["Thank you note", "Early access"]
    )
    print(f"Tier: {tier}")
    
    goal = FundingGoal(
        name="Infrastructure",
        target_amount=FundingAmount(500.0, CurrencyType.USD),
        current_amount=FundingAmount(150.0, CurrencyType.USD)
    )
    print(f"Goal: {goal}")
    print(f"Goal progress: {goal.progress_percentage:.1f}%")
    
    # Test configuration
    config = FundingConfiguration(
        project_name="TestProject",
        description="A test project for funding"
    )
    
    config.add_beneficiary(beneficiary)
    config.add_funding_source(source)
    config.add_tier(tier)
    config.add_goal(goal)
    
    print(f"\nConfiguration: {config}")
    print(f"Active sources: {len(config.get_active_sources())}")
    print(f"Active tiers: {len(config.get_active_tiers())}")
    
    # Test validation
    errors = FundingModelValidator.validate_configuration(config)
    if errors:
        print(f"\nValidation errors: {errors}")
    else:
        print("\n✓ Configuration is valid!")
    
    print("\nMetamodel test completed successfully!")

if __name__ == "__main__":
    test_metamodel() 