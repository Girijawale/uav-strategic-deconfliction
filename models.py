"""
Data models for the deconfliction system.
"""

from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class Waypoint:
    """Represents a 3D waypoint with spatial coordinates."""
    x: float
    y: float
    z: float
    
    def to_array(self) -> np.ndarray:
        """Convert waypoint to numpy array."""
        return np.array([self.x, self.y, self.z])
    
    def __repr__(self):
        return f"Waypoint(x={self.x:.1f}, y={self.y:.1f}, z={self.z:.1f})"


@dataclass
class Mission:
    """Represents a drone mission with waypoints and time window."""
    waypoints: List[Waypoint]
    start_time: float
    end_time: float
    mission_id: str = "PRIMARY"
    
    def duration(self) -> float:
        """Calculate mission duration."""
        return self.end_time - self.start_time
    
    def __repr__(self):
        return f"Mission(id={self.mission_id}, waypoints={len(self.waypoints)}, duration={self.duration():.1f}s)"


@dataclass
class Conflict:
    """Represents a detected conflict between drones."""
    time: float
    location: Waypoint
    distance: float
    primary_position: Waypoint
    other_position: Waypoint
    flight_id: str
    flight_name: str
    
    def __repr__(self):
        return (f"Conflict(time={self.time:.1f}s, distance={self.distance:.2f}m, "
                f"flight={self.flight_name}, location={self.location})")

