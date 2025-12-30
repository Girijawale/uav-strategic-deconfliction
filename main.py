from deconfliction_system import DeconflictionSystem
from visualizer import Visualizer
from scenarios import (
    create_conflict_scenario,
    create_clear_scenario,
    create_near_miss_scenario
)


def print_header():
   
    print("\n" + "=" * 70)
    print("4D DRONE DECONFLICTION SYSTEM")
    print("Strategic Airspace Management - 3D Space + Time Analysis")
    print("=" * 70)
    print("\nThis system performs spatiotemporal conflict detection to ensure")
    print("safe drone operations in shared airspace.")
    print("\n" + "=" * 70 + "\n")


def run_scenario(name, primary, simulated, system, visualizer, scenario_num):
    
    print(f"\n{'=' * 70}")
    print(f"SCENARIO {scenario_num}: {name}")
    print(f"{'=' * 70}\n")

    # Run core 4D deconfliction analysis
    result = system.check_mission(primary, simulated)

    # Output textual safety assessment
    system.print_report(result)

    print(f"\nGenerating visualizations for {name}...")

    # Normalize scenario name for file-safe output naming
    scenario_prefix = name.lower().replace(' ', '_')

    # Static 3D spatial plot (snapshot of trajectories)
    plot_path = f'output/{scenario_prefix}_3d.png'
    visualizer.plot_3d_static(primary, simulated, result, save_path=plot_path)

    # Animated visualization (time-evolving 4D behavior)
    anim_path = f'output/{scenario_prefix}_animation.gif'
    print(f"Creating animation (this may take a moment)...")
    visualizer.create_animation(primary, simulated, result, save_path=anim_path)

    print(f"\n✓ Scenario {scenario_num} complete!")
    print(f"  - 3D Plot: {plot_path}")
    print(f"  - Animation: {anim_path}")


def main():
    
    print_header()

    # Core system configuration
    system = DeconflictionSystem(
        safety_buffer=50.0,      # meters
        time_resolution=1.0      # seconds
    )

    # Visualization layer (consumes analysis output only)
    visualizer = Visualizer(system)

    print(f"System Configuration:")
    print(f"  • Safety Buffer: {system.safety_buffer}m")
    print(f"  • Time Resolution: {system.time_resolution}s")
    print(f"  • Analysis Mode: 4D (3D Space + Time)")

    # ------------------------------------------------------------------
    # Scenario 1: Guaranteed conflict case
    # Validates detection of spatial-temporal safety violations
    # ------------------------------------------------------------------
    primary1, simulated1 = create_conflict_scenario()
    run_scenario(
        "CONFLICT DETECTION",
        primary1,
        simulated1,
        system,
        visualizer,
        scenario_num=1
    )

    # ------------------------------------------------------------------
    # Scenario 2: Fully safe mission
    # Validates absence of false positives
    # ------------------------------------------------------------------
    primary2, simulated2 = create_clear_scenario()
    run_scenario(
        "CLEAR MISSION",
        primary2,
        simulated2,
        system,
        visualizer,
        scenario_num=2
    )

    # ------------------------------------------------------------------
    # Scenario 3: Near-miss case
    # Validates threshold-based safety buffer enforcement
    # ------------------------------------------------------------------
    primary3, simulated3 = create_near_miss_scenario()
    run_scenario(
        "NEAR MISS",
        primary3,
        simulated3,
        system,
        visualizer,
        scenario_num=3
    )

    # Final execution summary
    print("\n" + "=" * 70)
    print("ALL SCENARIOS COMPLETE")
    print("=" * 70)
    print("\nGenerated Files (in output/ folder):")
    print("  • conflict_detection_3d.png")
    print("  • conflict_detection_animation.gif")
    print("  • clear_mission_3d.png")
    print("  • clear_mission_animation.gif")
    print("  • near_miss_3d.png")
    print("  • near_miss_animation.gif")
    print("\n")


# Standard Python entry-point guard
# Enables safe importing without triggering execution
if __name__ == "__main__":
    main()
