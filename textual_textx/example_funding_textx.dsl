// Funding DSL Example for TextX Parser
// This file demonstrates all features of the Funding DSL

funding "AwesomeLib TextX Edition" {
    description "A comprehensive library showcasing TextX grammar capabilities"
    currency USD
    min_amount 1.0
    max_amount 1000.0
    
    // Define project beneficiaries
    beneficiaries {
        beneficiary "Alice Johnson" {
            email "alice@awesomelib.dev"
            github "alicej"
            website "https://alicej.dev"
            description "Lead maintainer and project founder"
        }
        
        beneficiary "Bob Smith" {
            github "bobsmith"
            description "Core contributor and documentation lead"
        }
    }
    
    // Configure funding platforms
    sources {
        github_sponsors "alicej" {
            type both
            active true
        }
        
        patreon "awesomelib-dev" {
            type recurring
            active true
            config {
                "campaign_id" "12345"
                "tier_mapping" "automatic"
            }
        }
        
        ko_fi "alicej" {
            type one_time
            active true
        }
        
        custom "PayPal Donations" {
            url "https://paypal.me/alicej"
            type both
            active true
        }
    }
    
    // Define sponsorship tiers
    tiers {
        tier "Coffee Supporter" {
            amount 5.0 USD
            description "Support with a small monthly contribution"
            benefits [
                "Thank you mention in README",
                "Priority issue responses",
                "Access to community chat"
            ]
        }
        
        tier "Monthly Backer" {
            amount 25.0 USD
            description "Regular monthly support for ongoing development"
            max_sponsors 50
            benefits [
                "All Coffee tier benefits",
                "Early access to new features",
                "Monthly progress updates",
                "Direct communication channel"
            ]
        }
        
        tier "Project Sponsor" {
            amount 100.0 USD
            description "Major project sponsorship with significant benefits"
            max_sponsors 5
            benefits [
                "All Backer tier benefits",
                "Logo placement in README and website",
                "Quarterly video calls with maintainers",
                "Feature request priority",
                "Custom integration support",
                "Annual sponsor recognition"
            ]
        }
    }
    
    // Set funding goals
    goals {
        goal "Server Infrastructure" {
            target 200.0 USD
            current 150.0 USD
            description "Cover monthly server hosting and infrastructure costs"
        }
        
        goal "Documentation Overhaul" {
            target 1000.0 USD
            current 250.0 USD
            deadline "2024-12-01"
            description "Complete rewrite of project documentation with interactive examples"
        }
        
        goal "Mobile App Development" {
            target 5000.0 USD
            current 0.0 USD
            deadline "2025-06-01"
            description "Develop companion mobile app for the library"
        }
    }
} 