"""
Predefined test scenarios for the deconfliction system.
"""

from models import Mission, Waypoint


def create_conflict_scenario():
    """
    Create a scenario with multiple conflicts.
    
    This scenario demonstrates:
    - Head-on collision course (PRIMARY vs ALPHA)
    - Crossing path conflict (PRIMARY vs BETA)
    """
    primary = Mission(
        waypoints=[
            Waypoint(0, 0, 100),
            Waypoint(100, 100, 150),
            Waypoint(200, 100, 100),
            Waypoint(300, 0, 100)
        ],
        start_time=0,
        end_time=60,
        mission_id="PRIMARY"
    )
    
    simulated = [
        Mission(
            waypoints=[
                Waypoint(300, 0, 100),
                Waypoint(200, 50, 120),
                Waypoint(100, 100, 140),
                Waypoint(0, 150, 100)
            ],
            start_time=0,
            end_time=60,
            mission_id="ALPHA"
        ),
        Mission(
            waypoints=[
                Waypoint(150, 0, 80),
                Waypoint(150, 200, 120)
            ],
            start_time=20,
            end_time=50,
            mission_id="BETA"
        )
    ]
    
    return primary, simulated


def create_clear_scenario():
    """
    Create a scenario with no conflicts.
    
    This scenario demonstrates:
    - Spatial separation (different altitudes/locations)
    - Temporal separation (non-overlapping time windows)
    """
    primary = Mission(
        waypoints=[
            Waypoint(0, 0, 100),
            Waypoint(100, 0, 100),
            Waypoint(200, 0, 100)
        ],
        start_time=0,
        end_time=40,
        mission_id="PRIMARY"
    )
    
    simulated = [
        Mission(
            waypoints=[
                Waypoint(0, 200, 150),
                Waypoint(200, 200, 150)
            ],
            start_time=0,
            end_time=40,
            mission_id="ALPHA"
        ),
        Mission(
            waypoints=[
                Waypoint(100, 100, 50),
                Waypoint(100, 100, 200)
            ],
            start_time=50,
            end_time=70,
            mission_id="BETA"
        )
    ]
    
    return primary, simulated


def create_near_miss_scenario():
    """
    Create a scenario with a near miss (close but safe).
    
    This scenario demonstrates the safety buffer working correctly.
    """
    primary = Mission(
        waypoints=[
            Waypoint(0, 0, 100),
            Waypoint(200, 0, 100)
        ],
        start_time=0,
        end_time=40,
        mission_id="PRIMARY"
    )
    
    simulated = [
        Mission(
            waypoints=[
                Waypoint(100, 60, 100),  # 60m away - just outside safety buffer
                Waypoint(100, 60, 150)
            ],
            start_time=0,
            end_time=40,
            mission_id="ALPHA"
        )
    ]
    
    return primary, simulated

