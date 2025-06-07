grammar FundingDSL;

// Entry point
fundingConfiguration
    : fundingBlock EOF
    ;

// Main funding block
fundingBlock
    : FUNDING STRING '{' configurationContent '}'
    ;

configurationContent
    : configurationElement*
    ;

configurationElement
    : descriptionElement
    | currencyElement  
    | minAmountElement
    | maxAmountElement
    | beneficiariesBlock
    | sourcesBlock
    | tiersBlock
    | goalsBlock
    ;

// Basic configuration elements
descriptionElement
    : DESCRIPTION STRING
    ;

currencyElement
    : CURRENCY currencyType
    ;

minAmountElement
    : MIN_AMOUNT NUMBER
    ;

maxAmountElement
    : MAX_AMOUNT NUMBER
    ;

// Beneficiaries block
beneficiariesBlock
    : BENEFICIARIES '{' beneficiaryElement* '}'
    ;

beneficiaryElement
    : BENEFICIARY STRING '{' beneficiaryProperty* '}'
    ;

beneficiaryProperty
    : emailProperty
    | githubProperty
    | websiteProperty
    | descriptionProperty
    ;

emailProperty
    : EMAIL STRING
    ;

githubProperty
    : GITHUB STRING
    ;

websiteProperty
    : WEBSITE STRING
    ;

descriptionProperty
    : DESCRIPTION STRING
    ;

// Sources block
sourcesBlock
    : SOURCES '{' sourceElement* '}'
    ;

sourceElement
    : platformSource
    | customSource
    ;

platformSource
    : platformType STRING '{' sourceProperty* '}'
    ;

customSource
    : CUSTOM STRING '{' customSourceProperty* '}'
    ;

sourceProperty
    : typeProperty
    | activeProperty
    | configProperty
    ;

customSourceProperty
    : urlProperty
    | typeProperty
    | activeProperty
    | configProperty
    ;

typeProperty
    : TYPE fundingType
    ;

activeProperty
    : ACTIVE booleanValue
    ;

urlProperty
    : URL STRING
    ;

configProperty
    : CONFIG '{' configKeyValue* '}'
    ;

configKeyValue
    : STRING STRING
    ;

// Tiers block
tiersBlock
    : TIERS '{' tierElement* '}'
    ;

tierElement
    : TIER STRING '{' tierProperty* '}'
    ;

tierProperty
    : amountProperty
    | descriptionProperty
    | maxSponsorsProperty
    | benefitsProperty
    ;

amountProperty
    : AMOUNT amount
    ;

maxSponsorsProperty
    : MAX_SPONSORS NUMBER
    ;

benefitsProperty
    : BENEFITS '[' stringList? ']'
    ;

stringList
    : STRING (',' STRING)*
    ;

// Goals block
goalsBlock
    : GOALS '{' goalElement* '}'
    ;

goalElement
    : GOAL STRING '{' goalProperty* '}'
    ;

goalProperty
    : targetProperty
    | currentProperty
    | deadlineProperty
    | descriptionProperty
    ;

targetProperty
    : TARGET amount
    ;

currentProperty
    : CURRENT amount
    ;

deadlineProperty
    : DEADLINE STRING
    ;

// Data types
amount
    : NUMBER currencyType
    ;

currencyType
    : USD | EUR | GBP | CAD | AUD
    ;

platformType
    : GITHUB_SPONSORS
    | PATREON
    | KO_FI
    | OPEN_COLLECTIVE
    | BUY_ME_A_COFFEE
    | LIBERAPAY
    | PAYPAL
    | TIDELIFT
    | ISSUEHUNT
    | COMMUNITY_BRIDGE
    | POLAR
    | THANKS_DEV
    ;

fundingType
    : ONE_TIME
    | RECURRING
    | BOTH
    ;

booleanValue
    : TRUE
    | FALSE
    ;

// Keywords
FUNDING: 'funding';
DESCRIPTION: 'description';
CURRENCY: 'currency';
MIN_AMOUNT: 'min_amount';
MAX_AMOUNT: 'max_amount';
BENEFICIARIES: 'beneficiaries';
BENEFICIARY: 'beneficiary';
EMAIL: 'email';
GITHUB: 'github';
WEBSITE: 'website';
SOURCES: 'sources';
GITHUB_SPONSORS: 'github_sponsors';
PATREON: 'patreon';
KO_FI: 'ko_fi';
OPEN_COLLECTIVE: 'open_collective';
BUY_ME_A_COFFEE: 'buy_me_a_coffee';
LIBERAPAY: 'liberapay';
PAYPAL: 'paypal';
TIDELIFT: 'tidelift';
ISSUEHUNT: 'issuehunt';
COMMUNITY_BRIDGE: 'community_bridge';
POLAR: 'polar';
THANKS_DEV: 'thanks_dev';
CUSTOM: 'custom';
TYPE: 'type';
ACTIVE: 'active';
URL: 'url';
CONFIG: 'config';
TIERS: 'tiers';
TIER: 'tier';
AMOUNT: 'amount';
MAX_SPONSORS: 'max_sponsors';
BENEFITS: 'benefits';
GOALS: 'goals';
GOAL: 'goal';
TARGET: 'target';
CURRENT: 'current';
DEADLINE: 'deadline';

// Enum values
USD: 'USD';
EUR: 'EUR';
GBP: 'GBP';
CAD: 'CAD';
AUD: 'AUD';
ONE_TIME: 'one_time';
RECURRING: 'recurring';
BOTH: 'both';
TRUE: 'true';
FALSE: 'false';

// Literals
STRING: '"' (~["\r\n])* '"';
NUMBER: [0-9]+ ('.' [0-9]+)?;

// Whitespace and comments
WS: [ \t\r\n]+ -> skip;
SINGLE_LINE_COMMENT: '//' ~[\r\n]* -> skip;
MULTI_LINE_COMMENT: '/*' .*? '*/' -> skip;

// Delimiters  
'{': '{';
'}': '}';
'[': '[';
']': ']';
',': ','; 