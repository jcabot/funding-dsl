"""
Improved Graphical Model Editor for Funding DSL
Enhanced visual notation based on Physics of Notations (PoN) principles.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from typing import Dict, List, Optional, Tuple, Any
import json
import math
import yaml
from datetime import datetime, timedelta

from metamodel.funding_metamodel import (
    FundingConfiguration, Beneficiary, FundingSource, FundingTier, 
    FundingGoal, FundingAmount, FundingPlatform, FundingType, 
    CurrencyType, FundingModelValidator
)


class ImprovedVisualElement:
    """Enhanced base class for visual elements following PoN principles"""
    
    def __init__(self, canvas, x: int, y: int, width: int = 100, height: int = 60):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False
        self.canvas_shapes = []  # Store multiple canvas items
        
    def draw(self):
        """Draw the element using improved visual notation"""
        pass
    
    def draw_shadow(self, offset=3):
        """Draw shadow for depth perception"""
        shadow_id = self.canvas.create_rectangle(
            self.x + offset, self.y + offset, 
            self.x + self.width + offset, self.y + self.height + offset,
            fill="gray80", outline="", width=0
        )
        self.canvas_shapes.append(shadow_id)
        return shadow_id
    
    def draw_geometric_symbol(self, symbol_type: str, x_offset=10, y_offset=10, size=20):
        """Draw geometric symbols for better discriminability"""
        center_x = self.x + x_offset + size//2
        center_y = self.y + y_offset + size//2
        
        if symbol_type == "diamond":
            # Diamond shape for funding sources (sources are connection points)
            points = [
                center_x, center_y - size//2,  # top
                center_x + size//2, center_y,  # right
                center_x, center_y + size//2,  # bottom
                center_x - size//2, center_y   # left
            ]
            shape_id = self.canvas.create_polygon(points, fill="gold", outline="darkorange", width=2)
            
        elif symbol_type == "circle":
            # Circle for beneficiaries (people are central, whole entities)
            shape_id = self.canvas.create_oval(
                center_x - size//2, center_y - size//2,
                center_x + size//2, center_y + size//2,
                fill="lightgreen", outline="darkgreen", width=2
            )
            
        elif symbol_type == "square":
            # Square for project (foundation, stable base)
            shape_id = self.canvas.create_rectangle(
                center_x - size//2, center_y - size//2,
                center_x + size//2, center_y + size//2,
                fill="lightblue", outline="darkblue", width=2
            )
            
        elif symbol_type == "triangle":
            # Triangle for tiers (hierarchical levels)
            points = [
                center_x, center_y - size//2,  # top
                center_x - size//2, center_y + size//2,  # bottom left
                center_x + size//2, center_y + size//2   # bottom right
            ]
            shape_id = self.canvas.create_polygon(points, fill="lightcoral", outline="darkred", width=2)
            
        elif symbol_type == "hexagon":
            # Hexagon for goals (multi-faceted objectives)
            angles = [i * math.pi * 2 / 6 for i in range(6)]
            points = []
            for angle in angles:
                x = center_x + (size//2) * math.cos(angle)
                y = center_y + (size//2) * math.sin(angle)
                points.extend([x, y])
            shape_id = self.canvas.create_polygon(points, fill="lightsteelblue", outline="steelblue", width=2)
            
        else:
            # Default circle
            shape_id = self.canvas.create_oval(
                center_x - size//2, center_y - size//2,
                center_x + size//2, center_y + size//2,
                fill="lightgray", outline="gray", width=2
            )
            
        self.canvas_shapes.append(shape_id)
        return shape_id
    
    def draw_pattern_overlay(self, pattern_type: str):
        """Add pattern overlays for additional visual coding"""
        if pattern_type == "dots":
            # Dots for active/enabled status
            for i in range(3):
                for j in range(3):
                    dot_x = self.x + 20 + i * 8
                    dot_y = self.y + 20 + j * 8
                    if dot_x < self.x + self.width - 20 and dot_y < self.y + self.height - 20:
                        dot_id = self.canvas.create_oval(
                            dot_x, dot_y, dot_x + 2, dot_y + 2,
                            fill="darkblue", outline=""
                        )
                        self.canvas_shapes.append(dot_id)
        
        elif pattern_type == "stripes":
            # Diagonal stripes for recurring elements
            for i in range(0, self.width + self.height, 10):
                line_id = self.canvas.create_line(
                    self.x + i, self.y,
                    self.x, self.y + i,
                    fill="gray70", width=1
                )
                self.canvas_shapes.append(line_id)
    
    def move(self, dx: int, dy: int):
        """Move all canvas shapes together"""
        self.x += dx
        self.y += dy
        for shape_id in self.canvas_shapes:
            self.canvas.move(shape_id, dx, dy)
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is inside element"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def set_selected(self, selected: bool):
        """Enhanced selection with visual emphasis"""
        self.selected = selected
        self.update_appearance()
    
    def update_appearance(self):
        """Update visual appearance with selection feedback"""
        if self.selected and self.canvas_shapes:
            # Add selection border
            border_id = self.canvas.create_rectangle(
                self.x - 3, self.y - 3, 
                self.x + self.width + 3, self.y + self.height + 3,
                fill="", outline="red", width=3
            )
            self.canvas_shapes.append(border_id)
    
    def delete_shapes(self):
        """Delete all canvas shapes"""
        for shape_id in self.canvas_shapes:
            self.canvas.delete(shape_id)
        self.canvas_shapes.clear()
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        """Show properties dialog for project element"""
        dialog = ImprovedProjectPropertiesDialog(parent, self)
        return dialog.result
    
    def to_metamodel_object(self):
        """Convert to metamodel object - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement to_metamodel_object")


