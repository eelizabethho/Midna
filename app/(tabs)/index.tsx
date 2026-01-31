import { BlurView } from "expo-blur";
import React from "react";
import { StyleSheet, Text, View } from "react-native";
import MapView from '../../components/map/mapView';
import { COLORS, SHADOWS } from "../../constants/theme";

// Cyberpunk Map JSON (Works in Expo Go!)
const MAP_STYLE = [
  { elementType: "geometry", stylers: [{ color: "#050505" }] },
  { featureType: "road", stylers: [{ color: "#1A1A1A" }] },
  { featureType: "road.highway", stylers: [{ color: "#222222" }] },
  { featureType: "water", stylers: [{ color: "#001122" }] },
  { featureType: "poi", stylers: [{ visibility: "off" }] },
];

export default function CommandCenter() {
  return (
    <View style={styles.container}>
      {/* The Standard Map (Expo Go Compatible) */}
      <MapView
        style={StyleSheet.absoluteFill}
        customMapStyle={MAP_STYLE}
        initialRegion={{
          latitude: 37.2296, // Blacksburg
          longitude: -80.4139,
          latitudeDelta: 0.02,
          longitudeDelta: 0.02,
        }}
      />

      {/* Your Front-End UI Layer */}
      <View style={styles.hudContainer}>
        <BlurView
          intensity={90}
          tint="dark"
          style={[styles.hud, SHADOWS.neonGlow]}
        >
          <Text style={styles.hudLabel}>LOCAL SAFETY SCORE</Text>
          <View style={styles.scoreRow}>
            <Text style={styles.scoreValue}>88</Text>
            <Text style={styles.scoreTotal}>/100</Text>
            <View style={styles.badge}>
              <Text style={styles.badgeText}>SECURE</Text>
            </View>
          </View>
        </BlurView>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  hudContainer: { position: "absolute", top: 60, left: 20, right: 20 },
  hud: {
    padding: 20,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: COLORS.glassBorder,
    overflow: "hidden",
  },
  hudLabel: {
    color: COLORS.primary,
    fontSize: 11,
    fontWeight: "900",
    letterSpacing: 1.5,
  },
  scoreRow: { flexDirection: "row", alignItems: "baseline", marginTop: 5 },
  scoreValue: { color: "#fff", fontSize: 44, fontWeight: "900" },
  scoreTotal: { color: COLORS.textMuted, fontSize: 18, marginLeft: 4 },
  badge: {
    marginLeft: "auto",
    backgroundColor: "rgba(0, 255, 159, 0.15)",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  badgeText: { color: COLORS.primary, fontWeight: "900", fontSize: 10 },
});
