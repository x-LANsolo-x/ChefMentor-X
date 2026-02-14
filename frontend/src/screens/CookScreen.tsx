import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function CookScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>What do you want to cook?</Text>
      <Button title="Maggi Noodles" onPress={() => navigation.navigate('RecipeDetail', { id: '1' })} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 20, marginBottom: 20 }
});
