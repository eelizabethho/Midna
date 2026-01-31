import { Tabs } from 'expo-router';
import { BlurView } from 'expo-blur';
import { StyleSheet, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SHADOWS } from '../../constants/theme';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.textMuted,
        tabBarStyle: styles.tabBar,
        tabBarBackground: () => (
          <BlurView intensity={80} tint="dark" style={StyleSheet.absoluteFill} />
        ),
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'COMMAND',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons name="navigate" size={24} color={color} style={focused ? SHADOWS.neonGlow : null} />
          ),
        }}
      />
      <Tabs.Screen
        name="reports"
        options={{
          title: 'REPORTS',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons name="megaphone" size={24} color={color} style={focused ? SHADOWS.dangerGlow : null} />
          ),
        }}
      />
      <Tabs.Screen
        name="guardian"
        options={{
          title: 'GUARDIAN',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons name="shield-checkmark" size={24} color={color} style={focused ? SHADOWS.neonGlow : null} />
          ),
        }}
      />
    </Tabs>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    position: 'absolute',
    bottom: Platform.OS === 'ios' ? 30 : 20,
    left: 16,
    right: 16,
    height: 64,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: COLORS.glassBorder,
    backgroundColor: 'transparent',
    overflow: 'hidden',
  },
});