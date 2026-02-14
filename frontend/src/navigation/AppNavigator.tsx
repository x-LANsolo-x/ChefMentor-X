import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

// Screens
import SplashScreen from '../screens/SplashScreen';
import LoginScreen from '../screens/LoginScreen';
import CookScreen from '../screens/CookScreen';
import RecipeDetailScreen from '../screens/RecipeDetailScreen';
import LiveCookingScreen from '../screens/LiveCookingScreen';
import AnalyzeScreen from '../screens/AnalyzeScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

<<<<<<< HEAD
const RootStack = createStackNavigator<RootStackParamList>();
const CookStack = createStackNavigator<CookStackParamList>();
const AnalyzeStack = createStackNavigator<AnalyzeStackParamList>();
const MainTab = createBottomTabNavigator<MainTabParamList>();

// ─── Cook Tab Stack ────────────────────────────────

function CookTabNavigator() {
    return (
        <CookStack.Navigator
            screenOptions={{
                headerShown: false,
                cardStyle: { backgroundColor: Colors.neutral[50] },
            }}
        >
            <CookStack.Screen name="RecipeList" component={RecipeListScreen} />
            <CookStack.Screen name="RecipeDetails" component={RecipeDetailsScreen} />
            <CookStack.Screen name="LiveCooking" component={LiveCookingScreen} />
            <CookStack.Screen name="Completion" component={CompletionScreen} />
        </CookStack.Navigator>
    );
}

// ─── Analyze Tab Stack ─────────────────────────────

function AnalyzeTabNavigator() {
    return (
        <AnalyzeStack.Navigator
            screenOptions={{
                headerShown: false,
                cardStyle: { backgroundColor: Colors.neutral[50] },
            }}
        >
            <AnalyzeStack.Screen name="UploadAnalysis" component={UploadAnalysisScreen} />
            <AnalyzeStack.Screen name="AnalysisLoading" component={AnalysisLoadingScreen} />
            <AnalyzeStack.Screen name="DiagnosisResult" component={DiagnosisResultScreen} />
        </AnalyzeStack.Navigator>
    );
}

// ─── Tab Icon Component ────────────────────────────

function TabIcon({ emoji, focused }: { emoji: string; focused: boolean }) {
    return (
        <View style={[styles.tabIcon, focused && styles.tabIconActive]}>
            <Text style={styles.tabEmoji}>{emoji}</Text>
        </View>
    );
}

// ─── Main Tab Navigator ────────────────────────────

function MainTabNavigator() {
    return (
        <MainTab.Navigator
            screenOptions={{
                headerShown: false,
                tabBarStyle: styles.tabBar,
                tabBarActiveTintColor: Colors.brand.orange,
                tabBarInactiveTintColor: Colors.neutral[400],
                tabBarLabelStyle: styles.tabLabel,
            }}
        >
            <MainTab.Screen
                name="CookTab"
                component={CookTabNavigator}
                options={{
                    tabBarLabel: 'Cook a Dish',
                    tabBarIcon: ({ focused }) => <TabIcon emoji="🍳" focused={focused} />,
                }}
            />
            <MainTab.Screen
                name="AnalyzeTab"
                component={AnalyzeTabNavigator}
                options={{
                    tabBarLabel: 'Analyze Dish',
                    tabBarIcon: ({ focused }) => <TabIcon emoji="🔍" focused={focused} />,
                }}
            />
        </MainTab.Navigator>
    );
}

// ─── Root Navigator ────────────────────────────────

export function AppNavigator() {
    return (
        <NavigationContainer>
            <RootStack.Navigator
                screenOptions={{
                    headerShown: false,
                    cardStyle: { backgroundColor: Colors.neutral[50] },
                }}
            >
                <RootStack.Screen name="Splash" component={SplashScreen} />
                <RootStack.Screen name="Login" component={LoginScreen} />
                <RootStack.Screen name="Onboarding" component={OnboardingScreen} />
                <RootStack.Screen name="MainTabs" component={MainTabNavigator} />
            </RootStack.Navigator>
        </NavigationContainer>
    );
}

// ─── Styles ────────────────────────────────────────

const styles = StyleSheet.create({
    tabBar: {
        backgroundColor: Colors.white,
        borderTopWidth: 1,
        borderTopColor: Colors.neutral[200],
        height: 80,
        paddingBottom: 16,
        paddingTop: 8,
        elevation: 8,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: -4 },
        shadowOpacity: 0.05,
        shadowRadius: 8,
    },
    tabLabel: {
        fontSize: Typography.fontSize.xs,
        fontWeight: Typography.fontWeight.semibold,
    },
    tabIcon: {
        width: TouchTarget.min,
        height: 32,
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: 16,
    },
    tabIconActive: {
        backgroundColor: Colors.brand.peach,
    },
    tabEmoji: {
        fontSize: 22,
    },
});
=======
function MainTabs() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }}>
      <Tab.Screen name="Cook" component={CookScreen} />
      <Tab.Screen name="Analyze" component={AnalyzeScreen} />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Splash" screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Splash" component={SplashScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="MainTabs" component={MainTabs} />
        <Stack.Screen name="RecipeDetail" component={RecipeDetailScreen} options={{ headerShown: true, title: 'Recipe' }} />
        <Stack.Screen name="LiveCooking" component={LiveCookingScreen} options={{ headerShown: true, title: 'Live Mode' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
>>>>>>> 965074bba05a4c69f6ad65a0d06051e580cc66b8
