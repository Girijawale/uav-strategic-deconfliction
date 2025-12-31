# 🚁 UAV Deconfliction System

> **Strategic Airspace Management Through Spatiotemporal Analysis**

A  system that verifies drone mission safety in shared airspace using 4D conflict detection (3D space + time).

---

## 📖 Overview

This system acts as the **final authority** for verifying whether a drone's planned mission is safe to execute. Before takeoff, it checks:

- ✅ No spatial conflicts with other drones (within safety buffer)
- ✅ No temporal overlaps at the same location  
- ✅ Compliance with mission time windows

**How it works:** The system interpolates drone positions at each time step, calculates 3D distances between all aircraft, detects safety buffer violations, and generates detailed conflict reports with visualizations.

---

## ✨ Features

**Core Capabilities**
- 🎯 Full 4D conflict detection (3D space + time)
- 📏 Configurable safety buffer (default: 50m)
- ⏱️ Adjustable time resolution (default: 1s)
- 📊 Automatic conflict consolidation
- 📝 Detailed reports with location, time, and severity

**Visualization**
- 📈 Static 3D trajectory plots
- 🎬 Animated 4D simulations  
- 🔴 Highlighted conflict zones
- 💾 Export as PNG and GIF

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Girijawale/uav-strategic-deconfliction.git
cd uav-strategic-deconfliction

# Install dependencies
pip install -r requirements.txt

# Create output directory
mkdir output
```

### Run the System

```bash
python main.py
```

This will run 3 test scenarios and generate visualizations in the `output/` folder.

**Expected output:**
```
======================================================================
4D DRONE DECONFLICTION SYSTEM
Strategic Airspace Management - 3D Space + Time Analysis
======================================================================

System Configuration:
  • Safety Buffer: 50.0m
  • Time Resolution: 1.0s
  • Analysis Mode: 4D (3D Space + Time)

Running Scenario 1: CONFLICT DETECTION...
✓ Scenario 1 complete!
  - 3D Plot: output/conflict_detection_3d.png
  - Animation: output/conflict_detection_animation.gif
```

---

## 📂 Project Structure

```
uav-strategic-deconfliction/
│
├── main.py                     # Entry point - runs all scenarios
├── deconfliction_system.py     # Core 4D conflict detection engine
├── visualizer.py               # 3D plots and animations
├── models.py                   # Data models (Waypoint, Mission, Conflict)
├── scenarios.py                # Test scenarios
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── REFLECTION.md               # Design decisions & architecture analysis
│
└── output/                     # Generated visualizations
    ├── conflict_detection_3d.png
    ├── conflict_detection_animation.gif
    ├── clear_mission_3d.png
    ├── clear_mission_animation.gif
    ├── near_miss_3d.png
    └── near_miss_animation.gif
```

---

## 💻 Usage

### Basic Example

```python
from deconfliction_system import DeconflictionSystem
from models import Mission, Waypoint

# Initialize system
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

# Define other flights
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
```

### Creating Custom Scenarios

```python
# Define your mission
custom_mission = Mission(
    waypoints=[
        Waypoint(x=0, y=0, z=100),
        Waypoint(x=50, y=50, z=120),
        Waypoint(x=100, y=100, z=100)
    ],
    start_time=0,
    end_time=30,
    mission_id="DELIVERY_001"
)
```

### Generating Visualizations

```python
from visualizer import Visualizer

visualizer = Visualizer(system)

# Static 3D plot
visualizer.plot_3d_static(primary, simulated, result, 
                         save_path='output/my_scenario.png')

# Animated simulation
visualizer.create_animation(primary, simulated, result,
                           save_path='output/my_scenario.gif')
