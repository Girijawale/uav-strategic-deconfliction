"""
Visualization system for drone missions and conflicts.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Optional, Dict
import os

from models import Mission
from deconfliction_system import DeconflictionSystem


class Visualizer:
    """Visualization system for drone missions and conflicts."""
    
    def __init__(self, deconfliction_system: DeconflictionSystem):
        self.system = deconfliction_system
        
        # Create output directory if it doesn't exist
        if not os.path.exists('output'):
            os.makedirs('output')
    
    def plot_3d_static(self, primary_mission: Mission, 
                       simulated_flights: List[Mission],
                       result: Dict,
                       save_path: Optional[str] = None):
        """
        Create static 3D visualization of missions and conflicts.
        
        Args:
            primary_mission: Primary drone mission
            simulated_flights: Other drone flights
            result: Deconfliction result
            save_path: Optional path to save figure
        """
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot primary mission
        primary_path = np.array([wp.to_array() for wp in primary_mission.waypoints])
        ax.plot(primary_path[:, 0], primary_path[:, 1], primary_path[:, 2],
                'b-', linewidth=3, label='Primary Mission', marker='o', markersize=8)
        
        # Plot simulated flights
        colors = ['r', 'orange', 'purple', 'brown', 'pink']
        for i, flight in enumerate(simulated_flights):
            flight_path = np.array([wp.to_array() for wp in flight.waypoints])
            ax.plot(flight_path[:, 0], flight_path[:, 1], flight_path[:, 2],
                    color=colors[i % len(colors)], linestyle='--', linewidth=2,
                    label=f'Flight {flight.mission_id}', marker='s', markersize=5)
        
        # Highlight conflicts
        if result['conflicts']:
            conflict_points = np.array([c['location'].to_array() for c in result['conflicts']])
            ax.scatter(conflict_points[:, 0], conflict_points[:, 1], conflict_points[:, 2],
                      c='red', s=400, alpha=0.4, marker='o', 
                      edgecolors='darkred', linewidths=3, label='Conflict Zones')
        
        # Formatting
        ax.set_xlabel('X (meters)', fontsize=12, labelpad=10)
        ax.set_ylabel('Y (meters)', fontsize=12, labelpad=10)
        ax.set_zlabel('Altitude Z (meters)', fontsize=12, labelpad=10)
        
        title_color = 'red' if result['status'] == 'CONFLICT_DETECTED' else 'green'
        ax.set_title(f'4D Deconfliction Analysis\nStatus: {result["status"]}',
                    fontsize=16, fontweight='bold', pad=20, color=title_color)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Set equal aspect ratio
        all_points = primary_path
        for flight in simulated_flights:
            all_points = np.vstack([all_points, np.array([wp.to_array() for wp in flight.waypoints])])
        
        max_range = np.array([
            all_points[:, 0].max() - all_points[:, 0].min(),
            all_points[:, 1].max() - all_points[:, 1].min(),
            all_points[:, 2].max() - all_points[:, 2].min()
        ]).max() / 2.0
        
        mid_x = (all_points[:, 0].max() + all_points[:, 0].min()) * 0.5
        mid_y = (all_points[:, 1].max() + all_points[:, 1].min()) * 0.5
        mid_z = (all_points[:, 2].max() + all_points[:, 2].min()) * 0.5
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved 3D visualization to {save_path}")
        else:
            plt.show()
    
    def create_animation(self, primary_mission: Mission,
                        simulated_flights: List[Mission],
                        result: Dict,
                        save_path: Optional[str] = None):
        """
        Create animated 4D visualization of drone missions over time.
        
        Args:
            primary_mission: Primary drone mission
            simulated_flights: Other drone flights
            result: Deconfliction result
            save_path: Optional path to save animation
        """
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot paths (faded)
        primary_path = np.array([wp.to_array() for wp in primary_mission.waypoints])
        ax.plot(primary_path[:, 0], primary_path[:, 1], primary_path[:, 2],
                'b-', linewidth=2, alpha=0.3, label='Primary Path')
        
        colors = ['r', 'orange', 'purple', 'brown']
        for i, flight in enumerate(simulated_flights):
            flight_path = np.array([wp.to_array() for wp in flight.waypoints])
            ax.plot(flight_path[:, 0], flight_path[:, 1], flight_path[:, 2],
                    color=colors[i % len(colors)], linestyle='--', 
                    linewidth=2, alpha=0.3, label=f'Flight {flight.mission_id}')
        
        # Initialize drone markers
        primary_drone, = ax.plot([], [], [], 'bo', markersize=15, 
                                label='Primary Drone', markeredgecolor='darkblue', 
                                markeredgewidth=2)
        other_drones = []
        for i, _ in enumerate(simulated_flights):
            drone, = ax.plot([], [], [], 'o', markersize=12, 
                           color=colors[i % len(colors)],
                           markeredgecolor='black', markeredgewidth=1)
            other_drones.append(drone)
        
        # Conflict zone marker
        conflict_zone, = ax.plot([], [], [], 'ro', markersize=35, 
                                alpha=0.3, markeredgecolor='darkred', 
                                markeredgewidth=3)
        
        # Text annotations
        time_text = ax.text2D(0.02, 0.97, '', transform=ax.transAxes, 
                             fontsize=14, fontweight='bold',
                             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        status_text = ax.text2D(0.02, 0.92, '', transform=ax.transAxes, 
                               fontsize=12, fontweight='bold')
        
        def init():
            primary_drone.set_data([], [])
            primary_drone.set_3d_properties([])
            for drone in other_drones:
                drone.set_data([], [])
                drone.set_3d_properties([])
            conflict_zone.set_data([], [])
            conflict_zone.set_3d_properties([])
            return [primary_drone] + other_drones + [conflict_zone, time_text, status_text]
        
        def animate(frame):
            current_time = primary_mission.start_time + frame * 0.5
            
            # Update primary drone
            primary_pos = self.system.interpolate_position(primary_mission, current_time)
            if primary_pos:
                primary_drone.set_data([primary_pos.x], [primary_pos.y])
                primary_drone.set_3d_properties([primary_pos.z])
            else:
                primary_drone.set_data([], [])
                primary_drone.set_3d_properties([])
            
            # Update other drones
            for i, flight in enumerate(simulated_flights):
                pos = self.system.interpolate_position(flight, current_time)
                if pos:
                    other_drones[i].set_data([pos.x], [pos.y])
                    other_drones[i].set_3d_properties([pos.z])
                else:
                    other_drones[i].set_data([], [])
                    other_drones[i].set_3d_properties([])
            
            # Check for conflicts at current time
            in_conflict = False
            for conflict in result['conflicts']:
                if conflict['start_time'] <= current_time <= conflict['end_time']:
                    in_conflict = True
                    conflict_zone.set_data([conflict['location'].x], [conflict['location'].y])
                    conflict_zone.set_3d_properties([conflict['location'].z])
                    break
            
            if not in_conflict:
                conflict_zone.set_data([], [])
                conflict_zone.set_3d_properties([])
            
            time_text.set_text(f'Time: {current_time:.1f}s / {primary_mission.end_time:.1f}s')
            status = '⚠ CONFLICT DETECTED' if in_conflict else '✓ Clear'
            status_color = 'red' if in_conflict else 'green'
            status_text.set_text(f'Status: {status}')
            status_text.set_color(status_color)
            
            return [primary_drone] + other_drones + [conflict_zone, time_text, status_text]
        
        # Set up axes
        ax.set_xlabel('X (meters)', fontsize=12, labelpad=10)
        ax.set_ylabel('Y (meters)', fontsize=12, labelpad=10)
        ax.set_zlabel('Altitude Z (meters)', fontsize=12, labelpad=10)
        ax.set_title('4D Deconfliction Simulation (3D Space + Time)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Set limits
        all_points = primary_path
        for flight in simulated_flights:
            all_points = np.vstack([all_points, np.array([wp.to_array() for wp in flight.waypoints])])
        
        margin = 50
        ax.set_xlim(all_points[:, 0].min() - margin, all_points[:, 0].max() + margin)
        ax.set_ylim(all_points[:, 1].min() - margin, all_points[:, 1].max() + margin)
        ax.set_zlim(all_points[:, 2].min() - margin, all_points[:, 2].max() + margin)
        
        # Create animation
        num_frames = int((primary_mission.end_time - primary_mission.start_time) / 0.5)
        anim = FuncAnimation(fig, animate, init_func=init, frames=num_frames,
                           interval=50, blit=True, repeat=True)
        
        if save_path:
            writer = PillowWriter(fps=20)
            anim.save(save_path, writer=writer)
            print(f"✓ Saved animation to {save_path}")
        else:
            plt.show()

