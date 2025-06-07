// Minimal Funding Configuration
// Equivalent to GitHub's funding.yml example:
// github: [octocat, surftocat]
// patreon: octocat
// tidelift: npm/octo-package
// custom: ["https://www.paypal.me/octocat", octocat.com]

funding "octo-package" {
    description "A minimal funding configuration example"
    currency USD
    
    beneficiaries {
        beneficiary "Octocat" {
            github "octocat"
            description "Primary maintainer"
        }
        
        beneficiary "Surftocat" {
            github "surftocat"
            description "Co-maintainer"
        }
    }
    
    sources {
        // GitHub Sponsors - multiple accounts
        github_sponsors "octocat" {
            type both
            active true
        }
        
        github_sponsors "surftocat" {
            type both
            active true
        }
        
        // Patreon
        patreon "octocat" {
            type recurring
            active true
        }
        
        // Tidelift (using custom platform for npm package)
        custom "tidelift-npm-octo-package" {
            type recurring
            active true
            url "https://tidelift.com/funding/github/npm/octo-package"
            config {
                "platform" "tidelift"
                "package" "npm/octo-package"
            }
        }
        
        // Custom funding URLs
        custom "paypal-octocat" {
            type one_time
            active true
            url "https://www.paypal.me/octocat"
            config {
                "platform" "paypal"
                "type" "personal"
            }
        }
        
        custom "octocat-website" {
            type both
            active true
            url "https://octocat.com"
            config {
                "platform" "website"
                "type" "personal"
            }
        }
    }
} 