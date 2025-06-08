funding "octo-package" {
    description "Funding configuration matching TEST-FUNDING.yml"
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
        github_sponsors "octocat" {
            type both
            active true
        }
        
        github_sponsors "surftocat" {
            type both
            active true
        }
        
        patreon "octocat" {
            type recurring
            active true
        }
        
        tidelift "npm/octo-package" {
            type recurring
            active true
        }
        
        custom "paypal-donation" {
            url "https://www.paypal.me/octocat"
            type one_time
            active true
        }
        
        custom "website-donation" {
            url "octocat.com"
            type both
            active true
        }
    }
} 