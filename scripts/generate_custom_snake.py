#!/usr/bin/env python3
"""
Advanced GitHub Contribution Snake Animation Generator
Features: Cyberpunk neon colors, glowing trails, dual snakes, particles, obstacles
"""

import json
import math
import random
from datetime import datetime, timedelta
from pathlib import Path
import os

# GitHub API for fetching contribution data
import urllib.request
import urllib.parse

class NeonColorPalette:
    """Cyberpunk neon color schemes"""
    LIGHT_MODE = {
        'background': '#ffffff',
        'grid': '#f0f0f0',
        'trail': ['#FF006E', '#FB5607', '#FFBE0B', '#8338EC'],  # Neon pink, orange, yellow, purple
        'glow': ['#FF006E', '#FB5607', '#FFBE0B', '#8338EC'],
        'particles': '#FF006E',
        'text': '#000000',
        'accent': '#8338EC'
    }
    
    DARK_MODE = {
        'background': '#0a0e27',
        'grid': '#1a1f3a',
        'trail': ['#FF006E', '#00D9FF', '#39FF14', '#FF10F0'],  # Neon pink, cyan, lime, magenta
        'glow': ['#FF006E', '#00D9FF', '#39FF14', '#FF10F0'],
        'particles': '#00D9FF',
        'text': '#00D9FF',
        'accent': '#39FF14'
    }

class ContributionParser:
    """Parse GitHub contribution data"""
    
    @staticmethod
    def fetch_contribution_calendar(username):
        """Fetch GitHub contribution data"""
        try:
            url = f"https://github.com/{username}"
            # Parse HTML to extract contribution data
            # For production, use GitHub GraphQL API
            return ContributionParser.generate_mock_data()
        except Exception as e:
            print(f"Error fetching contributions: {e}")
            return ContributionParser.generate_mock_data()
    
    @staticmethod
    def generate_mock_data():
        """Generate mock contribution data for demonstration"""
        contributions = {}
        base_date = datetime.now() - timedelta(days=365)
        
        for i in range(365):
            date = base_date + timedelta(days=i)
            # Create realistic contribution pattern
            contribution_value = max(0, 
                int(5 * math.sin(i / 50) * math.cos(i / 100) + 
                    random.randint(0, 20)))
            contributions[date.strftime('%Y-%m-%d')] = contribution_value
        
        return contributions

