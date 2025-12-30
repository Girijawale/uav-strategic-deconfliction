4D Drone Deconfliction System
Strategic Airspace Management - 3D Space + Time Analysis
Built for FlytBase Robotics Assignment 2025.

🎯 Overview
This system acts as the final authority for verifying whether a drone's planned waypoint mission is safe to execute in shared airspace. It performs comprehensive conflict detection by analyzing missions in four dimensions:

X, Y, Z coordinates (3D spatial positioning)
Time (temporal overlap detection)
The system checks a primary mission against multiple simulated flights and identifies any safety buffer violations with precise conflict location, timing, and severity reporting.

✨ Key Features
4D Conflict Detection: Full spatiotemporal analysis (3D space + time)
Safety Buffer Enforcement: Configurable minimum separation distance (default: 50m)
Temporal Resolution: Adjustable time-step precision (default: 1s)
Conflict Consolidation: Groups consecutive conflicts into time windows
Comprehensive Reporting: Detailed conflict reports with location, time, and severity
Rich Visualization:
Static 3D trajectory plots
Animated 4D simulations showing temporal evolution
Conflict zone highlighting
Multiple Test Scenarios: Pre-configured conflict, clear, and near-miss scenarios

📋 Requirements
System Requirements
Python 3.8+
pip (Python package manager)
Python Dependencies
numpy>=1.21.0
matplotlib>=3.4.0
🚀 Quick Start
1. Installation
Clone the repository and install dependencies:

bash
# Clone the repository
git clone <https://github.com/Girijawale/uav-strategic-deconfliction>
cd uav-strategic-deconfliction

# Install required packages
pip install numpy matplotlib

# Create output directory
mkdir output
2. Run the System
Execute the main program to run all test scenarios:

bash
python main.py
This will:

Run 3 predefined scenarios (Conflict Detection, Clear Mission, Near Miss)
Generate detailed console reports for each scenario
Create visualizations in the output/ folder
3. View Results
After execution, check the output/ folder for:

3D static plots (*_3d.png) - Spatial trajectory visualization
Animated simulations (*_animation.gif) - Time-evolving 4D visualization
📂 Project Structure
drone-deconfliction-system/
│
├── main.py                      # Main execution script
├── deconfliction_system.py      # Core 4D conflict detection logic
├── models.py                    # Data models (Waypoint, Mission, Conflict)
├── scenarios.py                 # Predefined test scenarios
├── visualizer.py                # Visualization and animation system
├── README.md                    # This file
│
└── output/                      # Generated visualizations (auto-created)
    ├── conflict_detection_3d.png
    ├── conflict_detection_animation.gif
    ├── clear_mission_3d.png
    ├── clear_mission_animation.gif
    ├── near_miss_3d.png
    └── near_miss_animation.gif


🔧 Usage Examples
Basic Usage
python

from deconfliction_system import DeconflictionSystem
from models import Mission, Waypoint

# Initialize system with custom parameters
system = DeconflictionSystem(
    safety_buffer=50.0,      # meters
    time_resolution=1.0      # seconds
)

# Define primary mission
primary = Mission(
    waypoints=[
        Waypoint(0, 0, 100),
        Waypoint(100, 100, 150),
        Waypoint(200, 100, 100)
    ],
    start_time=0,
    end_time=60,
    mission_id="PRIMARY"
)

# Define simulated flights
simulated = [
    Mission(
        waypoints=[
            Waypoint(200, 100, 100),
            Waypoint(0, 0, 100)
        ],
        start_time=0,
        end_time=60,
        mission_id="ALPHA"
    )
]

# Run deconfliction check
result = system.check_mission(primary, simulated)

# Print report
system.print_report(result)

# Access results programmatically
if result['status'] == 'CONFLICT_DETECTED':
    print(f"Found {result['summary']['total_conflicts']} conflicts")
    print(f"Minimum separation: {result['summary']['minimum_distance']:.2f}m")
Creating Custom Scenarios
python
from models import Mission, Waypoint

# Define your custom mission
custom_mission = Mission(
    waypoints=[
        Waypoint(x=0, y=0, z=100),      # Start point
        Waypoint(x=50, y=50, z=120),    # Intermediate
        Waypoint(x=100, y=100, z=100)   # End point
    ],
    start_time=0,      # seconds
    end_time=30,       # seconds
    mission_id="CUSTOM"
)
Visualization
python
from visualizer import Visualizer

visualizer = Visualizer(system)

# Create static 3D plot
visualizer.plot_3d_static(
    primary, 
    simulated, 
    result,
    save_path='output/my_scenario_3d.png'
)

# Create animated visualization
visualizer.create_animation(
    primary,
    simulated,
    result,
    save_path='output/my_scenario_animation.gif'
)
🧪 Test Scenarios
The system includes three predefined test scenarios in scenarios.py:

