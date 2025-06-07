"""
Funding Configuration Visualizer
Generates various graphical representations of funding configurations.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from metamodel.funding_metamodel import (
    FundingConfiguration, FundingSource, FundingPlatform, 
    Beneficiary, FundingTier, FundingGoal
)


class FundingVisualizer:
    """Main class for generating visual representations of funding configurations"""
    
    def __init__(self, config: FundingConfiguration):
        self.config = config
    
    def generate_mermaid_flowchart(self) -> str:
        """
        Generate a Mermaid flowchart showing the funding flow structure
        """
        lines = []
        lines.append("flowchart TD")
        lines.append("")
        
        # Project node
        project_id = "PROJECT"
        lines.append(f'    {project_id}["{self.config.project_name}"]')
        lines.append("")
        
        # Beneficiaries
        beneficiary_nodes = []
        for i, beneficiary in enumerate(self.config.beneficiaries):
            ben_id = f"BEN{i+1}"
            beneficiary_nodes.append(ben_id)
            lines.append(f'    {ben_id}["{beneficiary.name}<br/>🧑‍💻 {beneficiary.github_username}"]')
            lines.append(f'    {project_id} --> {ben_id}')
        
        lines.append("")
        
        # Funding sources grouped by platform
        platform_groups = {}
        for source in self.config.get_active_sources():
            platform = source.platform.value
            if platform not in platform_groups:
                platform_groups[platform] = []
            platform_groups[platform].append(source)
        
        # Platform nodes
        platform_nodes = []
        for platform, sources in platform_groups.items():
            platform_id = f"PLAT_{platform.upper()}"
            platform_nodes.append(platform_id)
            
            # Platform emoji mapping
            platform_emojis = {
                'github_sponsors': '💖',
                'patreon': '🎨',
                'ko_fi': '☕',
                'open_collective': '🤝',
                'tidelift': '🛡️',
                'liberapay': '💝',
                'custom': '🔗'
            }
            emoji = platform_emojis.get(platform, '💰')
            
            platform_name = platform.replace('_', ' ').title()
            if len(sources) == 1:
                lines.append(f'    {platform_id}["{emoji} {platform_name}<br/>{sources[0].username}"]')
            else:
                usernames = [s.username for s in sources[:3]]  # Show first 3
                if len(sources) > 3:
                    usernames.append(f"... +{len(sources)-3} more")
                lines.append(f'    {platform_id}["{emoji} {platform_name}<br/>{", ".join(usernames)}"]')
        
        lines.append("")
        
        # Connect platforms to beneficiaries
        for platform_id in platform_nodes:
            for ben_id in beneficiary_nodes:
                lines.append(f'    {platform_id} --> {ben_id}')
        
        lines.append("")
        
        # Sponsorship tiers (if any)
        if self.config.tiers:
            lines.append("    %% Sponsorship Tiers")
            for i, tier in enumerate(self.config.get_active_tiers()[:3]):  # Show first 3 tiers
                tier_id = f"TIER{i+1}"
                lines.append(f'    {tier_id}["{tier.name}<br/>💰 {tier.amount}"]')
                lines.append(f'    {tier_id} --> {project_id}')
        
        lines.append("")
        
        # Funding goals (if any)
        if self.config.goals:
            lines.append("    %% Funding Goals")
            for i, goal in enumerate(self.config.goals[:2]):  # Show first 2 goals
                goal_id = f"GOAL{i+1}"
                progress_emoji = "🎯" if goal.is_reached else "📈"
                lines.append(f'    {goal_id}["{progress_emoji} {goal.name}<br/>{goal.progress_percentage:.0f}% of {goal.target_amount}"]')
                lines.append(f'    {project_id} --> {goal_id}')
        
        return "\n".join(lines)
    
    def generate_mermaid_pie_chart(self) -> str:
        """
        Generate a Mermaid pie chart showing funding source distribution
        """
        # Count sources by platform
        platform_counts = {}
        for source in self.config.get_active_sources():
            platform = source.platform.value.replace('_', ' ').title()
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        if not platform_counts:
            return 'pie title "No Active Funding Sources"\n    "Inactive" : 1'
        
        lines = []
        lines.append(f'pie title "Funding Sources for {self.config.project_name}"')
        
        for platform, count in platform_counts.items():
            lines.append(f'    "{platform}" : {count}')
        
        return "\n".join(lines)
    
    def generate_mermaid_timeline(self) -> str:
        """
        Generate a Mermaid timeline showing funding goals progression
        """
        if not self.config.goals:
            return """timeline
    title Funding Timeline
    
    section Current
        No funding goals defined : No timeline available"""
        
        lines = []
        lines.append("timeline")
        lines.append(f'    title "{self.config.project_name} Funding Timeline"')
        lines.append("")
        
        # Group goals by status
        completed_goals = [g for g in self.config.goals if g.is_reached]
        ongoing_goals = [g for g in self.config.goals if not g.is_reached]
        
        if completed_goals:
            lines.append("    section Completed")
            for goal in completed_goals:
                lines.append(f'        {goal.name} : ✅ {goal.target_amount} reached')
        
        if ongoing_goals:
            lines.append("    section In Progress")
            for goal in ongoing_goals:
                progress = f"{goal.progress_percentage:.0f}%"
                deadline_str = ""
                if goal.deadline:
                    deadline_str = f" (by {goal.deadline.strftime('%Y-%m-%d')})"
                lines.append(f'        {goal.name} : 📈 {progress} of {goal.target_amount}{deadline_str}')
        
        return "\n".join(lines)
    
    def generate_mermaid_class_diagram(self) -> str:
        """
        Generate a Mermaid class diagram showing the funding structure
        """
        lines = []
        lines.append("classDiagram")
        lines.append("")
        
        # Project class
        lines.append("    class FundingConfiguration {")
        lines.append(f'        +string project_name "{self.config.project_name}"')
        lines.append(f'        +string description "{self.config.description[:30]}..."')
        lines.append(f'        +Currency preferred_currency')
        lines.append("        +getBeneficiaries()")
        lines.append("        +getFundingSources()")
        lines.append("        +getTiers()")
        lines.append("        +getGoals()")
        lines.append("    }")
        lines.append("")
        
        # Beneficiary class
        if self.config.beneficiaries:
            lines.append("    class Beneficiary {")
            lines.append("        +string name")
            lines.append("        +string github_username")
            lines.append("        +string email")
            lines.append("        +string website")
            lines.append("    }")
            lines.append("    FundingConfiguration ||--o{ Beneficiary")
            lines.append("")
        
        # Funding source class
        if self.config.funding_sources:
            lines.append("    class FundingSource {")
            lines.append("        +Platform platform")
            lines.append("        +string username")
            lines.append("        +FundingType funding_type")
            lines.append("        +boolean is_active")
            lines.append("        +string custom_url")
            lines.append("    }")
            lines.append("    FundingConfiguration ||--o{ FundingSource")
            lines.append("")
        
        # Funding tier class
        if self.config.tiers:
            lines.append("    class FundingTier {")
            lines.append("        +string name")
            lines.append("        +Money amount")
            lines.append("        +string description")
            lines.append("        +List~string~ benefits")
            lines.append("        +int max_sponsors")
            lines.append("    }")
            lines.append("    FundingConfiguration ||--o{ FundingTier")
            lines.append("")
        
        # Funding goal class
        if self.config.goals:
            lines.append("    class FundingGoal {")
            lines.append("        +string name")
            lines.append("        +Money target_amount")
            lines.append("        +Money current_amount")
            lines.append("        +float progress_percentage")
            lines.append("        +boolean is_reached")
            lines.append("        +Date deadline")
            lines.append("    }")
            lines.append("    FundingConfiguration ||--o{ FundingGoal")
        
        return "\n".join(lines)
    
    def generate_ascii_overview(self) -> str:
        """
        Generate an ASCII art overview of the funding configuration
        """
        lines = []
        lines.append("╔" + "═" * 60 + "╗")
        lines.append(f"║ {self.config.project_name.center(58)} ║")
        lines.append("╠" + "═" * 60 + "╣")
        
        # Description
        if self.config.description:
            desc = self.config.description[:56]
            lines.append(f"║ {desc:<58} ║")
            lines.append("║" + " " * 60 + "║")
        
        # Beneficiaries
        lines.append(f"║ 👥 Beneficiaries: {len(self.config.beneficiaries):<43} ║")
        for beneficiary in self.config.beneficiaries[:3]:
            name = f"   • {beneficiary.name} (@{beneficiary.github_username})"[:58]
            lines.append(f"║ {name:<58} ║")
        
        if len(self.config.beneficiaries) > 3:
            more = f"   ... and {len(self.config.beneficiaries) - 3} more"
            lines.append(f"║ {more:<58} ║")
        
        lines.append("║" + " " * 60 + "║")
        
        # Funding sources
        active_sources = self.config.get_active_sources()
        lines.append(f"║ 💰 Active Funding Sources: {len(active_sources):<35} ║")
        
        platform_counts = {}
        for source in active_sources:
            platform = source.platform.value.replace('_', ' ').title()
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        for platform, count in list(platform_counts.items())[:5]:
            source_line = f"   • {platform}: {count} source{'s' if count > 1 else ''}"
            lines.append(f"║ {source_line:<58} ║")
        
        if len(platform_counts) > 5:
            more = f"   ... and {len(platform_counts) - 5} more platforms"
            lines.append(f"║ {more:<58} ║")
        
        lines.append("║" + " " * 60 + "║")
        
        # Sponsorship tiers
        active_tiers = self.config.get_active_tiers()
        if active_tiers:
            lines.append(f"║ 🎯 Sponsorship Tiers: {len(active_tiers):<38} ║")
            for tier in active_tiers[:3]:
                tier_line = f"   • {tier.name}: {tier.amount}"[:58]
                lines.append(f"║ {tier_line:<58} ║")
            
            if len(active_tiers) > 3:
                more = f"   ... and {len(active_tiers) - 3} more tiers"
                lines.append(f"║ {more:<58} ║")
            
            lines.append("║" + " " * 60 + "║")
        
        # Funding goals
        if self.config.goals:
            lines.append(f"║ 📈 Funding Goals: {len(self.config.goals):<40} ║")
            for goal in self.config.goals[:2]:
                status = "✅" if goal.is_reached else "🔄"
                goal_line = f"   {status} {goal.name}: {goal.progress_percentage:.0f}%"[:58]
                lines.append(f"║ {goal_line:<58} ║")
            
            if len(self.config.goals) > 2:
                more = f"   ... and {len(self.config.goals) - 2} more goals"
                lines.append(f"║ {more:<58} ║")
        
        lines.append("╚" + "═" * 60 + "╝")
        
        return "\n".join(lines)
    
    def generate_funding_matrix(self) -> str:
        """
        Generate a matrix showing the relationship between beneficiaries and funding sources
        """
        if not self.config.beneficiaries or not self.config.funding_sources:
            return "No beneficiaries or funding sources to display matrix"
        
        lines = []
        lines.append("Funding Sources Matrix")
        lines.append("=" * 50)
        lines.append()
        
        # Header with beneficiary names
        header = "Platform".ljust(15)
        for beneficiary in self.config.beneficiaries[:4]:  # Limit to 4 for readability
            header += beneficiary.name[:10].ljust(12)
        lines.append(header)
        lines.append("-" * len(header))
        
        # Group sources by platform
        platform_groups = {}
        for source in self.config.get_active_sources():
            platform = source.platform.value.replace('_', ' ').title()
            if platform not in platform_groups:
                platform_groups[platform] = []
            platform_groups[platform].append(source)
        
        # Show relationship (simplified - all active sources benefit all beneficiaries)
        for platform, sources in platform_groups.items():
            row = platform[:14].ljust(15)
            for _ in self.config.beneficiaries[:4]:
                row += "✓".ljust(12)
            lines.append(row)
        
        return "\n".join(lines)


def visualize_funding_config(config: FundingConfiguration, diagram_type: str = "flowchart") -> str:
    """
    Convenience function to generate visualizations
    
    Args:
        config: The funding configuration to visualize
        diagram_type: Type of visualization ('flowchart', 'pie', 'timeline', 'class', 'ascii', 'matrix')
    
    Returns:
        The generated visualization content
    """
    visualizer = FundingVisualizer(config)
    
    if diagram_type == "flowchart":
        return visualizer.generate_mermaid_flowchart()
    elif diagram_type == "pie":
        return visualizer.generate_mermaid_pie_chart()
    elif diagram_type == "timeline":
        return visualizer.generate_mermaid_timeline()
    elif diagram_type == "class":
        return visualizer.generate_mermaid_class_diagram()
    elif diagram_type == "ascii":
        return visualizer.generate_ascii_overview()
    elif diagram_type == "matrix":
        return visualizer.generate_funding_matrix()
    else:
        raise ValueError(f"Unsupported diagram type: {diagram_type}")


def generate_all_visualizations(config: FundingConfiguration) -> Dict[str, str]:
    """
    Generate all available visualizations for a funding configuration
    
    Returns:
        Dictionary mapping visualization type to content
    """
    visualizer = FundingVisualizer(config)
    
    return {
        "flowchart": visualizer.generate_mermaid_flowchart(),
        "pie_chart": visualizer.generate_mermaid_pie_chart(),
        "timeline": visualizer.generate_mermaid_timeline(),
        "class_diagram": visualizer.generate_mermaid_class_diagram(),
        "ascii_overview": visualizer.generate_ascii_overview(),
        "funding_matrix": visualizer.generate_funding_matrix()
    } 