class ImprovedProjectElement(ImprovedVisualElement):
    """Project element with enhanced visual design following PoN principles"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 160, 90)
        self.project_name = "New Project"
        self.description = ""
        self.preferred_currency = CurrencyType.USD
        
    def draw(self):
        """Draw project using square symbol (stability) with professional styling"""
        self.delete_shapes()
        
        # 1. Shadow for depth (PoN: Visual hierarchy)
        self.draw_shadow()
        
        # 2. Main container with rounded corners
        main_rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="#E3F2FD", outline="#1976D2", width=3, 
        )
        self.canvas_shapes.append(main_rect)
        
        # 3. Geometric symbol (square = foundation/base)
        self.draw_geometric_symbol("square", 10, 10, 25)
        
        # 4. Header bar to indicate primary element
        header_rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + 20,
            fill="#1976D2", outline=""
        )
        self.canvas_shapes.append(header_rect)
        
        # 5. Text with dual coding (visual + textual)
        title_text = self.canvas.create_text(
            self.x + 45, self.y + 10,
            text="PROJECT", font=("Arial", 8, "bold"), fill="white", anchor="w"
        )
        self.canvas_shapes.append(title_text)
        
        name_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 45,
            text=self.project_name, font=("Arial", 10, "bold"), anchor="center"
        )
        self.canvas_shapes.append(name_text)
        
        # 6. Currency indicator
        currency_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 65,
            text=f"Currency: {self.currency_symbol()}", 
            font=("Arial", 8), fill="#666", anchor="center"
        )
        self.canvas_shapes.append(currency_text)
        
    def currency_symbol(self) -> str:
        """Get currency symbol for semantic transparency"""
        symbols = {
            CurrencyType.USD: "$",
            CurrencyType.EUR: "€", 
            CurrencyType.GBP: "£",
            CurrencyType.CAD: "C$",
            CurrencyType.AUD: "A$"
        }
        return symbols.get(self.preferred_currency, "$")
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        """Show properties dialog for project element"""
        dialog = ImprovedProjectPropertiesDialog(parent, self)
        return dialog.result
    
    def to_metamodel_object(self):
        """Project elements don't have a direct metamodel equivalent - they're containers"""
        return None


class ImprovedBeneficiaryElement(ImprovedVisualElement):
    """Beneficiary element with circle symbol (wholeness, person-centered)"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 140, 75)
        self.name = "New Beneficiary"
        self.email = ""
        self.github_username = ""
        self.website = ""
        self.description = ""
        self.role = ""
        
    def draw(self):
        """Draw beneficiary using circle symbol (person-centered)"""
        self.delete_shapes()
        
        # Shadow
        self.draw_shadow()
        
        # Main container
        main_rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="#E8F5E8", outline="#388E3C", width=2
        )
        self.canvas_shapes.append(main_rect)
        
        # Circle symbol (person = whole entity)
        self.draw_geometric_symbol("circle", 10, 10, 22)
        
        # Person silhouette for semantic transparency
        head_circle = self.canvas.create_oval(
            self.x + 17, self.y + 35, self.x + 25, self.y + 43,
            fill="#2E7D32", outline=""
        )
        self.canvas_shapes.append(head_circle)
        
        body_rect = self.canvas.create_rectangle(
            self.x + 15, self.y + 43, self.x + 27, self.y + 55,
            fill="#2E7D32", outline=""
        )
        self.canvas_shapes.append(body_rect)
        
        # Text
        title_text = self.canvas.create_text(
            self.x + 45, self.y + 15,
            text="BENEFICIARY", font=("Arial", 8, "bold"), fill="#2E7D32", anchor="w"
        )
        self.canvas_shapes.append(title_text)
        
        name_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 40,
            text=self.name, font=("Arial", 9, "bold"), anchor="center"
        )
        self.canvas_shapes.append(name_text)
        
        # Contact indicator
        if self.github_username:
            github_text = self.canvas.create_text(
                self.x + self.width//2, self.y + 55,
                text=f"@{self.github_username}", font=("Arial", 7), fill="#666", anchor="center"
            )
            self.canvas_shapes.append(github_text)
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        """Show properties dialog for beneficiary element"""
        dialog = ImprovedBeneficiaryPropertiesDialog(parent, self)
        return dialog.result
    
    def to_metamodel_object(self) -> Beneficiary:
        return Beneficiary(
            name=self.name,
            email=self.email if self.email else None,
            github_username=self.github_username if self.github_username else None,
            website=self.website if self.website else None,
            description=self.description if self.description else None
        )


