import numpy as np
from typing import List, Optional, Dict
from models import Waypoint, Mission, Conflict


class DeconflictionSystem:
    """
    Strategic deconfliction system for verifying drone mission safety.
    
    This system performs 4D (3D space + time) conflict detection.
    """
    
    def __init__(self, safety_buffer: float = 50.0, time_resolution: float = 1.0):
        """
        Initialize the deconfliction system.
        
        Args:
            safety_buffer: Minimum safe separation distance in meters
            time_resolution: Time step for conflict checking in seconds
        """
        self.safety_buffer = safety_buffer
        self.time_resolution = time_resolution
        self.conflicts: List[Conflict] = []
        
    def distance_3d(self, p1: Waypoint, p2: Waypoint) -> float:
        """Calculate 3D Euclidean distance between two waypoints."""
        return np.linalg.norm(p1.to_array() - p2.to_array())
    
    def interpolate_position(self, mission: Mission, current_time: float) -> Optional[Waypoint]:
        """
        Interpolate drone position at a specific time (4D calculation).
        
        This is the core 4D function: calculates 3D position as a function of time.
        """
        if current_time < mission.start_time or current_time > mission.end_time:
            return None
        
        total_distance = self._calculate_path_length(mission.waypoints)
        time_elapsed = current_time - mission.start_time
        total_duration = mission.end_time - mission.start_time
        progress = time_elapsed / total_duration
        target_distance = progress * total_distance
        
        accumulated_distance = 0.0
        for i in range(len(mission.waypoints) - 1):
            segment_length = self.distance_3d(mission.waypoints[i], mission.waypoints[i + 1])
            
            if accumulated_distance + segment_length >= target_distance:
                segment_progress = (target_distance - accumulated_distance) / segment_length
                return self._lerp_waypoint(
                    mission.waypoints[i],
                    mission.waypoints[i + 1],
                    segment_progress
                )
            
            accumulated_distance += segment_length
        
        return mission.waypoints[-1]
    
    def _calculate_path_length(self, waypoints: List[Waypoint]) -> float:
        """Calculate total length of path through waypoints."""
        length = 0.0
        for i in range(len(waypoints) - 1):
            length += self.distance_3d(waypoints[i], waypoints[i + 1])
        return length
    
    def _lerp_waypoint(self, p1: Waypoint, p2: Waypoint, t: float) -> Waypoint:
        """Linear interpolation between two waypoints."""
        return Waypoint(
            x=p1.x + (p2.x - p1.x) * t,
            y=p1.y + (p2.y - p1.y) * t,
            z=p1.z + (p2.z - p1.z) * t
        )
    
    def check_mission(self, primary_mission: Mission, 
                     simulated_flights: List[Mission]) -> Dict:
        """
        Main deconfliction check - 4D spatiotemporal analysis.
        
        Returns:
            Dictionary containing status, conflicts, and summary
        """
        self.conflicts = []
        
        # 4D analysis: check each time step
        current_time = primary_mission.start_time
        while current_time <= primary_mission.end_time:
            primary_pos = self.interpolate_position(primary_mission, current_time)
            
            if primary_pos is None:
                current_time += self.time_resolution
                continue
            
            for flight in simulated_flights:
                other_pos = self.interpolate_position(flight, current_time)
                
                if other_pos is None:
                    continue
                
                distance = self.distance_3d(primary_pos, other_pos)
                
                if distance < self.safety_buffer:
                    conflict = Conflict(
                        time=current_time,
                        location=primary_pos,
                        distance=distance,
                        primary_position=primary_pos,
                        other_position=other_pos,
                        flight_id=flight.mission_id,
                        flight_name=flight.mission_id
                    )
                    self.conflicts.append(conflict)
            
            current_time += self.time_resolution
        
        consolidated_conflicts = self._consolidate_conflicts(self.conflicts)
        summary = self._generate_summary(consolidated_conflicts)
        
        return {
            'status': 'CLEAR' if len(consolidated_conflicts) == 0 else 'CONFLICT_DETECTED',
            'conflicts': consolidated_conflicts,
            'summary': summary
        }
    
    def _consolidate_conflicts(self, conflicts: List[Conflict]) -> List[Dict]:
        """Consolidate consecutive conflicts into time windows."""
        if not conflicts:
            return []
        
        consolidated = []
        current = {
            'start_time': conflicts[0].time,
            'end_time': conflicts[0].time,
            'location': conflicts[0].location,
            'min_distance': conflicts[0].distance,
            'flight_id': conflicts[0].flight_id,
            'flight_name': conflicts[0].flight_name
        }
        
        for conflict in conflicts[1:]:
            if (conflict.flight_id == current['flight_id'] and 
                conflict.time - current['end_time'] <= 2 * self.time_resolution):
                current['end_time'] = conflict.time
                current['min_distance'] = min(current['min_distance'], conflict.distance)
            else:
                consolidated.append(current.copy())
                current = {
                    'start_time': conflict.time,
                    'end_time': conflict.time,
                    'location': conflict.location,
                    'min_distance': conflict.distance,
                    'flight_id': conflict.flight_id,
                    'flight_name': conflict.flight_name
                }
        
        consolidated.append(current)
        return consolidated
    
    def _generate_summary(self, conflicts: List[Dict]) -> Dict:
        """Generate summary statistics for conflict report."""
        if not conflicts:
            return {
                'total_conflicts': 0,
                'affected_flights': 0,
                'minimum_distance': None,
                'message': '✓ MISSION CLEAR - No conflicts detected. Safe to execute.'
            }
        
        unique_flights = set(c['flight_id'] for c in conflicts)
        min_distance = min(c['min_distance'] for c in conflicts)
        
        return {
            'total_conflicts': len(conflicts),
            'affected_flights': len(unique_flights),
            'minimum_distance': min_distance,
            'message': f'✗ CONFLICT DETECTED - {len(conflicts)} conflict window(s) with {len(unique_flights)} flight(s). Minimum separation: {min_distance:.2f}m'
        }
    
    def print_report(self, result: Dict):
        """Print detailed conflict report to console."""
        print("\n" + "="*70)
        print("DECONFLICTION SYSTEM REPORT")
        print("="*70)
        print(f"\nStatus: {result['status']}")
        print(f"Safety Buffer: {self.safety_buffer}m")
        print(f"\n{result['summary']['message']}")
        
        if result['conflicts']:
            print(f"\n{'─'*70}")
            print("CONFLICT DETAILS:")
            print(f"{'─'*70}")
            
            for i, conflict in enumerate(result['conflicts'], 1):
                print(f"\nConflict #{i}:")
                print(f"  Flight: {conflict['flight_name']}")
                print(f"  Time Window: {conflict['start_time']:.1f}s - {conflict['end_time']:.1f}s")
                print(f"  Location: ({conflict['location'].x:.1f}, {conflict['location'].y:.1f}, {conflict['location'].z:.1f})")
                print(f"  Minimum Separation: {conflict['min_distance']:.2f}m")
                print(f"  ⚠ VIOLATION: {self.safety_buffer - conflict['min_distance']:.2f}m below safety buffer")
        
        print("\n" + "="*70 + "\n")