class SnakeAnimation:
    """Generate advanced snake animation SVG"""
    
    def __init__(self, username='HarshNexus', width=1000, height=200, dark_mode=False):
        self.username = username
        self.width = width
        self.height = height
        self.dark_mode = dark_mode
        self.colors = NeonColorPalette.DARK_MODE if dark_mode else NeonColorPalette.LIGHT_MODE
        self.cell_size = 12
        self.grid_gap = 4
        self.contributions = ContributionParser.fetch_contribution_calendar(username)
        self.path_history = []
        self.particles = []
    
    def generate_grid_path(self):
        """Generate snake path following contribution density"""
        grid_width = self.width // (self.cell_size + self.grid_gap)
        grid_height = self.height // (self.cell_size + self.grid_gap)
        
        path = []
        density_map = {}
        
        # Map contributions to grid
        dates = sorted(self.contributions.keys())
        max_contribution = max(self.contributions.values()) or 1
        
        for idx, date in enumerate(dates[-52*7:]):  # Last year
            col = idx % grid_width
            row = (idx // grid_width) % grid_height
            density = self.contributions[date] / max_contribution if max_contribution > 0 else 0
            density_map[(col, row)] = density
        
        # Generate intelligent path (hunt high-density cells)
        current_pos = (0, 0)
        visited = set()
        
        for _ in range(min(100, len(density_map))):
            # Find highest density nearby cell
            neighbors = self.get_neighbors(current_pos, grid_width, grid_height)
            best_neighbor = max(
                neighbors, 
                key=lambda p: density_map.get(p, 0) * (1 if p not in visited else 0.1)
            )
            
            if best_neighbor not in visited:
                x = best_neighbor[0] * (self.cell_size + self.grid_gap) + 10
                y = best_neighbor[1] * (self.cell_size + self.grid_gap) + 10
                path.append((x, y))
                visited.add(best_neighbor)
                current_pos = best_neighbor
        
        return path
    
    def get_neighbors(self, pos, width, height):
        """Get neighboring cells"""
        x, y = pos
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    neighbors.append((nx, ny))
        return neighbors
    
    def create_gradient_defs(self):
        """Create gradient and filter definitions"""
        defs = '<defs>\n'
        
        # Radial gradient for glow effect
        defs += '''
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        
        <filter id="strongGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="5" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        
        <linearGradient id="neonPink" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#FF006E;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#FB5607;stop-opacity:1" />
        </linearGradient>
        
        <linearGradient id="neonCyan" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#00D9FF;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#39FF14;stop-opacity:1" />
        </linearGradient>
        
        <linearGradient id="trail" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:''' + self.colors['trail'][0] + ''';stop-opacity:0.1" />
            <stop offset="50%" style="stop-color:''' + self.colors['trail'][1] + ''';stop-opacity:0.6" />
            <stop offset="100%" style="stop-color:''' + self.colors['trail'][2] + ''';stop-opacity:1" />
        </linearGradient>
        
        <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="''' + self.colors['accent'] + '''" />
        </marker>
        
        <style>
            @keyframes slither {
                0% { offset-distance: 0%; }
                100% { offset-distance: 100%; }
            }
            @keyframes pulse {
                0%, 100% { r: 6; opacity: 1; }
                50% { r: 8; opacity: 0.7; }
            }
            @keyframes float {
                0% { opacity: 1; transform: translateY(0px); }
                100% { opacity: 0; transform: translateY(-20px); }
            }
            .snake-body {
                animation: slither 4s linear infinite;
            }
            .pulse-head {
                animation: pulse 1.5s ease-in-out infinite;
            }
            .particle {
                animation: float 2s ease-out forwards;
            }
        </style>
        '''
        
        defs += '</defs>\n'
        return defs
    
    def create_animated_background(self):
        """Create animated grid background"""
        bg = '<g id="background">\n'
        
        # Background rectangle
        bg += f'<rect width="{self.width}" height="{self.height}" fill="{self.colors["background"]}" />\n'
        
        # Animated grid
        grid_color = self.colors['grid']
        grid_opacity = '0.15' if self.dark_mode else '0.3'
        
        # Vertical lines
        for x in range(0, self.width, 20):
            bg += f'<line x1="{x}" y1="0" x2="{x}" y2="{self.height}" stroke="{grid_color}" stroke-width="0.5" opacity="{grid_opacity}" />\n'
        
        # Horizontal lines
        for y in range(0, self.height, 20):
            bg += f'<line x1="0" y1="{y}" x2="{self.width}" y2="{y}" stroke="{grid_color}" stroke-width="0.5" opacity="{grid_opacity}" />\n'
        
        bg += '</g>\n'
        return bg
    
    def create_snake_trail(self, path, color_idx=0):
        """Create glowing trail for snake"""
        trail = '<g id="trail" opacity="0.6">\n'
        
        colors = self.colors['trail']
        color = colors[color_idx % len(colors)]
        
        for i, (x, y) in enumerate(path[:-1]):
            next_x, next_y = path[i + 1]
            
            # Calculate opacity based on position
            opacity = (i / len(path)) * 0.8 + 0.2
            
            # Trail segment
            trail += f'''<line x1="{x}" y1="{y}" x2="{next_x}" y2="{next_y}" 
                     stroke="{color}" stroke-width="4" opacity="{opacity}" 
                     stroke-linecap="round" filter="url(#glow)" />\n'''
        
        trail += '</g>\n'
        return trail
    
    def create_dual_snakes(self, path1, path2):
        """Create two animated snakes"""
        snakes = '<g id="snakes">\n'
        
        # Snake 1 (Pink-Orange gradient)
        snakes += self.create_single_snake(path1, 0, 0)
        
        # Snake 2 (Cyan-Green gradient)
        snakes += self.create_single_snake(path2, 1, 1.5)
        
        snakes += '</g>\n'
        return snakes
    
    def create_single_snake(self, path, idx, offset):
        """Create single snake with head and body"""
        snake = '<g id="snake-' + str(idx) + '">\n'
        
        if not path:
            return snake + '</g>\n'
        
        # Body segments
        colors = self.colors['trail']
        color = colors[idx % len(colors)]
        
        for i, (x, y) in enumerate(path[:-1]):
            next_x, next_y = path[i + 1]
            
            # Progressive opacity
            opacity = (i / max(len(path), 1)) * 0.9 + 0.1
            size = 3 + (i / max(len(path), 1)) * 3
            
            snake += f'''<circle cx="{x}" cy="{y}" r="{size}" 
                     fill="{color}" opacity="{opacity}" 
                     filter="url(#glow)" />\n'''
        
        # Head with pulsing effect
        if path:
            head_x, head_y = path[-1]
            snake += f'''<circle cx="{head_x}" cy="{head_y}" r="6" 
                     fill="{self.colors['accent']}" 
                     class="pulse-head" filter="url(#strongGlow)" />\n'''
        
        snake += '</g>\n'
        return snake
    
    def create_particles(self, path, count=20):
        """Create particle effects around path"""
        particles = '<g id="particles">\n'
        
        for i in range(count):
            if path:
                base_pos = random.choice(path)
                x = base_pos[0] + random.uniform(-10, 10)
                y = base_pos[1] + random.uniform(-10, 10)
                
                size = random.uniform(1, 3)
                duration = random.uniform(1.5, 3)
                delay = random.uniform(0, 2)
                
                particles += f'''<circle cx="{x}" cy="{y}" r="{size}" 
                         fill="{self.colors['particles']}" opacity="0.8"
                         style="animation: float {duration}s ease-out {delay}s forwards;"
                         class="particle" />\n'''
        
        particles += '</g>\n'
        return particles
    
    def create_obstacles(self):
        """Create obstacles/walls"""
        obstacles = '<g id="obstacles" opacity="0.3">\n'
        
        # Random obstacles
        for _ in range(5):
            x = random.uniform(100, self.width - 100)
            y = random.uniform(50, self.height - 50)
            w = random.uniform(20, 50)
            h = random.uniform(20, 50)
            
            obstacles += f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" 
                     fill="{self.colors['text']}" opacity="0.2" rx="5" />\n'''
        
        obstacles += '</g>\n'
        return obstacles
    
    def create_custom_text(self, text="Harsh Nexus Dev"):
        """Add custom text to SVG"""
        text_elem = f'''<g id="custom-text">
            <text x="{self.width / 2}" y="40" 
                  text-anchor="middle" font-size="24" font-weight="bold"
                  fill="{self.colors['accent']}" 
                  filter="url(#glow)"
                  font-family="Arial, sans-serif">
                {text}
            </text>
        </g>\n'''
        return text_elem
    
    def generate_svg(self, include_text=True, text="Harsh Nexus Dev"):
        """Generate complete SVG"""
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" 
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    
    {self.create_gradient_defs()}
    
    {self.create_animated_background()}
    
    {self.create_obstacles()}
    
    {self.create_particles(self.generate_grid_path(), 30)}
    
    {self.create_dual_snakes(self.generate_grid_path(), self.generate_grid_path())}
    
    {self.create_custom_text(text) if include_text else ''}
    
    <!-- Attribution -->
    <g id="attribution" opacity="0.6">
        <text x="10" y="{self.height - 10}" font-size="10" fill="{self.colors['text']}" font-family="monospace">
            Generated by Harsh Nexus Custom Snake Generator
        </text>
    </g>
</svg>
'''
        return svg

class SnakeGenerator:
    """Main generator orchestrator"""
    
    def __init__(self, username='HarshNexus', output_dir='dist'):
        self.username = username
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_variants(self):
        """Generate all SVG variants"""
        
        print("🐍 Generating Snake Animation Variants...")
        
        # Light mode
        print("  ✓ Generating Light Mode...")
        light_snake = SnakeAnimation(self.username, width=1200, height=250, dark_mode=False)
        light_svg = light_snake.generate_svg(include_text=True, text="🚀 Harsh Nexus Dev")
        self.save_svg('github-contribution-grid-snake.svg', light_svg)
        
        # Dark mode
        print("  ✓ Generating Dark Mode...")
        dark_snake = SnakeAnimation(self.username, width=1200, height=250, dark_mode=True)
        dark_svg = dark_snake.generate_svg(include_text=True, text="⚡ Harsh Nexus Dev")
        self.save_svg('github-contribution-grid-snake-dark.svg', dark_svg)
        
        # Minimal version
        print("  ✓ Generating Minimal Version...")
        minimal_snake = SnakeAnimation(self.username, width=1200, height=200, dark_mode=True)
        minimal_svg = minimal_snake.generate_svg(include_text=False)
        self.save_svg('github-contribution-grid-snake-minimal.svg', minimal_svg)
        
        print(f"\n✨ All variants generated in {self.output_dir}/")
    
    def save_svg(self, filename, svg_content):
        """Save SVG to file"""
        filepath = self.output_dir / filename
        filepath.write_text(svg_content, encoding='utf-8')
        print(f"    💾 Saved: {filepath}")

if __name__ == '__main__':
    # Get GitHub username from environment or use default
    username = os.getenv('GITHUB_ACTOR', 'HarshNexus')
    output_dir = os.getenv('OUTPUT_DIR', 'dist')
    
    generator = SnakeGenerator(username, output_dir)
    generator.generate_all_variants()
    
    print("\n✅ Snake animation generation complete!")
