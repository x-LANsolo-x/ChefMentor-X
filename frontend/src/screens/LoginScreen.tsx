import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function LoginScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      <Button title="Login with Google" onPress={() => navigation.replace('MainTabs')} />
      <Button title="Try Demo Mode" onPress={() => navigation.replace('MainTabs')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 24, marginBottom: 20 }
});
