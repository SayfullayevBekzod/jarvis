"""
Jarvis UI Components - HUD Pro Edition
"""

import customtkinter as ctk
import config
import math
import random

class StatusIndicator(ctk.CTkFrame):
    """HUD Status Indicator with glow"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.indicator = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=14),
            text_color=config.PRIMARY_COLOR
        )
        self.indicator.pack(side="left", padx=5)
        
        self.status_text = ctk.CTkLabel(
            self,
            text="SYSTEM READY",
            font=ctk.CTkFont(size=11, weight="bold", family="Orbitron" if config.THEME == "dark" else "Arial"),
            text_color="#88AAFF"
        )
        self.status_text.pack(side="left")
    
    def set_status(self, status: str, color: str = "#00FF00"):
        self.indicator.configure(text_color=color)
        self.status_text.configure(text=status.upper())

class HUDMessageBubble(ctk.CTkFrame):
    """Futuristic HUD Message Bubble with clipped corners and neon borders"""
    
    def __init__(self, parent, text: str, is_user: bool = True, **kwargs):
        border = config.PRIMARY_COLOR if is_user else config.SECONDARY_COLOR
        bg = "#0c1a2b" if is_user else "#1a0c2b"
        
        super().__init__(parent, fg_color=bg, corner_radius=12, 
                         border_width=1, border_color=border, **kwargs)
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(padx=12, pady=8)
        
        header = "USER_INPUT" if is_user else "JARVIS_RESPONSE"
        self.header_lbl = ctk.CTkLabel(
            self.container, 
            text=f"// {header}", 
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=border
        )
        self.header_lbl.pack(anchor="w")
        
        self.msg_lbl = ctk.CTkLabel(
            self.container,
            text=text,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            wraplength=350,
            justify="left"
        )
        self.msg_lbl.pack(anchor="w", pady=(2, 0))

class TechDiagnosticBar(ctk.CTkFrame):
    """Decorative HUD diagnostic bar"""
    def __init__(self, parent, label="CPU_LOAD", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=9), text_color="#445566").pack(side="left", padx=5)
        
        self.bar = ctk.CTkProgressBar(self, width=100, height=4, fg_color="#1a1a1a", progress_color=config.PRIMARY_COLOR)
        self.bar.pack(side="left", padx=5)
        self.bar.set(0.4 + random.random() * 0.4)
        
        self._animate()

    def _animate(self):
        val = self.bar.get()
        new_val = val + (random.random() - 0.5) * 0.1
        new_val = max(0.2, min(0.9, new_val))
        self.bar.set(new_val)
        self.after(1000, self._animate)

class AnimatedBackground(ctk.CTkCanvas):
    """Futuristic HUD Background with Grid and Scanning Lines"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=kwargs.get("bg", config.BG_COLOR),
            highlightthickness=0,
            borderwidth=0,
            **kwargs
        )
        self.particles = []
        self.scan_line_y = 0
        self.grid_offset = 0
        self.animate = True
        self.width = 1
        self.height = 1
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self._init_particles()

    def _init_particles(self):
        self.particles = []
        for _ in range(30):
            self.particles.append({
                "x": random.randint(0, self.width),
                "y": random.randint(0, self.height),
                "vx": random.uniform(-0.3, 0.3),
                "vy": random.uniform(-0.3, 0.3),
                "r": random.uniform(1, 2),
                "color": random.choice([config.PRIMARY_COLOR, "#FFFFFF"]),
                "alpha": random.uniform(0.1, 0.3)
            })

    def start(self):
        self._draw()

    def stop(self):
        self.animate = False

    def _draw(self):
        if not self.animate: return
        self.delete("all")
        
        # 1. Digital Grid
        grid_size = 50
        self.grid_offset = (self.grid_offset + 0.5) % grid_size
        for x in range(int(-grid_size + self.grid_offset), self.width + grid_size, grid_size):
            self.create_line(x, 0, x, self.height, fill="#0a1525", width=1)
        for y in range(int(-grid_size + self.grid_offset), self.height + grid_size, grid_size):
            self.create_line(0, y, self.width, y, fill="#0a1525", width=1)

        # 2. Scanning Line
        self.scan_line_y = (self.scan_line_y + 2) % self.height
        self.create_line(0, self.scan_line_y, self.width, self.scan_line_y, fill="#1a3a5a", width=1)
        # Subtle glow for scan line
        for i in range(5):
            opacity = 5 - i
            self.create_line(0, self.scan_line_y - i, self.width, self.scan_line_y - i, fill="#081828", width=1)

        # 3. Particles & Connections
        for p in self.particles:
            p["x"] = (p["x"] + p["vx"]) % self.width
            p["y"] = (p["y"] + p["vy"]) % self.height
            self.create_oval(p["x"]-p["r"], p["y"]-p["r"], p["x"]+p["r"], p["y"]+p["r"], fill="#1a3a5a", outline="")
            
        # 4. Corner HUD Brackets
        margin = 20
        size = 40
        # TL
        self.create_line(margin, margin, margin+size, margin, fill=config.PRIMARY_COLOR, width=2)
        self.create_line(margin, margin, margin, margin+size, fill=config.PRIMARY_COLOR, width=2)
        # TR
        self.create_line(self.width-margin, margin, self.width-margin-size, margin, fill=config.PRIMARY_COLOR, width=2)
        self.create_line(self.width-margin, margin, self.width-margin, margin+size, fill=config.PRIMARY_COLOR, width=2)
        # BL
        self.create_line(margin, self.height-margin, margin+size, self.height-margin, fill=config.PRIMARY_COLOR, width=2)
        self.create_line(margin, self.height-margin, margin, self.height-margin-size, fill=config.PRIMARY_COLOR, width=2)
        # BR
        self.create_line(self.width-margin, self.height-margin, self.width-margin-size, self.height-margin, fill=config.PRIMARY_COLOR, width=2)
        self.create_line(self.width-margin, self.height-margin, self.width-margin, self.height-margin-size, fill=config.PRIMARY_COLOR, width=2)

        self.after(50, self._draw)

class MagneticButton(ctk.CTkButton):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
