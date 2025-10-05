import folium
import math
import webbrowser

def main():
    print("=== Asteroid Impact Simulation 🌍 ===")

    # ======== Entering coordinates ========
    try:
        lat = float(input("Enter latitude (-90 to 90, e.g. 50.45): ").strip())
        lon = float(input("Enter longitude (-180 to 180, e.g. 30.52): ").strip())
    except ValueError:
        print("❌ Error: please enter numeric coordinates.")
        return

    # Checking geographical boundaries
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        print("❌ Error: coordinates are outside Earth's range!")
        print("Latitude must be between -90 and 90, longitude between -180 and 180.")
        return

    # ======== Input asteroid parameters ========і
    try:
        mass = float(input("Enter asteroid mass (kg, e.g. 1e9): ").strip())
        # Boundary for third cosmic velocity
        velocity = float(input("Enter asteroid velocity (m/s, between 11200 and 16700 m/s): ").strip())
        angle_deg = float(input("Enter angle of entry (degrees, 0-90): ").strip())
    except ValueError:
        print("❌ Error: mass, velocity, and angle must be numbers.")
        return

    # Physical bounds check
    if not (0 < mass <= 1e15):
        print("❌ Error: mass must be realistic (1 to 1e15 kg).")
        return
    if not (11200 <= velocity <= 16700):
        print("❌ Error: velocity must be between 11200 and 16,700 m/s.")
        return
    if not (0 <= angle_deg <= 90):
        print("❌ Error: angle must be between 0° and 90°.")
        return

    # ======== Energy calculation ========
    total_energy = 0.5 * mass * velocity**2
    angle_radians = math.radians(angle_deg)
    effective_energy = total_energy * math.sin(angle_radians)

    print(f"\nTotal kinetic energy: {total_energy:.2e} J")
    print(f"Impact angle: {angle_deg}°")
    print(f"Effective impact energy: {effective_energy:.2e} J")

    # ======== Asteroid classification ========
    if effective_energy < 1e15:
        category = "Small"
        consequences = "Local damage, minor atmospheric effects."
        scale_factor = 3
    elif effective_energy < 1e18:
        category = "Medium"
        consequences = "Severe destruction, strong shockwave."
        scale_factor = 8
    else:
        category = "Large"
        consequences = "Global effects, major climate impact."
        scale_factor = 20

    print(f"\nAsteroid category: {category}")
    print(f"Possible consequences: {consequences}")

    # ======== Damage radius estimation ========
    base_radius = (effective_energy ** (1/3.85)) * scale_factor / 1000  # km
    if base_radius > 4000:
        base_radius = 4000  # Earth's size limit

    print(f"Estimated base impact radius: {base_radius:.1f} km")

    # ======== Risk zones ========
    zones = [
        (base_radius * 0.3, 'red', 'High risk zone'),
        (base_radius * 0.6, 'orange', 'Medium risk zone'),
        (base_radius, 'yellow', 'Low risk zone')
    ]

    # ======== Create map ========
    zoom = 6 if base_radius < 200 else 4 if base_radius < 800 else 3
    m = folium.Map(location=[lat, lon], zoom_start=zoom)

    # Impact point marker
    folium.Marker(
        location=[lat, lon],
        popup=(f"Asteroid Impact\n"
               f"Mass: {mass:.2e} kg\n"
               f"Velocity: {velocity:.2e} m/s\n"
               f"Angle: {angle_deg}°\n"
               f"Effective Energy: {effective_energy:.2e} J\n"
               f"Category: {category}\n"
               f"Consequences: {consequences}"),
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

    # Colored zones
    for radius_km, color, label in zones:
        folium.Circle(
            location=[lat, lon],
            radius=radius_km * 1000,
            color=color,
            fill=True,
            fill_opacity=0.3,
            popup=f"{label} ({radius_km:.1f} km)"
        ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # ======== Save map and open ========
    output_file = "asteroid_impact_map.html"
    m.save(output_file)
    print(f"\n✅ Map saved as '{output_file}'. Open it in your browser!")

    # Automatically open the map in browser
    webbrowser.open(output_file)

# ======== Main run ========
if __name__ == "__main__":
    main()