```

---

## 🧪 Test Scenarios

The system includes three predefined scenarios:

**1. Conflict Detection**
- Tests: Multiple drones with crossing paths
- Expected: Conflicts detected
- Output: `conflict_detection_*` files

**2. Clear Mission**  
- Tests: Well-separated missions (spatial & temporal)
- Expected: CLEAR status (no false positives)
- Output: `clear_mission_*` files

**3. Near Miss**
- Tests: Drones passing at ~60m (just outside 50m buffer)
- Expected: CLEAR status
- Output: `near_miss_*` files

---

## 📊 Sample Output

**Console Report:**
```
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
======================================================================
```

**Programmatic Access:**
```python
result = {
    'status': 'CONFLICT_DETECTED',
    'conflicts': [...],
    'summary': {
        'total_conflicts': 2,
        'affected_flights': 2,
        'minimum_distance': 15.23,
        'message': '✗ CONFLICT DETECTED - ...'
    }
}
```

---

## ⚙️ Configuration

### System Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `safety_buffer` | 50.0 | Minimum safe separation (meters) |
| `time_resolution` | 1.0 | Time step precision (seconds) |

**Example:**
```python
system = DeconflictionSystem(
    safety_buffer=75.0,      # More conservative
    time_resolution=0.5      # Higher precision
)
```

---

## 🏗️ Architecture

**Algorithm Flow:**
1. Loop through each time step in the mission
2. Interpolate primary drone's 3D position
3. For each other flight, interpolate their position
4. Calculate 3D Euclidean distance
5. If distance < safety buffer → record conflict
6. Consolidate consecutive conflicts into time windows
7. Generate detailed report

**Core Components:**

| Component | File | Purpose |
|-----------|------|---------|
| Deconfliction Engine | `deconfliction_system.py` | 4D interpolation & conflict detection |
| Data Models | `models.py` | Waypoint, Mission, Conflict classes |
| Test Scenarios | `scenarios.py` | Predefined test cases |
| Visualization | `visualizer.py` | 3D plots & 4D animations |

---

## 🔍 Edge Cases Handled

- ✅ Zero-length paths (stationary drones)
- ✅ Single waypoint missions
- ✅ Non-overlapping time windows
- ✅ Identical waypoint positions
- ✅ Zero mission duration
- ✅ Empty flight lists

---

## 🚀 Scalability

**Current System:**
- Complexity: O(T × N) where T = time steps, N = flights
- Single-threaded execution
- In-memory data storage

**For 10,000+ Drones, Need:**
- **Spatial indexing** (R-tree) for 100x faster lookups
- **Distributed computing** (Kubernetes cluster)
- **Real-time pipeline** (Kafka streaming)
- **Database layer** (InfluxDB + PostGIS + Redis)
- **ML models** for trajectory prediction

See [REFLECTION.md](REFLECTION.md) for detailed scalability analysis.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **README.md** | Setup and usage guide (this file) |
| **[REFLECTION.md](REFLECTION.md)** | Design decisions, architecture, AI integration, testing strategy, scalability analysis |

**REFLECTION.md covers:**
1. Design decisions and architectural choices
2. Spatial and temporal check implementation details
3. AI integration (Claude.ai, development workflow, validation)
4. Testing strategy and edge cases
5. Scalability requirements for production (10,000+ drones)

---

## 🐛 Troubleshooting

**ModuleNotFoundError:**
```bash
pip install numpy matplotlib
```

**Missing output directory:**
```bash
mkdir output
```

**Slow animation generation:**
- This is normal - animations take 30-60 seconds
- Reduce mission duration or increase `time_resolution` for faster generation

---

## 🎥 Demo Video

> **[https://www.loom.com/share/f28147fa36fa4d21a1f155907eacc09a]** > **Note:** There is a brief microphone issue at the beginning of the Loom video, so the audio is low for the first few seconds. Audio clarity improves shortly after.


The demo showcases:
- System architecture overview
- Live conflict detection
- 3D visualizations and 4D animations
- Design decisions and trade-offs

---

## 🤝 Built With

- 🐍 **Python 3.8+**
- 🔢 **NumPy** - Numerical computing
- 📊 **Matplotlib** - Visualization
- 🤖 **Claude AI, Grok, ChatGPT** - Development assistance

---

## 👤 Author

**Girija Wale**  
📧 girijawale432@gmail.com  
🔗 [GitHub](https://github.com/Girijawale)

*Assignment submitted: December 31, 2025*

---

## 🙏 Acknowledgments

- **FlytBase Robotics** for the challenging assignment
- **Claude AI, Grok, ChatGPT** for accelerating development
- **Open-source community** for NumPy and Matplotlib

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

*Made with ❤️ for safe autonomous flight operations*

**FlytBase Robotics Assignment 2025**

</div>
