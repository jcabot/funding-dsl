"""
Graphical Model Editor for Funding DSL
A canvas-based visual editor for creating funding configurations using drag-and-drop.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from typing import Dict, List, Optional, Tuple, Any
import json
import pickle
from datetime import datetime, timedelta

from metamodel.funding_metamodel import (
    FundingConfiguration, Beneficiary, FundingSource, FundingTier, 
    FundingGoal, FundingAmount, FundingPlatform, FundingType, 
    CurrencyType, FundingModelValidator
)


class VisualElement:
    """Base class for visual elements on the canvas"""
    
    def __init__(self, canvas, x: int, y: int, width: int = 100, height: int = 60):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False
        self.canvas_id = None
        self.text_id = None
        
    def draw(self):
        """Draw the element on the canvas"""
        pass
    
    def move(self, dx: int, dy: int):
        """Move the element by dx, dy"""
        self.x += dx
        self.y += dy
        if self.canvas_id:
            self.canvas.move(self.canvas_id, dx, dy)
        if self.text_id:
            self.canvas.move(self.text_id, dx, dy)
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if point (x, y) is inside this element"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def set_selected(self, selected: bool):
        """Set selection state"""
        self.selected = selected
        self.update_appearance()
    
    def update_appearance(self):
        """Update visual appearance based on state"""
        if self.canvas_id:
            color = "red" if self.selected else self.get_default_color()
            self.canvas.itemconfig(self.canvas_id, outline=color, width=2 if self.selected else 1)
    
    def get_default_color(self) -> str:
        """Get default color for this element type"""
        return "black"
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        """Show properties dialog and return configuration dict"""
        return None
    
    def to_metamodel_object(self):
        """Convert to corresponding metamodel object"""
        pass


class ProjectElement(VisualElement):
    """Visual element representing the main project/funding configuration"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 150, 80)
        self.project_name = "New Project"
        self.description = ""
        self.preferred_currency = CurrencyType.USD
        
    def draw(self):
        self.canvas_id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="lightblue", outline="blue", width=2
        )
        self.text_id = self.canvas.create_text(
            self.x + self.width//2, self.y + self.height//2,
            text=f"📦\n{self.project_name}", font=("Arial", 10, "bold")
        )
    
    def get_default_color(self) -> str:
        return "blue"
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        dialog = ProjectPropertiesDialog(parent, self)
        if dialog.result:
            return dialog.result
        return None


class BeneficiaryElement(VisualElement):
    """Visual element representing a beneficiary"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 120, 70)
        self.name = "New Beneficiary"
        self.email = ""
        self.github_username = ""
        self.website = ""
        self.description = ""
        
    def draw(self):
        self.canvas_id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="lightgreen", outline="green"
        )
        self.text_id = self.canvas.create_text(
            self.x + self.width//2, self.y + self.height//2,
            text=f"👤\n{self.name}", font=("Arial", 9)
        )
    
    def get_default_color(self) -> str:
        return "green"
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        dialog = BeneficiaryPropertiesDialog(parent, self)
        if dialog.result:
            return dialog.result
        return None
    
    def to_metamodel_object(self) -> Beneficiary:
        return Beneficiary(
            name=self.name,
            email=self.email if self.email else None,
            github_username=self.github_username if self.github_username else None,
            website=self.website if self.website else None,
            description=self.description if self.description else None
        )


class FundingSourceElement(VisualElement):
    """Visual element representing a funding source"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 130, 70)
        self.platform = FundingPlatform.GITHUB_SPONSORS
        self.username = "username"
        self.funding_type = FundingType.BOTH
        self.is_active = True
        self.custom_url = ""
        
    def draw(self):
        self.canvas_id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="lightyellow", outline="orange"
        )
        platform_emoji = {
            "github": "💖", "patreon": "🎨", "ko_fi": "☕", 
            "open_collective": "🤝", "buy_me_a_coffee": "☕", 
            "liberapay": "💝", "paypal": "💳", 
            "tidelift": "🛡️", "issuehunt": "🐛", 
            "community_bridge": "🌉", "polar": "🐻", 
            "thanks_dev": "🙏"
        }.get(self.platform.value, "💰")
        self.text_id = self.canvas.create_text(
            self.x + self.width//2, self.y + self.height//2,
            text=f"{platform_emoji}\n{self.platform.value}\n{self.username}", 
            font=("Arial", 8)
        )
    
    def get_default_color(self) -> str:
        return "orange"
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        dialog = FundingSourcePropertiesDialog(parent, self)
        if dialog.result:
            return dialog.result
        return None
    
    def to_metamodel_object(self) -> FundingSource:
        return FundingSource(
            platform=self.platform,
            username=self.username,
            funding_type=self.funding_type,
            is_active=self.is_active,
            custom_url=self.custom_url if self.custom_url else None
        )


