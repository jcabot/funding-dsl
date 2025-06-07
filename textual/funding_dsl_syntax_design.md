# Funding DSL Textual Syntax Design

## Overview
This document defines the concrete textual syntax for the Funding DSL that users will write in `.funding` files.

## Example Funding DSL File

```funding
// Funding configuration for AwesomeLib project
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
                campaign_id "12345"
                tier_mapping "auto"
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
```

## Syntax Elements

### 1. **Top-level Structure**
```funding
funding "ProjectName" {
    // configuration content
}
```

### 2. **Basic Properties**
```funding
description "Project description"
currency USD
min_amount 1.00
max_amount 1000.00
```

### 3. **Beneficiaries Block**
```funding
beneficiaries {
    beneficiary "Name" {
        email "email@example.com"      // optional
        github "username"              // optional  
        website "https://..."          // optional
        description "Description"      // optional
    }
}
```

### 4. **Sources Block**
```funding
sources {
    github_sponsors "username" { ... }
    patreon "username" { ... }
    ko_fi "username" { ... }
    open_collective "username" { ... }
    buy_me_a_coffee "username" { ... }
    liberapay "username" { ... }
    paypal "username" { ... }
    custom "name" { url "..." ... }
}
```

### 5. **Tiers Block**
```funding
tiers {
    tier "Tier Name" {
        amount 25.00 USD
        description "Description"      // optional
        max_sponsors 10               // optional
        benefits [                    // optional
            "Benefit 1",
            "Benefit 2"
        ]
    }
}
```

### 6. **Goals Block**
```funding
goals {
    goal "Goal Name" {
        target 1000.00 USD
        current 250.00 USD           // optional, defaults to 0
        deadline "YYYY-MM-DD"        // optional
        description "Description"     // optional
    }
}
```

## Data Types

- **String**: Quoted strings `"text"`
- **Number**: Decimal numbers `25.00`
- **Currency**: Amount with currency `25.00 USD`
- **Boolean**: `true` or `false`
- **Date**: ISO format `"2024-06-01"`
- **Array**: `[item1, item2, ...]`
- **Enum values**: `both`, `one_time`, `recurring`, `USD`, `EUR`, etc.

## Comments

- Single line: `// comment`
- Multi line: `/* comment */`

## Platform Types

Supported funding platforms:
- `github_sponsors`
- `patreon`
- `ko_fi` 
- `open_collective`
- `buy_me_a_coffee`
- `liberapay`
- `paypal`
- `custom`

## Funding Types

- `one_time` - One-time donations only
- `recurring` - Recurring subscriptions only  
- `both` - Support both types

## Currencies

- `USD`, `EUR`, `GBP`, `CAD`, `AUD` 