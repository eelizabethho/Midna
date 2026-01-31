import React from 'react';
import { StyleSheet, View } from 'react-native';
import Mapbox from '@rnmapbox/maps';

// Replace with your PUBLIC token (starts with pk.)
Mapbox.setAccessToken('pk.eyJ1Ijoic3VkZWVrc2hhcHIiLCJhIjoiY21sMnJpaWU0MGxsYTNsb3E2cjQxZzVuayJ9.K6ZWQurgpI-o9RxyBwwy6w');

const Mapview = () => {
  return (
    <View style={styles.container}>
      <Mapbox.MapView 
        style={styles.map} 
        styleURL={Mapbox.StyleURL.Street}
      >
        <Mapbox.Camera 
          zoomLevel={12} 
          centerCoordinate={[-74.006, 40.7128]} // [Longitude, Latitude]
        />
      </Mapbox.MapView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { flex: 1 },
});

export default Mapview;