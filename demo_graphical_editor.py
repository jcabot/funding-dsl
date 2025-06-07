"""
Demo: Funding DSL Graphical Model Editor
Launch the visual editor for creating funding configurations.
"""

import sys
import os

# Add the project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graphical.graphical_editor import GraphicalFundingEditor


def main():
    """Launch the graphical editor with instructions"""
    
    print("=" * 60)
    print("🎨 FUNDING DSL - GRAPHICAL MODEL EDITOR")
    print("=" * 60)
    print()
    print("Welcome to the visual funding configuration editor!")
    print()
    print("HOW TO USE:")
    print("1. Start by adding a 📦 Project element (required)")
    print("2. Add funding elements using the toolbar buttons:")
    print("   👤 Beneficiary - People who receive funding")
    print("   💰 Funding Source - Platforms like GitHub Sponsors, Patreon")
    print("   🎯 Tier - Sponsorship levels with pricing and benefits")
    print("   📈 Goal - Funding targets and milestones")
    print()
    print("3. Double-click elements to edit their properties")
    print("4. Drag elements to reposition them")
    print("5. Right-click for context menu options")
    print("6. Use 💾 Save Model to save your visual design")
    print("7. Use 📄 Export DSL to convert to metamodel objects")
    print()
    print("KEYBOARD SHORTCUTS:")
    print("• Double-click: Edit element properties")
    print("• Right-click: Context menu")
    print("• Click & drag: Move elements")
    print()
    print("Starting the graphical editor...")
    print("=" * 60)
    
    # Launch the editor
    try:
        editor = GraphicalFundingEditor()
        editor.run()
    except Exception as e:
        print(f"Error launching editor: {e}")
        print("Make sure you have tkinter installed (usually comes with Python)")


if __name__ == "__main__":
    main() 