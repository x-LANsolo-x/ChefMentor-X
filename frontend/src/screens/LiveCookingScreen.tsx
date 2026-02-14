import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function LiveCookingScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Live Mode</Text>
      <Text>Step 1: Boil Water</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#000' },
  title: { fontSize: 24, color: '#fff' }
});
