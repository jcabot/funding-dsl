"""
Interactive Funding Configuration Diagrams
Creates and displays visual diagrams in the chat interface.
"""

from typing import Dict, Any
from metamodel.funding_metamodel import FundingConfiguration
from .funding_visualizer import FundingVisualizer


class InteractiveDiagramGenerator:
    """Generator for interactive diagrams that can be displayed in chat"""
    
    def __init__(self, config: FundingConfiguration):
        self.config = config
        self.visualizer = FundingVisualizer(config)
    
    def create_funding_flow_diagram(self) -> str:
        """
        Create an interactive Mermaid flowchart showing funding flow
        """
        return self.visualizer.generate_mermaid_flowchart()
    
    def create_platform_distribution_chart(self) -> str:
        """
        Create a pie chart showing platform distribution
        """
        return self.visualizer.generate_mermaid_pie_chart()
    
    def create_timeline_diagram(self) -> str:
        """
        Create a timeline showing funding goals progression
        """
        return self.visualizer.generate_mermaid_timeline()
    
    def create_structure_diagram(self) -> str:
        """
        Create a class diagram showing the funding configuration structure
        """
        return self.visualizer.generate_mermaid_class_diagram()
    
    def get_ascii_summary(self) -> str:
        """
        Get ASCII art summary for text-based display
        """
        return self.visualizer.generate_ascii_overview()
    
    def analyze_configuration(self) -> Dict[str, Any]:
        """
        Analyze the configuration and return key metrics for visualization
        """
        active_sources = self.config.get_active_sources()
        active_tiers = self.config.get_active_tiers()
        
        # Platform analysis
        platform_counts = {}
        for source in active_sources:
            platform = source.platform.value.replace('_', ' ').title()
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        # Goal analysis
        goal_analysis = {}
        if self.config.goals:
            total_target = sum(goal.target_amount.value for goal in self.config.goals)
            total_current = sum(goal.current_amount.value for goal in self.config.goals)
            overall_progress = (total_current / total_target * 100) if total_target > 0 else 0
            
            goal_analysis = {
                "total_goals": len(self.config.goals),
                "completed_goals": len([g for g in self.config.goals if g.is_reached]),
                "total_target_amount": total_target,
                "total_current_amount": total_current,
                "overall_progress": overall_progress
            }
        
        # Tier analysis
        tier_analysis = {}
        if active_tiers:
            tier_prices = [tier.amount.value for tier in active_tiers]
            tier_analysis = {
                "total_tiers": len(active_tiers),
                "min_tier_price": min(tier_prices),
                "max_tier_price": max(tier_prices),
                "avg_tier_price": sum(tier_prices) / len(tier_prices)
            }
        
        return {
            "project_name": self.config.project_name,
            "beneficiaries_count": len(self.config.beneficiaries),
            "total_funding_sources": len(self.config.funding_sources),
            "active_funding_sources": len(active_sources),
            "platform_distribution": platform_counts,
            "goal_analysis": goal_analysis,
            "tier_analysis": tier_analysis,
            "has_github_sponsors": any(s.platform.value == 'github_sponsors' for s in active_sources),
            "has_recurring_funding": any(s.funding_type.value == 'recurring' for s in active_sources),
            "has_one_time_funding": any(s.funding_type.value == 'one_time' for s in active_sources)
        }


def create_funding_diagrams(config: FundingConfiguration) -> Dict[str, str]:
    """
    Create all available diagrams for a funding configuration
    
    Returns:
        Dictionary mapping diagram type to Mermaid content
    """
    generator = InteractiveDiagramGenerator(config)
    
    return {
        "funding_flow": generator.create_funding_flow_diagram(),
        "platform_distribution": generator.create_platform_distribution_chart(),
        "timeline": generator.create_timeline_diagram(),
        "structure": generator.create_structure_diagram()
    }


def display_configuration_summary(config: FundingConfiguration) -> str:
    """
    Create a comprehensive text summary with ASCII art
    """
    generator = InteractiveDiagramGenerator(config)
    analysis = generator.analyze_configuration()
    
    summary_lines = []
    summary_lines.append("🎨 FUNDING CONFIGURATION VISUAL SUMMARY")
    summary_lines.append("=" * 50)
    summary_lines.append("")
    
    # ASCII overview
    summary_lines.append(generator.get_ascii_summary())
    summary_lines.append("")
    
    # Analysis summary
    summary_lines.append("📊 CONFIGURATION ANALYSIS")
    summary_lines.append("-" * 30)
    summary_lines.append(f"Project: {analysis['project_name']}")
    summary_lines.append(f"Beneficiaries: {analysis['beneficiaries_count']}")
    summary_lines.append(f"Funding Sources: {analysis['active_funding_sources']}/{analysis['total_funding_sources']} active")
    summary_lines.append("")
    
    # Platform breakdown
    if analysis['platform_distribution']:
        summary_lines.append("Platform Distribution:")
        for platform, count in analysis['platform_distribution'].items():
            summary_lines.append(f"  • {platform}: {count} source{'s' if count > 1 else ''}")
        summary_lines.append("")
    
    # Goal progress
    if analysis['goal_analysis']:
        goal_data = analysis['goal_analysis']
        summary_lines.append("Goal Progress:")
        summary_lines.append(f"  • Total Goals: {goal_data['total_goals']}")
        summary_lines.append(f"  • Completed: {goal_data['completed_goals']}")
        summary_lines.append(f"  • Overall Progress: {goal_data['overall_progress']:.1f}%")
        summary_lines.append("")
    
    # Tier information
    if analysis['tier_analysis']:
        tier_data = analysis['tier_analysis']
        summary_lines.append("Sponsorship Tiers:")
        summary_lines.append(f"  • Total Tiers: {tier_data['total_tiers']}")
        summary_lines.append(f"  • Price Range: {tier_data['min_tier_price']:.0f} - {tier_data['max_tier_price']:.0f}")
        summary_lines.append(f"  • Average Price: {tier_data['avg_tier_price']:.0f}")
        summary_lines.append("")
    
    # Recommendations
    summary_lines.append("💡 RECOMMENDATIONS")
    summary_lines.append("-" * 20)
    
    if not analysis['has_github_sponsors']:
        summary_lines.append("  • Consider adding GitHub Sponsors for better integration")
    
    if not analysis['has_recurring_funding']:
        summary_lines.append("  • Add recurring funding options for sustainable income")
    
    if analysis['platform_distribution'] and len(analysis['platform_distribution']) == 1:
        summary_lines.append("  • Diversify funding platforms to reduce dependency")
    
    if not analysis['goal_analysis']:
        summary_lines.append("  • Set funding goals to track progress and motivate supporters")
    
    return "\n".join(summary_lines) 