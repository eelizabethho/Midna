// constants/Theme.ts

export const COLORS = {
  // Base Colors
  background: "#050505",
  surface: "#1A1A1A", // For cards/containers
  text: "#FFFFFF",
  textMuted: "#666666",

  // Cyber Accents
  primary: "#00FF9F", // Neo-Mint (Safe / Brand)
  secondary: "#FF0055", // Electric Pink (Danger / Alert)
  warning: "#FFFF00", // Cyber Yellow (Caution)
  info: "#00D4FF", // Tech Blue (Intelligence)

  // Glass Effects
  glassBorder: "rgba(255, 255, 255, 0.15)",
  glassBackground: "rgba(255, 255, 255, 0.05)",
};

export const SHADOWS = {
  neonGlow: {
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 5, // For Android
  },
  dangerGlow: {
    shadowColor: COLORS.secondary,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.7,
    shadowRadius: 15,
    elevation: 8,
  },
};