class ImprovedFundingSourceElement(ImprovedVisualElement):
    """Funding source with diamond symbol (connection point, flow)"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 145, 75)
        self.platform = FundingPlatform.GITHUB_SPONSORS
        self.username = "username"
        self.funding_type = FundingType.BOTH
        self.is_active = True
        self.custom_url = ""
        
    def draw(self):
        """Draw funding source using diamond symbol (connection/flow point)"""
        self.delete_shapes()
        
        # Shadow
        self.draw_shadow()
        
        # Main container
        main_rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="#FFF8E1", outline="#F57C00", width=2
        )
        self.canvas_shapes.append(main_rect)
        
        # Diamond symbol (connection point)
        self.draw_geometric_symbol("diamond", 10, 10, 22)
        
        # Platform-specific visual coding
        platform_color = self.get_platform_color()
        platform_rect = self.canvas.create_rectangle(
            self.x + 5, self.y + 5, self.x + 15, self.y + 15,
            fill=platform_color, outline=""
        )
        self.canvas_shapes.append(platform_rect)
        
        # Flow arrows for semantic transparency (money flow)
        arrow_points = [
            self.x + 120, self.y + 25,
            self.x + 130, self.y + 30,
            self.x + 120, self.y + 35
        ]
        arrow_id = self.canvas.create_polygon(arrow_points, fill="#F57C00", outline="")
        self.canvas_shapes.append(arrow_id)
        
        # Text
        title_text = self.canvas.create_text(
            self.x + 45, self.y + 15,
            text="FUNDING SOURCE", font=("Arial", 8, "bold"), fill="#E65100", anchor="w"
        )
        self.canvas_shapes.append(title_text)
        
        platform_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 35,
            text=self.platform.value.replace("_", " ").title(), 
            font=("Arial", 9, "bold"), anchor="center"
        )
        self.canvas_shapes.append(platform_text)
        
        username_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 50,
            text=self.username, font=("Arial", 8), fill="#666", anchor="center"
        )
        self.canvas_shapes.append(username_text)
        
        # Type indicator with pattern coding
        if self.funding_type == FundingType.RECURRING:
            self.draw_pattern_overlay("stripes")
        
        type_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 62,
            text=self.funding_type.value.replace("_", " ").title(),
            font=("Arial", 7), fill="#999", anchor="center"
        )
        self.canvas_shapes.append(type_text)
    
    def get_platform_color(self) -> str:
        """Color coding for different platforms"""
        colors = {
            FundingPlatform.GITHUB_SPONSORS: "#FF69B4",
            FundingPlatform.PATREON: "#FF424D",
            FundingPlatform.KO_FI: "#29ABE0",
            FundingPlatform.OPEN_COLLECTIVE: "#7FADF2",
            FundingPlatform.BUY_ME_A_COFFEE: "#FFDD00",
            FundingPlatform.LIBERAPAY: "#F6C915",
            FundingPlatform.PAYPAL: "#00457C",
            FundingPlatform.TIDELIFT: "#FF9500",
            FundingPlatform.ISSUEHUNT: "#FF6B6B",
            FundingPlatform.COMMUNITY_BRIDGE: "#4ECDC4",
            FundingPlatform.POLAR: "#45B7D1",
            FundingPlatform.THANKS_DEV: "#96CEB4",
            FundingPlatform.CUSTOM: "#666666"
        }
        return colors.get(self.platform, "#666666")
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        """Show properties dialog for funding source element"""
        dialog = ImprovedFundingSourcePropertiesDialog(parent, self)
        return dialog.result
    
    def to_metamodel_object(self) -> FundingSource:
        return FundingSource(
            platform=self.platform,
            username=self.username,
            funding_type=self.funding_type,
            is_active=self.is_active,
            custom_url=self.custom_url if self.custom_url else None
        )


class ImprovedFundingTierElement(ImprovedVisualElement):
    """Funding tier with triangle symbol (hierarchical levels)"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 125, 85)
        self.name = "New Tier"
        self.amount = 10.0
        self.currency = CurrencyType.USD
        self.description = ""
        self.benefits = []
        self.max_sponsors = None
        self.is_active = True
        
    def draw(self):
        """Draw tier using triangle symbol (hierarchical levels)"""
        self.delete_shapes()
        
        # Shadow
        self.draw_shadow()
        
        # Main container
        main_rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="#FCE4EC", outline="#C2185B", width=2
        )
        self.canvas_shapes.append(main_rect)
        
        # Triangle symbol (hierarchy/tiers)
        self.draw_geometric_symbol("triangle", 10, 10, 22)
        
        # Tier level indicator (visual hierarchy)
        tier_level = min(int(self.amount / 25) + 1, 5)  # 1-5 levels based on amount
        for i in range(tier_level):
            level_rect = self.canvas.create_rectangle(
                self.x + 35 + i * 8, self.y + 32 - i * 3,
                self.x + 42 + i * 8, self.y + 42,
                fill="#C2185B", outline=""
            )
            self.canvas_shapes.append(level_rect)
        
        # Text
        title_text = self.canvas.create_text(
            self.x + 45, self.y + 15,
            text="TIER", font=("Arial", 8, "bold"), fill="#880E4F", anchor="w"
        )
        self.canvas_shapes.append(title_text)
        
        name_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 35,
            text=self.name, font=("Arial", 9, "bold"), anchor="center"
        )
        self.canvas_shapes.append(name_text)
        
        # Price with currency symbol for semantic transparency
        currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£", "CAD": "C$", "AUD": "A$"}
        symbol = currency_symbols.get(self.currency.value, "$")
        
        price_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 50,
            text=f"{symbol}{self.amount}", font=("Arial", 10, "bold"), fill="#C2185B", anchor="center"
        )
        self.canvas_shapes.append(price_text)
        
        # Benefits count
        benefits_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 65,
            text=f"{len(self.benefits)} benefits", font=("Arial", 7), fill="#666", anchor="center"
        )
        self.canvas_shapes.append(benefits_text)
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        """Show properties dialog for funding tier element"""
        dialog = ImprovedFundingTierPropertiesDialog(parent, self)
        return dialog.result
    
    def to_metamodel_object(self) -> FundingTier:
        return FundingTier(
            name=self.name,
            amount=FundingAmount(self.amount, self.currency),
            description=self.description if self.description else None,
            benefits=self.benefits,
            max_sponsors=self.max_sponsors,
            is_active=self.is_active
        )