class FundingTierElement(VisualElement):
    """Visual element representing a funding tier"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 110, 80)
        self.name = "New Tier"
        self.amount = 10.0
        self.currency = CurrencyType.USD
        self.description = ""
        self.benefits = []
        self.max_sponsors = None
        self.is_active = True
        
    def draw(self):
        self.canvas_id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="lightpink", outline="purple"
        )
        self.text_id = self.canvas.create_text(
            self.x + self.width//2, self.y + self.height//2,
            text=f"🎯\n{self.name}\n${self.amount}", font=("Arial", 8)
        )
    
    def get_default_color(self) -> str:
        return "purple"
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        dialog = FundingTierPropertiesDialog(parent, self)
        if dialog.result:
            return dialog.result
        return None
    
    def to_metamodel_object(self) -> FundingTier:
        return FundingTier(
            name=self.name,
            amount=FundingAmount(self.amount, self.currency),
            description=self.description if self.description else None,
            benefits=self.benefits,
            max_sponsors=self.max_sponsors,
            is_active=self.is_active
        )


class FundingGoalElement(VisualElement):
    """Visual element representing a funding goal"""
    
    def __init__(self, canvas, x: int, y: int):
        super().__init__(canvas, x, y, 120, 80)
        self.name = "New Goal"
        self.target_amount = 1000.0
        self.current_amount = 0.0
        self.currency = CurrencyType.USD
        self.description = ""
        self.deadline = None
        
    def draw(self):
        self.canvas_id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill="lightcyan", outline="teal"
        )
        progress = (self.current_amount / self.target_amount * 100) if self.target_amount > 0 else 0
        self.text_id = self.canvas.create_text(
            self.x + self.width//2, self.y + self.height//2,
            text=f"📈\n{self.name}\n{progress:.0f}%", font=("Arial", 8)
        )
    
    def get_default_color(self) -> str:
        return "teal"
    
    def get_properties_dialog(self, parent) -> Optional[Dict[str, Any]]:
        dialog = FundingGoalPropertiesDialog(parent, self)
        if dialog.result:
            return dialog.result
        return None
    
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


class GraphicalFundingEditor:
    """Main graphical editor for funding configurations"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Funding DSL - Graphical Model Editor")
        self.root.geometry("1200x800")
        
        # Editor state
        self.elements: List[VisualElement] = []
        self.selected_element: Optional[VisualElement] = None
        self.drag_start: Optional[Tuple[int, int]] = None
        self.project_element: Optional[ProjectElement] = None
        
        self.setup_ui()
        self.setup_bindings()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Element creation buttons
        ttk.Label(toolbar, text="Add Elements:").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(toolbar, text="📦 Project", 
                  command=self.add_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="👤 Beneficiary", 
                  command=self.add_beneficiary).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💰 Funding Source", 
                  command=self.add_funding_source).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🎯 Tier", 
                  command=self.add_funding_tier).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📈 Goal", 
                  command=self.add_funding_goal).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # File operations
        ttk.Button(toolbar, text="💾 Save Model", 
                  command=self.save_model).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 Load Model", 
                  command=self.load_model).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📄 Export DSL", 
                  command=self.export_to_dsl).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑️ Clear", 
                  command=self.clear_canvas).pack(side=tk.LEFT, padx=2)
        
        # Create canvas frame with scrollbars
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg="white", 
                               scrollregion=(0, 0, 2000, 1500))
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack scrollbars and canvas
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready - Add a Project element to start", 
                                   relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, pady=2)
        
    def setup_bindings(self):
        """Setup event bindings"""
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)  # Right click
        
    def add_project(self):
        """Add a project element"""
        if self.project_element:
            messagebox.showwarning("Warning", "Only one project element is allowed")
            return
            
        element = ProjectElement(self.canvas, 100, 100)
        element.draw()
        self.elements.append(element)
        self.project_element = element
        self.update_status("Added project element")
        
    def add_beneficiary(self):
        """Add a beneficiary element"""
        element = BeneficiaryElement(self.canvas, 300, 200)
        element.draw()
        self.elements.append(element)
        self.update_status("Added beneficiary element")
        
    def add_funding_source(self):
        """Add a funding source element"""
        element = FundingSourceElement(self.canvas, 500, 200)
        element.draw()
        self.elements.append(element)
        self.update_status("Added funding source element")
        
    def add_funding_tier(self):
        """Add a funding tier element"""
        element = FundingTierElement(self.canvas, 300, 350)
        element.draw()
        self.elements.append(element)
        self.update_status("Added funding tier element")
        
    def add_funding_goal(self):
        """Add a funding goal element"""
        element = FundingGoalElement(self.canvas, 500, 350)
        element.draw()
        self.elements.append(element)
        self.update_status("Added funding goal element")
        
    def on_canvas_click(self, event):
        """Handle canvas click"""
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        # Find clicked element
        clicked_element = None
        for element in self.elements:
            if element.contains_point(x, y):
                clicked_element = element
                break
        
        # Update selection
        if self.selected_element:
            self.selected_element.set_selected(False)
        
        self.selected_element = clicked_element
        if clicked_element:
            clicked_element.set_selected(True)
            self.drag_start = (x, y)
            self.update_status(f"Selected {type(clicked_element).__name__}")
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
            self.edit_element_properties(self.selected_element)
            
    def on_canvas_right_click(self, event):
        """Handle right click context menu"""
        if self.selected_element:
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Edit Properties", 
                           command=lambda: self.edit_element_properties(self.selected_element))
            menu.add_command(label="Delete", 
                           command=lambda: self.delete_element(self.selected_element))
            menu.tk_popup(event.x_root, event.y_root)
            
    def edit_element_properties(self, element: VisualElement):
        """Edit element properties"""
        result = element.get_properties_dialog(self.root)
        if result:
            # Update element properties and redraw
            for key, value in result.items():
                setattr(element, key, value)
            
            # Redraw element
            self.canvas.delete(element.canvas_id)
            self.canvas.delete(element.text_id)
            element.draw()
            element.set_selected(True)  # Maintain selection
            
            self.update_status(f"Updated {type(element).__name__} properties")
            
    def delete_element(self, element: VisualElement):
        """Delete an element"""
        if element == self.project_element:
            self.project_element = None
        
        if element in self.elements:
            self.elements.remove(element)
            self.canvas.delete(element.canvas_id)
            self.canvas.delete(element.text_id)
            
        if element == self.selected_element:
            self.selected_element = None
            
        self.update_status(f"Deleted {type(element).__name__}")
        
    def clear_canvas(self):
        """Clear all elements"""
        if messagebox.askyesno("Confirm", "Clear all elements?"):
            for element in self.elements:
                self.canvas.delete(element.canvas_id)
                self.canvas.delete(element.text_id)
            
            self.elements.clear()
            self.selected_element = None
            self.project_element = None
            self.update_status("Canvas cleared")
            
    def save_model(self):
        """Save the visual model"""
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
                self.update_status(f"Model saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save model: {e}")
                
    def load_model(self):
        """Load a visual model"""
        filename = filedialog.askopenfilename(
            filetypes=[("Funding Model", "*.fmodel"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    model_data = json.load(f)
                
                self.clear_canvas()
                self.deserialize_model(model_data)
                self.update_status(f"Model loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load model: {e}")
                
    def export_to_dsl(self):
        """Export the visual model to a metamodel instance and optionally save as DSL"""
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
        """Create a FundingConfiguration from visual elements"""
        if not self.project_element:
            raise ValueError("Project element is required")
        
        config = FundingConfiguration(
            project_name=self.project_element.project_name,
            description=self.project_element.description,
            preferred_currency=self.project_element.preferred_currency
        )
        
        # Add beneficiaries
        for element in self.elements:
            if isinstance(element, BeneficiaryElement):
                config.add_beneficiary(element.to_metamodel_object())
        
        # Add funding sources
        for element in self.elements:
            if isinstance(element, FundingSourceElement):
                config.add_funding_source(element.to_metamodel_object())
        
        # Add tiers
        for element in self.elements:
            if isinstance(element, FundingTierElement):
                config.add_tier(element.to_metamodel_object())
        
        # Add goals
        for element in self.elements:
            if isinstance(element, FundingGoalElement):
                config.add_goal(element.to_metamodel_object())
        
        return config
        
    def serialize_model(self) -> Dict[str, Any]:
        """Serialize the visual model to a dictionary"""
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
        """Deserialize a model from dictionary data"""
        element_classes = {
            "ProjectElement": ProjectElement,
            "BeneficiaryElement": BeneficiaryElement,
            "FundingSourceElement": FundingSourceElement,
            "FundingTierElement": FundingTierElement,
            "FundingGoalElement": FundingGoalElement
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
                    setattr(element, key, value)
            
            element.draw()
            self.elements.append(element)
            
            if isinstance(element, ProjectElement):
                self.project_element = element
                
    def get_element_properties(self, element: VisualElement) -> Dict[str, Any]:
        """Get serializable properties of an element"""
        props = {}
        for attr in dir(element):
            if not attr.startswith('_') and not callable(getattr(element, attr)):
                value = getattr(element, attr)
                if isinstance(value, (str, int, float, bool, list)) or value is None:
                    props[attr] = value
                elif hasattr(value, 'value'):  # Enum
                    props[attr] = value.value
        return props
        
    def show_export_summary(self, config: FundingConfiguration):
        """Show export summary dialog"""
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Export Summary")
        summary_window.geometry("500x400")
        
        text_widget = tk.Text(summary_window, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(summary_window, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Generate summary
        summary = f"""FUNDING CONFIGURATION EXPORT SUMMARY
{'='*50}

Project: {config.project_name}
Description: {config.description or 'None'}
Preferred Currency: {config.preferred_currency.value}

Beneficiaries ({len(config.beneficiaries)}):
"""
        for i, beneficiary in enumerate(config.beneficiaries, 1):
            summary += f"  {i}. {beneficiary.name}"
            if beneficiary.github_username:
                summary += f" (@{beneficiary.github_username})"
            summary += "\n"
        
        summary += f"\nFunding Sources ({len(config.funding_sources)}):\n"
        for i, source in enumerate(config.funding_sources, 1):
            summary += f"  {i}. {source.platform.value}: {source.username} ({source.funding_type.value})\n"
        
        summary += f"\nFunding Tiers ({len(config.tiers)}):\n"
        for i, tier in enumerate(config.tiers, 1):
            summary += f"  {i}. {tier.name}: {tier.amount}\n"
        
        summary += f"\nFunding Goals ({len(config.goals)}):\n"
        for i, goal in enumerate(config.goals, 1):
            summary += f"  {i}. {goal.name}: {goal.progress_percentage:.1f}% of {goal.target_amount}\n"
        
        summary += f"\n✅ Configuration is valid and ready for export!"
        
        text_widget.insert(tk.END, summary)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add close button
        ttk.Button(summary_window, text="Close", 
                  command=summary_window.destroy).pack(pady=10)
        
    def update_status(self, message: str):
        """Update status bar"""
        self.status_bar.config(text=message)
        
    def run(self):
        """Start the graphical editor"""
        self.root.mainloop()


# Property dialogs for each element type

class ProjectPropertiesDialog:
    def __init__(self, parent, element: ProjectElement):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Project Properties")
        dialog.geometry("400x300")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Project name
        ttk.Label(dialog, text="Project Name:").pack(pady=5)
        name_var = tk.StringVar(value=element.project_name)
        ttk.Entry(dialog, textvariable=name_var, width=40).pack(pady=5)
        
        # Description
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_text = tk.Text(dialog, height=4, width=40)
        desc_text.insert(tk.END, element.description)
        desc_text.pack(pady=5)
        
        # Currency
        ttk.Label(dialog, text="Preferred Currency:").pack(pady=5)
        currency_var = tk.StringVar(value=element.preferred_currency.value)
        currency_combo = ttk.Combobox(dialog, textvariable=currency_var,
                                     values=[c.value for c in CurrencyType])
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
            
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)


class BeneficiaryPropertiesDialog:
    def __init__(self, parent, element: BeneficiaryElement):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Beneficiary Properties")
        dialog.geometry("400x350")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Form fields
        fields = [
            ("Name:", "name"),
            ("Email:", "email"),
            ("GitHub Username:", "github_username"),
            ("Website:", "website")
        ]
        
        vars = {}
        for label, attr in fields:
            ttk.Label(dialog, text=label).pack(pady=2)
            var = tk.StringVar(value=getattr(element, attr))
            vars[attr] = var
            ttk.Entry(dialog, textvariable=var, width=40).pack(pady=2)
        
        # Description
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_text = tk.Text(dialog, height=3, width=40)
        desc_text.insert(tk.END, element.description)
        desc_text.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def save():
            self.result = {attr: var.get() for attr, var in vars.items()}
            self.result["description"] = desc_text.get("1.0", tk.END).strip()
            dialog.destroy()
            
        def cancel():
            dialog.destroy()
            
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)


class FundingSourcePropertiesDialog:
    def __init__(self, parent, element: FundingSourceElement):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Funding Source Properties")
        dialog.geometry("400x300")
        dialog.transient(parent)
        dialog.grab_set()
        
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
        ttk.Checkbutton(dialog, text="Active", variable=active_var).pack(pady=5)
        
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
            
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)


class FundingTierPropertiesDialog:
    def __init__(self, parent, element: FundingTierElement):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Funding Tier Properties")
        dialog.geometry("400x400")
        dialog.transient(parent)
        dialog.grab_set()
        
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
        ttk.Checkbutton(dialog, text="Active", variable=active_var).pack(pady=5)
        
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
            
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)


class FundingGoalPropertiesDialog:
    def __init__(self, parent, element: FundingGoalElement):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Funding Goal Properties")
        dialog.geometry("400x350")
        dialog.transient(parent)
        dialog.grab_set()
        
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
                "current_amount": current_var.get(),
                "currency": CurrencyType(currency_var.get()),
                "description": desc_text.get("1.0", tk.END).strip(),
                "deadline": deadline
            }
            dialog.destroy()
            
        def cancel():
            dialog.destroy()
            
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)


def main():
    """Launch the graphical funding editor"""
    editor = GraphicalFundingEditor()
    editor.run()


if __name__ == "__main__":
    main()