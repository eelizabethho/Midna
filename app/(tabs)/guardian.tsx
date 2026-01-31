import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { COLORS, SHADOWS } from "../../constants/theme";

export default function GuardianScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>GUARDIAN</Text>

      <View style={styles.center}>
        <Pressable style={[styles.sosButton, SHADOWS.dangerGlow]}>
          <Text style={styles.sosText}>SOS</Text>
        </Pressable>
        <Text style={styles.hint}>HOLD 3 SECONDS TO PING</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    padding: 25,
    paddingTop: 60,
  },
  title: { color: "#fff", fontSize: 28, fontWeight: "900" },
  center: { flex: 1, alignItems: "center", justifyContent: "center" },
  sosButton: {
    width: 180,
    height: 180,
    borderRadius: 90,
    backgroundColor: COLORS.secondary,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 8,
    borderColor: "rgba(255, 255, 255, 0.2)",
  },
  sosText: { color: "#fff", fontSize: 40, fontWeight: "900" },
  hint: {
    color: COLORS.textMuted,
    marginTop: 20,
    fontWeight: "700",
    letterSpacing: 1,
  },
});