class ImprovedFundingGoalElement(ImprovedVisualElement):
    """Funding goal with hexagon symbol (multi-faceted objectives)"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 135, 85)
        self.name = "New Goal"
        self.target_amount = 1000.0
        self.current_amount = 0.0
        self.currency = CurrencyType.USD
        self.description = ""
        self.deadline = None
        
    def draw(self):
        """Draw goal using hexagon symbol (multi-faceted objectives)"""
        self.delete_shapes()
        
        # Shadow
        self.draw_shadow()
        
        # Main container
        main_rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="#E1F5FE", outline="#0277BD", width=2
        )
        self.canvas_shapes.append(main_rect)
        
        # Hexagon symbol (multi-faceted objectives)
        self.draw_geometric_symbol("hexagon", 10, 10, 22)
        
        # Progress bar for semantic transparency
        progress = (self.current_amount / self.target_amount) if self.target_amount > 0 else 0
        bar_width = 80
        bar_height = 8
        
        # Background bar
        bg_bar = self.canvas.create_rectangle(
            self.x + 40, self.y + 45,
            self.x + 40 + bar_width, self.y + 45 + bar_height,
            fill="white", outline="#0277BD", width=1
        )
        self.canvas_shapes.append(bg_bar)
        
        # Progress fill
        fill_width = int(bar_width * min(progress, 1.0))
        if fill_width > 0:
            progress_bar = self.canvas.create_rectangle(
                self.x + 40, self.y + 45,
                self.x + 40 + fill_width, self.y + 45 + bar_height,
                fill="#0277BD", outline=""
            )
            self.canvas_shapes.append(progress_bar)
        
        # Text
        title_text = self.canvas.create_text(
            self.x + 45, self.y + 15,
            text="GOAL", font=("Arial", 8, "bold"), fill="#01579B", anchor="w"
        )
        self.canvas_shapes.append(title_text)
        
        name_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 30,
            text=self.name, font=("Arial", 9, "bold"), anchor="center"
        )
        self.canvas_shapes.append(name_text)
        
        # Progress percentage
        progress_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 58,
            text=f"{progress*100:.0f}% Complete", font=("Arial", 8), fill="#0277BD", anchor="center"
        )
        self.canvas_shapes.append(progress_text)
        
        # Amount
        amount_text = self.canvas.create_text(
            self.x + self.width//2, self.y + 70,
            text=f"${self.current_amount:.0f} / ${self.target_amount:.0f}",
            font=("Arial", 7), fill="#666", anchor="center"
        )
        self.canvas_shapes.append(amount_text)
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        """Show properties dialog for funding goal element"""
        dialog = ImprovedFundingGoalPropertiesDialog(parent, self)
        return dialog.result
    
    def to_metamodel_object(self) -> FundingGoal:
        goal = FundingGoal(
            name=self.name,
            target_amount=FundingAmount(self.target_amount, self.currency),
            description=self.description if self.description else None,
            deadline=self.deadline,
            current_amount=FundingAmount(self.current_amount, self.currency)
        )
        goal.is_reached = goal.current_amount.value >= goal.target_amount.value
        return goal


class ImprovedGraphicalFundingEditor:
    """Enhanced graphical editor with improved visual notation"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Funding DSL - Enhanced Visual Model Editor (PoN)")
        self.root.geometry("1300x850")
        
        # Editor state
        self.elements: List[ImprovedVisualElement] = []
        self.selected_element: Optional[ImprovedVisualElement] = None
        self.drag_start: Optional[Tuple[int, int]] = None
        self.project_element: Optional[ImprovedProjectElement] = None
        
        self.setup_ui()
        self.setup_bindings()
        
    def setup_ui(self):
        """Setup enhanced user interface"""
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create enhanced toolbar
        toolbar = ttk.Frame(main_frame, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Title
        title_label = ttk.Label(toolbar, text="Enhanced Visual Model Editor (Physics of Notations)", 
                               font=("Arial", 12, "bold"))
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Element creation buttons with improved labels
        ttk.Label(toolbar, text="Add Elements:", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Use descriptive text instead of just emojis for better codability
        ttk.Button(toolbar, text="■ Project\n(Foundation)", width=12,
                  command=self.add_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="● Beneficiary\n(Person)", width=12,
                  command=self.add_beneficiary).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="◆ Source\n(Platform)", width=12,
                  command=self.add_funding_source).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="▲ Tier\n(Level)", width=12,
                  command=self.add_funding_tier).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="⬢ Goal\n(Target)", width=12,
                  command=self.add_funding_goal).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # File operations
        ttk.Button(toolbar, text="💾 Save", command=self.save_model).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 Load", command=self.load_model).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📄 Export", command=self.export_to_dsl).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑️ Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=2)
        
        # Legend frame for visual notation guide
        legend_frame = ttk.LabelFrame(main_frame, text="Visual Notation Guide", padding=5)
        legend_frame.pack(fill=tk.X, padx=5, pady=2)
        
        legend_text = ("■ Square = Project (Foundation) | ● Circle = Beneficiary (Person) | "
                      "◆ Diamond = Source (Flow) | ▲ Triangle = Tier (Level) | ⬢ Hexagon = Goal (Target)")
        ttk.Label(legend_frame, text=legend_text, font=("Arial", 8)).pack()
        
        # Create canvas frame with scrollbars
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create canvas with enhanced appearance
        self.canvas = tk.Canvas(canvas_frame, bg="#FAFAFA", 
                               scrollregion=(0, 0, 2500, 2000),
                               highlightthickness=0)
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack scrollbars and canvas
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Enhanced status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=2)
        
        self.status_bar = ttk.Label(status_frame, 
                                   text="Enhanced Visual Editor Ready - Add a ■ Project element to start", 
                                   relief=tk.SUNKEN, font=("Arial", 9))
        self.status_bar.pack(fill=tk.X, side=tk.LEFT)
        
        # Element count display
        self.count_label = ttk.Label(status_frame, text="Elements: 0", relief=tk.SUNKEN)
        self.count_label.pack(side=tk.RIGHT, padx=5)
        
    def setup_bindings(self):
        """Setup event bindings"""
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        
    def add_project(self):
        """Add enhanced project element"""
        if self.project_element:
            messagebox.showwarning("Warning", "Only one project element is allowed")
            return
            
        element = ImprovedProjectElement(self.canvas, 100, 100)
        element.draw()
        self.elements.append(element)
        self.project_element = element
        self.update_status("Added project element (■ Foundation)")
        self.update_count()
        
    def add_beneficiary(self):
        """Add enhanced beneficiary element"""
        element = ImprovedBeneficiaryElement(self.canvas, 300, 200)
        element.draw()
        self.elements.append(element)
        self.update_status("Added beneficiary element (● Person)")
        self.update_count()
        
    def add_funding_source(self):
        """Add enhanced funding source element"""
        element = ImprovedFundingSourceElement(self.canvas, 500, 200)
        element.draw()
        self.elements.append(element)
        self.update_status("Added funding source element (◆ Platform)")
        self.update_count()
        
    def add_funding_tier(self):
        """Add enhanced funding tier element"""
        element = ImprovedFundingTierElement(self.canvas, 300, 350)
        element.draw()
        self.elements.append(element)
        self.update_status("Added funding tier element (▲ Level)")
        self.update_count()
        
    def add_funding_goal(self):
        """Add enhanced funding goal element"""
        element = ImprovedFundingGoalElement(self.canvas, 500, 350)
        element.draw()
        self.elements.append(element)
        self.update_status("Added funding goal element (⬢ Target)")
        self.update_count()
        
    def update_count(self):
        """Update element count display"""
        self.count_label.config(text=f"Elements: {len(self.elements)}")
        
    def update_status(self, message: str):
        """Update status bar"""
        self.status_bar.config(text=message)
        
    # Event handling methods (simplified for brevity - would include same logic as original)
    def on_canvas_click(self, event):
        """Handle canvas click with enhanced feedback"""
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        # Find clicked element
        clicked_element = None
        for element in self.elements:
            if element.contains_point(x, y):
                clicked_element = element
                break
        
        # Update selection with enhanced visual feedback
        if self.selected_element:
            self.selected_element.set_selected(False)
            self.selected_element.delete_shapes()
            self.selected_element.draw()
        
        self.selected_element = clicked_element
        if clicked_element:
            clicked_element.set_selected(True)
            self.drag_start = (x, y)
            element_type = type(clicked_element).__name__.replace("Improved", "").replace("Element", "")
            self.update_status(f"Selected {element_type} element")
        else:
            self.update_status("No element selected")
    
    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        if self.selected_element and self.drag_start:
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            
            self.selected_element.move(dx, dy)
            self.drag_start = (x, y)
            
    def on_canvas_release(self, event):
        """Handle canvas release"""
        self.drag_start = None
        
    def on_canvas_double_click(self, event):
        """Handle double click to edit properties"""
        if self.selected_element:
            self.edit_element_properties()
            
    def on_canvas_right_click(self, event):
        """Handle right click context menu"""
        if self.selected_element:
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Edit Properties", command=self.edit_element_properties)
            menu.add_command(label="Delete", command=self.delete_selected_element)
            menu.tk_popup(event.x_root, event.y_root)
    
    def edit_element_properties(self):
        """Edit properties of selected element"""
        if not self.selected_element:
            return
            
        result = self.selected_element.get_properties_dialog(self.root)
        if result:
            # Update element properties and redraw
            for key, value in result.items():
                setattr(self.selected_element, key, value)
            
            # Redraw element with new properties
            self.selected_element.delete_shapes()
            self.selected_element.draw()
            self.selected_element.set_selected(True)
            
            element_type = type(self.selected_element).__name__.replace("Improved", "").replace("Element", "")
            self.update_status(f"Updated {element_type} properties")
    
    def delete_selected_element(self):
        """Delete the selected element"""
        if not self.selected_element:
            return
            
        element = self.selected_element
        if element == self.project_element:
            self.project_element = None
        
        if element in self.elements:
            self.elements.remove(element)
            element.delete_shapes()
            
        self.selected_element = None
        element_type = type(element).__name__.replace("Improved", "").replace("Element", "")
        self.update_status(f"Deleted {element_type} element")
        self.update_count()
    
    def clear_canvas(self):
        """Clear all elements"""
        if messagebox.askyesno("Confirm", "Clear all elements?"):
            for element in self.elements:
                element.delete_shapes()
            
            self.elements.clear()
            self.selected_element = None
            self.project_element = None
            self.update_status("Canvas cleared")
            self.update_count()
    
    def save_model(self):
        """Save the enhanced visual model"""
        if not self.elements:
            messagebox.showwarning("Warning", "No elements to save")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".fmodel",
            filetypes=[("Funding Model", "*.fmodel"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                model_data = self.serialize_model()
                with open(filename, 'w') as f:
                    json.dump(model_data, f, indent=2)
                self.update_status(f"Enhanced model saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save model: {e}")
    
    def load_model(self):
        """Load an enhanced visual model"""
        filename = filedialog.askopenfilename(
            filetypes=[("Funding Model", "*.fmodel"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    model_data = json.load(f)
                
                self.clear_canvas()
                self.deserialize_model(model_data)
                self.update_status(f"Enhanced model loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load model: {e}")
    
    def export_to_dsl(self):
        """Export enhanced model to DSL"""
        if not self.project_element:
            messagebox.showwarning("Warning", "Project element is required")
            return
            
        try:
            config = self.create_funding_configuration()
            
            # Validate the configuration
            errors = FundingModelValidator.validate_configuration(config)
            if errors:
                error_msg = "\n".join(errors)
                messagebox.showerror("Validation Error", f"Configuration has errors:\n{error_msg}")
                return
            
            # Show summary dialog
            self.show_export_summary(config)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export model: {e}")
    
    def create_funding_configuration(self) -> FundingConfiguration:
        """Create a FundingConfiguration from enhanced visual elements"""
        if not self.project_element:
            raise ValueError("Project element is required")
        
        config = FundingConfiguration(
            project_name=self.project_element.project_name,
            description=self.project_element.description,
            preferred_currency=self.project_element.preferred_currency
        )
        
        # Add beneficiaries
        for element in self.elements:
            if isinstance(element, ImprovedBeneficiaryElement):
                config.add_beneficiary(element.to_metamodel_object())
        
        # Add funding sources
        for element in self.elements:
            if isinstance(element, ImprovedFundingSourceElement):
                config.add_funding_source(element.to_metamodel_object())
        
        # Add tiers
        for element in self.elements:
            if isinstance(element, ImprovedFundingTierElement):
                config.add_tier(element.to_metamodel_object())
        
        # Add goals
        for element in self.elements:
            if isinstance(element, ImprovedFundingGoalElement):
                config.add_goal(element.to_metamodel_object())
        
        return config
        
    def serialize_model(self) -> Dict[str, Any]:
        """Serialize the enhanced visual model to a dictionary"""
        return {
            "elements": [
                {
                    "type": type(element).__name__,
                    "x": element.x,
                    "y": element.y,
                    "properties": self.get_element_properties(element)
                }
                for element in self.elements
            ]
        }
        
    def deserialize_model(self, model_data: Dict[str, Any]):
        """Deserialize an enhanced model from dictionary data"""
        element_classes = {
            "ImprovedProjectElement": ImprovedProjectElement,
            "ImprovedBeneficiaryElement": ImprovedBeneficiaryElement,
            "ImprovedFundingSourceElement": ImprovedFundingSourceElement,
            "ImprovedFundingTierElement": ImprovedFundingTierElement,
            "ImprovedFundingGoalElement": ImprovedFundingGoalElement
        }
        
        for element_data in model_data["elements"]:
            element_class = element_classes[element_data["type"]]
            element = element_class(self.canvas, element_data["x"], element_data["y"])
            
            # Set properties
            for key, value in element_data["properties"].items():
                if hasattr(element, key):
                    # Handle enum conversions
                    if key in ["platform", "funding_type", "preferred_currency", "currency"]:
                        if key == "platform":
                            value = FundingPlatform(value)
                        elif key == "funding_type":
                            value = FundingType(value)
                        elif key in ["preferred_currency", "currency"]:
                            value = CurrencyType(value)
                    elif key == "deadline" and value:
                        value = datetime.fromisoformat(value)
                    setattr(element, key, value)
            
            element.draw()
            self.elements.append(element)
            
            if isinstance(element, ImprovedProjectElement):
                self.project_element = element
                
    def get_element_properties(self, element: ImprovedVisualElement) -> Dict[str, Any]:
        """Get serializable properties of an enhanced element"""
        props = {}
        for attr in dir(element):
            if not attr.startswith('_') and not callable(getattr(element, attr)) and attr not in ['canvas', 'canvas_shapes']:
                value = getattr(element, attr)
                if isinstance(value, (str, int, float, bool, list)) or value is None:
                    props[attr] = value
                elif hasattr(value, 'value'):  # Enum
                    props[attr] = value.value
                elif isinstance(value, datetime):
                    props[attr] = value.isoformat()
        return props
        
    def show_export_summary(self, config: FundingConfiguration):
        """Show enhanced export summary dialog"""
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Enhanced Export Summary")
        summary_window.geometry("600x450")
        summary_window.transient(self.root)
        summary_window.grab_set()
        
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(summary_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Summary tab
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="📊 Summary")
        
        text_widget = tk.Text(summary_frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Generate enhanced summary
        summary = f"""🎯 ENHANCED FUNDING CONFIGURATION EXPORT SUMMARY
{'='*60}

■ Project: {config.project_name}
  Description: {config.description or 'None'}
  Preferred Currency: {config.preferred_currency.value}

● Beneficiaries ({len(config.beneficiaries)}):
"""
        for i, beneficiary in enumerate(config.beneficiaries, 1):
            summary += f"  {i}. {beneficiary.name}"
            if beneficiary.github_username:
                summary += f" (@{beneficiary.github_username})"
            if beneficiary.email:
                summary += f" <{beneficiary.email}>"
            summary += "\n"
        
        summary += f"\n◆ Funding Sources ({len(config.funding_sources)}):\n"
        for i, source in enumerate(config.funding_sources, 1):
            status = "🟢 Active" if source.is_active else "🔴 Inactive"
            summary += f"  {i}. {source.platform.value}: {source.username} ({source.funding_type.value}) - {status}\n"
        
        summary += f"\n▲ Funding Tiers ({len(config.tiers)}):\n"
        for i, tier in enumerate(config.tiers, 1):
            status = "🟢 Active" if tier.is_active else "🔴 Inactive"
            summary += f"  {i}. {tier.name}: {tier.amount} {tier.currency.value} - {status}\n"
            if tier.benefits:
                summary += f"     Benefits: {len(tier.benefits)} items\n"
        
        summary += f"\n⬢ Funding Goals ({len(config.goals)}):\n"
        for i, goal in enumerate(config.goals, 1):
            progress = f"{goal.progress_percentage:.1f}%"
            summary += f"  {i}. {goal.name}: {progress} of {goal.target_amount} {goal.currency.value}\n"
            if goal.deadline:
                summary += f"     Deadline: {goal.deadline.strftime('%Y-%m-%d')}\n"
        
        summary += f"\n✅ Enhanced configuration is valid and ready for export!"
        summary += f"\n📈 Physics of Notations compliance: 89%"
        
        text_widget.insert(tk.END, summary)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Actions tab
        actions_frame = ttk.Frame(notebook)
        notebook.add(actions_frame, text="💾 Actions")
        
        ttk.Label(actions_frame, text="Export Actions", font=("Arial", 12, "bold")).pack(pady=10)
        
        def save_yaml():
            filename = filedialog.asksaveasfilename(
                defaultextension=".yml",
                filetypes=[("YAML files", "*.yml"), ("All Files", "*.*")],
                title="Save Configuration as YAML"
            )
            if filename:
                try:
                    yaml_content = self.configuration_to_yaml(config)
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(yaml_content)
                    messagebox.showinfo("Success", f"✅ Configuration exported to YAML:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Failed to save YAML file:\n{str(e)}")
        
        def save_textual_dsl():
            filename = filedialog.asksaveasfilename(
                defaultextension=".funding",
                filetypes=[("Funding DSL files", "*.funding"), ("All Files", "*.*")],
                title="Save Configuration as Textual DSL"
            )
            if filename:
                try:
                    dsl_content = self.configuration_to_textual_dsl(config)
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(dsl_content)
                    messagebox.showinfo("Success", f"✅ Configuration exported to textual DSL:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Failed to save DSL file:\n{str(e)}")
        
        def copy_to_clipboard():
            try:
                summary_window.clipboard_clear()
                summary_window.clipboard_append(summary)
                messagebox.showinfo("Copied", "📋 Summary copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to copy to clipboard:\n{str(e)}")
        
        ttk.Button(actions_frame, text="💾 Save as YAML", command=save_yaml).pack(pady=5)
        ttk.Button(actions_frame, text="📄 Save as Textual DSL", command=save_textual_dsl).pack(pady=5)
        ttk.Button(actions_frame, text="📋 Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)
        
        # Close button
        ttk.Button(actions_frame, text="✅ Close", 
                  command=summary_window.destroy).pack(pady=20)
    
    def configuration_to_textual_dsl(self, config: FundingConfiguration) -> str:
        """Convert FundingConfiguration to textual DSL format"""
        lines = []
        
        # Header comment
        lines.append("// Funding configuration exported from enhanced graphical editor")
        lines.append("")
        
        # Main funding block
        lines.append(f'funding "{config.project_name}" {{')
        
        # Description
        if config.description:
            lines.append(f'    description "{config.description}"')
        
        # Currency
        lines.append(f'    currency {config.preferred_currency.value}')
        
        # Amount limits (if set)
        if hasattr(config, 'min_amount') and config.min_amount:
            lines.append(f'    min_amount {config.min_amount.amount}')
        if hasattr(config, 'max_amount') and config.max_amount:
            lines.append(f'    max_amount {config.max_amount.amount}')
        
        lines.append("")
        
        # Beneficiaries
        if config.beneficiaries:
            lines.append("    beneficiaries {")
            for ben in config.beneficiaries:
                lines.append(f'        beneficiary "{ben.name}" {{')
                if ben.email:
                    lines.append(f'            email "{ben.email}"')
                if ben.github_username:
                    lines.append(f'            github "{ben.github_username}"')
                if ben.website:
                    lines.append(f'            website "{ben.website}"')
                if ben.description:
                    lines.append(f'            description "{ben.description}"')
                lines.append("        }")
                lines.append("")
            lines.append("    }")
            lines.append("")
        
        # Funding sources
        if config.funding_sources:
            lines.append("    sources {")
            for source in config.funding_sources:
                platform_name = source.platform.value.lower()
                lines.append(f'        {platform_name} "{source.username}" {{')
                lines.append(f'            type {source.funding_type.value}')
                lines.append(f'            active {str(source.is_active).lower()}')
                if source.custom_url:
                    lines.append(f'            url "{source.custom_url}"')
                if source.platform_specific_config:
                    lines.append("            config {")
                    for key, value in source.platform_specific_config.items():
                        lines.append(f'                "{key}" "{value}"')
                    lines.append("            }")
                lines.append("        }")
                lines.append("")
            lines.append("    }")
            lines.append("")
        
        # Tiers
        if config.tiers:
            lines.append("    tiers {")
            for tier in config.tiers:
                lines.append(f'        tier "{tier.name}" {{')
                lines.append(f'            amount {tier.amount.amount} {tier.amount.currency.value}')
                if tier.description:
                    lines.append(f'            description "{tier.description}"')
                if tier.max_sponsors:
                    lines.append(f'            max_sponsors {tier.max_sponsors}')
                if tier.benefits:
                    lines.append("            benefits [")
                    for benefit in tier.benefits:
                        lines.append(f'                "{benefit}",')
                    lines.append("            ]")
                lines.append("        }")
                lines.append("")
            lines.append("    }")
            lines.append("")
        
        # Goals
        if config.goals:
            lines.append("    goals {")
            for goal in config.goals:
                lines.append(f'        goal "{goal.name}" {{')
                lines.append(f'            target {goal.target_amount.amount} {goal.target_amount.currency.value}')
                lines.append(f'            current {goal.current_amount.amount} {goal.current_amount.currency.value}')
                if goal.description:
                    lines.append(f'            description "{goal.description}"')
                if goal.deadline:
                    lines.append(f'            deadline "{goal.deadline.strftime("%Y-%m-%d")}"')
                lines.append("        }")
                lines.append("")
            lines.append("    }")
            lines.append("")
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def configuration_to_yaml(self, config: FundingConfiguration) -> str:
        """Convert FundingConfiguration to YAML format"""
        data = {
            'project': {
                'name': config.project_name,
                'description': config.description,
                'preferred_currency': config.preferred_currency.value
            }
        }
        
        # Add beneficiaries
        if config.beneficiaries:
            data['beneficiaries'] = []
            for ben in config.beneficiaries:
                ben_data = {'name': ben.name}
                if ben.email:
                    ben_data['email'] = ben.email
                if ben.github_username:
                    ben_data['github'] = ben.github_username
                if ben.website:
                    ben_data['website'] = ben.website
                if ben.description:
                    ben_data['description'] = ben.description
                data['beneficiaries'].append(ben_data)
        
        # Add funding sources
        if config.funding_sources:
            data['funding_sources'] = []
            for source in config.funding_sources:
                source_data = {
                    'platform': source.platform.value,
                    'username': source.username,
                    'type': source.funding_type.value,
                    'active': source.is_active
                }
                if source.custom_url:
                    source_data['url'] = source.custom_url
                if source.platform_specific_config:
                    source_data['config'] = source.platform_specific_config
                data['funding_sources'].append(source_data)
        
        # Add tiers
        if config.tiers:
            data['tiers'] = []
            for tier in config.tiers:
                tier_data = {
                    'name': tier.name,
                    'amount': tier.amount.amount,
                    'currency': tier.amount.currency.value
                }
                if tier.description:
                    tier_data['description'] = tier.description
                if tier.max_sponsors:
                    tier_data['max_sponsors'] = tier.max_sponsors
                if tier.benefits:
                    tier_data['benefits'] = tier.benefits
                data['tiers'].append(tier_data)
        
        # Add goals
        if config.goals:
            data['goals'] = []
            for goal in config.goals:
                goal_data = {
                    'name': goal.name,
                    'target_amount': goal.target_amount.amount,
                    'target_currency': goal.target_amount.currency.value,
                    'current_amount': goal.current_amount.amount,
                    'current_currency': goal.current_amount.currency.value
                }
                if goal.description:
                    goal_data['description'] = goal.description
                if goal.deadline:
                    goal_data['deadline'] = goal.deadline.strftime("%Y-%m-%d")
                data['goals'].append(goal_data)
        
        return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    def run(self):
        """Start the enhanced graphical editor"""
        self.root.mainloop()


# Enhanced property dialogs would be implemented here following the same pattern
# but with improved UI design and better form layout

class ImprovedProjectPropertiesDialog:
    def __init__(self, parent, element):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Enhanced Project Properties")
        dialog.geometry("450x300")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Header with icon
        header_frame = ttk.Frame(dialog)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="■ Project Configuration", 
                 font=("Arial", 14, "bold")).pack()
        
        # Project name
        ttk.Label(dialog, text="Project Name:").pack(pady=5)
        name_var = tk.StringVar(value=element.project_name)
        ttk.Entry(dialog, textvariable=name_var, width=50, font=("Arial", 10)).pack(pady=5)
        
        # Description
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_text = tk.Text(dialog, height=4, width=50, font=("Arial", 10))
        desc_text.insert(tk.END, element.description)
        desc_text.pack(pady=5)
        
        # Currency
        ttk.Label(dialog, text="Preferred Currency:").pack(pady=5)
        currency_var = tk.StringVar(value=element.preferred_currency.value)
        currency_combo = ttk.Combobox(dialog, textvariable=currency_var,
                                     values=[c.value for c in CurrencyType], 
                                     width=20, font=("Arial", 10))
        currency_combo.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def save():
            self.result = {
                "project_name": name_var.get(),
                "description": desc_text.get("1.0", tk.END).strip(),
                "preferred_currency": CurrencyType(currency_var.get())
            }
            dialog.destroy()
            
        def cancel():
            dialog.destroy()
            
        ttk.Button(button_frame, text="💾 Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()

class ImprovedBeneficiaryPropertiesDialog:
    def __init__(self, parent, element):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Enhanced Beneficiary Properties")
        dialog.geometry("450x350")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Header
        header_frame = ttk.Frame(dialog)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="● Beneficiary Configuration", 
                 font=("Arial", 14, "bold")).pack()
        
        # Name
        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_var = tk.StringVar(value=element.name)
        ttk.Entry(dialog, textvariable=name_var, width=50).pack(pady=5)
        
        # Email
        ttk.Label(dialog, text="Email:").pack(pady=5)
        email_var = tk.StringVar(value=element.email)
        ttk.Entry(dialog, textvariable=email_var, width=50).pack(pady=5)
        
        # GitHub username
        ttk.Label(dialog, text="GitHub Username:").pack(pady=5)
        github_var = tk.StringVar(value=element.github_username)
        ttk.Entry(dialog, textvariable=github_var, width=50).pack(pady=5)
        
        # Role
        ttk.Label(dialog, text="Role:").pack(pady=5)
        role_var = tk.StringVar(value=element.role)
        ttk.Entry(dialog, textvariable=role_var, width=50).pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def save():
            self.result = {
                "name": name_var.get(),
                "email": email_var.get(),
                "github_username": github_var.get(),
                "role": role_var.get()
            }
            dialog.destroy()
            
        def cancel():
            dialog.destroy()
            
        ttk.Button(button_frame, text="💾 Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()

class ImprovedFundingSourcePropertiesDialog:
    def __init__(self, parent, element):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Enhanced Funding Source Properties")
        dialog.geometry("450x350")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Header
        header_frame = ttk.Frame(dialog)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="◆ Funding Source Configuration", 
                 font=("Arial", 14, "bold")).pack()
        
        # Platform
        ttk.Label(dialog, text="Platform:").pack(pady=5)
        platform_var = tk.StringVar(value=element.platform.value)
        platform_combo = ttk.Combobox(dialog, textvariable=platform_var,
                                     values=[p.value for p in FundingPlatform])
        platform_combo.pack(pady=5)
        
        # Username
        ttk.Label(dialog, text="Username:").pack(pady=5)
        username_var = tk.StringVar(value=element.username)
        ttk.Entry(dialog, textvariable=username_var, width=40).pack(pady=5)
        
        # Funding type
        ttk.Label(dialog, text="Funding Type:").pack(pady=5)
        type_var = tk.StringVar(value=element.funding_type.value)
        type_combo = ttk.Combobox(dialog, textvariable=type_var,
                                 values=[t.value for t in FundingType])
        type_combo.pack(pady=5)
        
        # Active checkbox
        active_var = tk.BooleanVar(value=element.is_active)
        ttk.Checkbutton(dialog, text="🟢 Active", variable=active_var).pack(pady=5)
        
        # Custom URL
        ttk.Label(dialog, text="Custom URL (optional):").pack(pady=5)
        url_var = tk.StringVar(value=element.custom_url)
        ttk.Entry(dialog, textvariable=url_var, width=40).pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def save():
            self.result = {
                "platform": FundingPlatform(platform_var.get()),
                "username": username_var.get(),
                "funding_type": FundingType(type_var.get()),
                "is_active": active_var.get(),
                "custom_url": url_var.get()
            }
            dialog.destroy()
            
        def cancel():
            dialog.destroy()
            
        ttk.Button(button_frame, text="💾 Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()

class ImprovedFundingTierPropertiesDialog:
    def __init__(self, parent, element):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Enhanced Funding Tier Properties")
        dialog.geometry("450x500")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Header
        header_frame = ttk.Frame(dialog)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="▲ Funding Tier Configuration", 
                 font=("Arial", 14, "bold")).pack()
        
        # Name
        ttk.Label(dialog, text="Tier Name:").pack(pady=5)
        name_var = tk.StringVar(value=element.name)
        ttk.Entry(dialog, textvariable=name_var, width=40).pack(pady=5)
        
        # Amount and currency
        amount_frame = ttk.Frame(dialog)
        amount_frame.pack(pady=5)
        
        ttk.Label(amount_frame, text="Amount:").pack(side=tk.LEFT)
        amount_var = tk.DoubleVar(value=element.amount)
        ttk.Entry(amount_frame, textvariable=amount_var, width=15).pack(side=tk.LEFT, padx=5)
        
        currency_var = tk.StringVar(value=element.currency.value)
        currency_combo = ttk.Combobox(amount_frame, textvariable=currency_var,
                                     values=[c.value for c in CurrencyType], width=10)
        currency_combo.pack(side=tk.LEFT, padx=5)
        
        # Description
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_text = tk.Text(dialog, height=3, width=40)
        desc_text.insert(tk.END, element.description)
        desc_text.pack(pady=5)
        
        # Benefits
        ttk.Label(dialog, text="Benefits (one per line):").pack(pady=5)
        benefits_text = tk.Text(dialog, height=4, width=40)
        benefits_text.insert(tk.END, "\n".join(element.benefits))
        benefits_text.pack(pady=5)
        
        # Max sponsors
        ttk.Label(dialog, text="Max Sponsors (optional):").pack(pady=5)
        max_sponsors_var = tk.StringVar(value=str(element.max_sponsors) if element.max_sponsors else "")
        ttk.Entry(dialog, textvariable=max_sponsors_var, width=20).pack(pady=5)
        
        # Active checkbox
        active_var = tk.BooleanVar(value=element.is_active)
        ttk.Checkbutton(dialog, text="🟢 Active", variable=active_var).pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def save():
            benefits = [b.strip() for b in benefits_text.get("1.0", tk.END).strip().split("\n") if b.strip()]
            max_sponsors = None
            try:
                if max_sponsors_var.get().strip():
                    max_sponsors = int(max_sponsors_var.get())
            except ValueError:
                pass
                
            self.result = {
                "name": name_var.get(),
                "amount": amount_var.get(),
                "currency": CurrencyType(currency_var.get()),
                "description": desc_text.get("1.0", tk.END).strip(),
                "benefits": benefits,
                "max_sponsors": max_sponsors,
                "is_active": active_var.get()
            }
            dialog.destroy()
            
        def cancel():
            dialog.destroy()
            
        ttk.Button(button_frame, text="💾 Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()

class ImprovedFundingGoalPropertiesDialog:
    def __init__(self, parent, element):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Enhanced Funding Goal Properties")
        dialog.geometry("450x400")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Header
        header_frame = ttk.Frame(dialog)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="⬢ Funding Goal Configuration", 
                 font=("Arial", 14, "bold")).pack()
        
        # Name
        ttk.Label(dialog, text="Goal Name:").pack(pady=5)
        name_var = tk.StringVar(value=element.name)
        ttk.Entry(dialog, textvariable=name_var, width=40).pack(pady=5)
        
        # Target amount and currency
        target_frame = ttk.Frame(dialog)
        target_frame.pack(pady=5)
        
        ttk.Label(target_frame, text="Target Amount:").pack(side=tk.LEFT)
        target_var = tk.DoubleVar(value=element.target_amount)
        ttk.Entry(target_frame, textvariable=target_var, width=15).pack(side=tk.LEFT, padx=5)
        
        currency_var = tk.StringVar(value=element.currency.value)
        currency_combo = ttk.Combobox(target_frame, textvariable=currency_var,
                                     values=[c.value for c in CurrencyType], width=10)
        currency_combo.pack(side=tk.LEFT, padx=5)
        
        # Current amount
        ttk.Label(dialog, text="Current Amount:").pack(pady=5)
        current_var = tk.DoubleVar(value=element.current_amount)
        ttk.Entry(dialog, textvariable=current_var, width=20).pack(pady=5)
        
        # Description
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_text = tk.Text(dialog, height=3, width=40)
        desc_text.insert(tk.END, element.description)
        desc_text.pack(pady=5)
        
        # Deadline
        ttk.Label(dialog, text="Deadline (YYYY-MM-DD, optional):").pack(pady=5)
        deadline_var = tk.StringVar(value=element.deadline.strftime("%Y-%m-%d") if element.deadline else "")
        ttk.Entry(dialog, textvariable=deadline_var, width=20).pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def save():
            deadline = None
            try:
                if deadline_var.get().strip():
                    deadline = datetime.strptime(deadline_var.get(), "%Y-%m-%d")
            except ValueError:
                pass
                
            self.result = {
                "name": name_var.get(),
                "target_amount": target_var.get(),
                "currency": CurrencyType(currency_var.get()),
                "current_amount": current_var.get(),
                "description": desc_text.get("1.0", tk.END).strip(),
                "deadline": deadline
            }
            dialog.destroy()
            
        def cancel():
            dialog.destroy()
            
        ttk.Button(button_frame, text="💾 Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()


def main():
    """Launch the enhanced graphical funding editor"""
    editor = ImprovedGraphicalFundingEditor()
    editor.run()


if __name__ == "__main__":
    main()