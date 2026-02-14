import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function RecipeDetailScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Recipe Detail</Text>
      <Button title="Start Cooking" onPress={() => navigation.navigate('LiveCooking')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, marginBottom: 20 }
});
