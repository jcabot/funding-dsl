// Example Funding DSL Configuration
// This file demonstrates the complete syntax of the Funding DSL

funding "AwesomeLib" {
    description "A comprehensive library for awesome functionality"
    currency USD
    min_amount 1.00
    max_amount 1000.00
    
    // Define who receives the funding
    beneficiaries {
        beneficiary "Alice Johnson" {
            email "alice@example.com"
            github "alicej" 
            website "https://alicej.dev"
            description "Lead maintainer and project founder"
        }
        
        beneficiary "Bob Smith" {
            github "bobsmith"
            description "Core contributor and documentation maintainer"
        }
    }
    
    // Define funding sources/platforms
    sources {
        github_sponsors "alicej" {
            type both
            active true
        }
        
        patreon "alicej-dev" {
            type recurring
            config {
                "campaign_id" "12345"
                "tier_mapping" "auto"
            }
        }
        
        ko_fi "alicej" {
            type one_time
        }
        
        custom "Custom Donations" {
            url "https://example.com/donate"
            type both
        }
    }
    
    // Define sponsorship tiers
    tiers {
        tier "Buy me a coffee" {
            amount 5.00 USD
            description "Support with a small donation"
            benefits [
                "Thank you mention in README",
                "Priority issue responses"
            ]
        }
        
        tier "Monthly Supporter" {
            amount 25.00 USD
            description "Regular monthly support"
            max_sponsors 100
            benefits [
                "All Coffee tier benefits",
                "Early access to new features", 
                "Monthly progress updates",
                "Direct communication channel"
            ]
        }
        
        tier "Project Sponsor" {
            amount 100.00 USD
            description "Major project sponsorship"
            max_sponsors 5
            benefits [
                "All Supporter tier benefits",
                "Logo placement in README",
                "Quarterly video calls",
                "Feature request priority",
                "Custom integration support"
            ]
        }
    }
    
    // Define funding goals
    goals {
        goal "Server Hosting" {
            target 200.00 USD
            current 150.00 USD
            description "Cover monthly server and infrastructure costs"
        }
        
        goal "Documentation Overhaul" {
            target 1000.00 USD
            current 250.00 USD
            deadline "2024-06-01"
            description "Complete rewrite of project documentation with examples"
        }
    }
} 