1. Conflict Detection Scenario
Purpose: Validates conflict detection capabilities
Setup: Multiple drones with crossing paths and head-on collisions
Expected: Multiple conflicts detected
Output: conflict_detection_* files
2. Clear Mission Scenario
Purpose: Validates absence of false positives
Setup: Well-separated missions (spatial and temporal)
Expected: No conflicts (CLEAR status)
Output: clear_mission_* files
3. Near Miss Scenario
Purpose: Validates safety buffer threshold enforcement
Setup: Drones pass within ~60m (just outside 50m buffer)
Expected: No conflicts, but close proximity
Output: near_miss_* files
⚙️ Configuration
System Parameters
Adjust in main.py or when initializing DeconflictionSystem:

python
system = DeconflictionSystem(
    safety_buffer=50.0,      # Minimum safe separation (meters)
    time_resolution=1.0      # Time step for checks (seconds)
)
Parameter Guidelines:

safety_buffer: Larger values = more conservative (typical: 30-100m)
time_resolution: Smaller values = higher precision but slower (typical: 0.5-2s)
Mission Parameters
When creating missions:

python
Mission(
    waypoints=[...],         # List of Waypoint objects
    start_time=0,           # Mission start time (seconds)
    end_time=60,            # Mission end time (seconds)
    mission_id="NAME"       # Unique identifier
)
📊 Output Format
Console Report
======================================================================
DECONFLICTION SYSTEM REPORT
======================================================================

Status: CONFLICT_DETECTED
Safety Buffer: 50.0m

✗ CONFLICT DETECTED - 2 conflict window(s) with 2 flight(s). 
  Minimum separation: 15.23m

──────────────────────────────────────────────────────────────────────
CONFLICT DETAILS:
──────────────────────────────────────────────────────────────────────

Conflict #1:
  Flight: ALPHA
  Time Window: 25.0s - 35.0s
  Location: (100.0, 100.0, 145.0)
  Minimum Separation: 15.23m
  ⚠ VIOLATION: 34.77m below safety buffer
Programmatic Access
python
result = {
    'status': 'CONFLICT_DETECTED',  # or 'CLEAR'
    'conflicts': [
        {
            'start_time': 25.0,
            'end_time': 35.0,
            'location': Waypoint(...),
            'min_distance': 15.23,
            'flight_id': 'ALPHA'
        }
    ],
    'summary': {
        'total_conflicts': 2,
        'affected_flights': 2,
        'minimum_distance': 15.23,
        'message': '...'
    }
}
🏗️ Architecture
Core Components
DeconflictionSystem (deconfliction_system.py)
4D interpolation engine
Conflict detection algorithm
Temporal-spatial analysis
Data Models (models.py)
Waypoint: 3D spatial coordinates
Mission: Waypoint sequence + time window
Conflict: Detected safety violations
Scenarios (scenarios.py)
Predefined test cases
Edge case validation
Visualizer (visualizer.py)
3D static plotting
4D animation generation
Conflict highlighting
Algorithm Overview
For each time step in primary mission:
  1. Interpolate primary drone position
  2. For each simulated flight:
     a. Interpolate other drone position
     b. Calculate 3D distance
     c. If distance < safety_buffer:
        - Record conflict
  3. Advance time by time_resolution

Consolidate conflicts into time windows
Generate detailed report
🔍 Edge Cases Handled
✅ Zero-length paths (stationary drones)
✅ Single-waypoint missions
✅ Non-overlapping time windows
✅ Identical waypoint positions
✅ Zero mission duration
✅ Empty simulated flight lists
🚀 Scalability Considerations
See the reflection document for detailed scalability discussion. Key considerations for production deployment:

Spatial Indexing: R-tree or Octree for O(log n) lookups
Distributed Computing: Microservices architecture for parallel processing
Streaming Data: Real-time ingestion pipelines (Kafka, Redis)
Predictive Algorithms: Machine learning for conflict prediction
Caching: Redis for frequently queried trajectories
Database: Time-series DB (InfluxDB) for historical data
🐛 Troubleshooting
Common Issues
Issue: ModuleNotFoundError: No module named 'numpy'

bash
# Solution
pip install numpy matplotlib
Issue: FileNotFoundError: [Errno 2] No such file or directory: 'output'

bash
# Solution
mkdir output
Issue: Animation generation is slow

bash
# This is normal - animations can take 30-60 seconds to generate
# For faster results, reduce mission duration or increase time_resolution
📝 License
This project was created for the FlytBase Robotics Assignment 2025.

👤 Author
Girija Wale
Date:31 December 2025

🙏 Acknowledgments
Built with AI assistance (Claude.ai, Grok, ChatGPT)
Assignment provided by FlytBase Robotics
Visualization powered by Matplotlib
Numerical computing with NumPy
