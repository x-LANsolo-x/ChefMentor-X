import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function AnalyzeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Analyze Failed Dish</Text>
      <Button title="Take Photo" onPress={() => {}} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, marginBottom: 20 }
});
