import { BlurView } from "expo-blur";
import React from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { COLORS } from "../../constants/theme";

export default function ReportsScreen() {
  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={{ paddingTop: 60, paddingBottom: 120 }}
    >
      <Text style={styles.title}>ACTIVE PINGS</Text>

      {/* Example Report Card */}
      <View style={styles.cardWrapper}>
        <BlurView intensity={30} tint="dark" style={styles.card}>
          <View style={styles.indicator} />
          <View>
            <Text style={styles.reportType}>STALKER SPOTTED</Text>
            <Text style={styles.reportLoc}>Downtown Blacksburg • 5m ago</Text>
          </View>
        </BlurView>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    paddingHorizontal: 20,
  },
  title: { color: "#fff", fontSize: 28, fontWeight: "900", marginBottom: 25 },
  cardWrapper: {
    borderRadius: 16,
    borderWidth: 1,
    borderColor: COLORS.secondary,
    overflow: "hidden",
    marginBottom: 15,
  },
  card: { padding: 20, flexDirection: "row", alignItems: "center" },
  indicator: {
    width: 4,
    height: 30,
    backgroundColor: COLORS.secondary,
    borderRadius: 2,
    marginRight: 15,
  },
  reportType: {
    color: COLORS.secondary,
    fontWeight: "900",
    fontSize: 14,
    letterSpacing: 1,
  },
  reportLoc: { color: "#fff", fontSize: 15, marginTop: 2 },
});
