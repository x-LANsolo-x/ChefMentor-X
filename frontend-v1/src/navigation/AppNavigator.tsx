/**
 * ChefMentor X – Navigation Configuration
 *
 * Structure:
 *   RootStack
 *   ├── Splash (public)
 *   ├── Login (public)
 *   ├── Onboarding (public)
 *   └── MainTabs (authenticated / demo)
 *       ├── CookTab (stack)
 *       │   ├── RecipeList
 *       │   ├── RecipeDetails
 *       │   ├── LiveCooking
 *       │   └── Completion
 *       ├── AnalyzeTab (stack)
 *       │   ├── UploadAnalysis
 *       │   ├── AnalysisLoading
 *       │   └── DiagnosisResult
 *       ├── HistoryTab → CookingHistory
 *       └── ProfileTab (stack)
 *           ├── Profile
 *           ├── CookingHistory (push)
 *           └── Settings (push)
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text, View, StyleSheet } from 'react-native';
import { Colors, Typography, TouchTarget } from '../constants/theme';
import type {
    RootStackParamList,
    MainTabParamList,
    CookStackParamList,
    AnalyzeStackParamList,
    ProfileStackParamList,
} from '../types';

import {
    SplashScreen,
    LoginScreen,
    OnboardingScreen,
    PermissionsScreen,
    SkillLevelScreen,
    RecipeListScreen,
    RecipeDetailsScreen,
    LiveCookingScreen,
    LiveCameraScreen,
    CompletionScreen,
    UploadAnalysisScreen,
    ContextQuestionsScreen,
    AnalysisLoadingScreen,
    DiagnosisResultScreen,
    ProfileScreen,
    CookingHistoryScreen,
    SettingsScreen,
} from '../screens';

// ─── Stack Navigators ───────────────────────────────

const RootStack = createNativeStackNavigator<RootStackParamList>();
const CookStack = createNativeStackNavigator<CookStackParamList>();
const AnalyzeStack = createNativeStackNavigator<AnalyzeStackParamList>();
const ProfileStack = createNativeStackNavigator<ProfileStackParamList>();
const MainTab = createBottomTabNavigator<MainTabParamList>();

// ─── Cook Tab Stack ─────────────────────────────────

function CookTabNavigator() {
    return (
        <CookStack.Navigator
            screenOptions={{
                headerShown: false,
                animation: 'fade',
                contentStyle: { backgroundColor: Colors.neutral[50] },
            }}
        >
            <CookStack.Screen name="RecipeList" component={RecipeListScreen} />
            <CookStack.Screen name="RecipeDetails" component={RecipeDetailsScreen} />
            <CookStack.Screen name="LiveCooking" component={LiveCookingScreen} />
            <CookStack.Screen name="LiveCamera" component={LiveCameraScreen} options={{ headerShown: false }} />
            <CookStack.Screen name="Completion" component={CompletionScreen} />
        </CookStack.Navigator>
    );
}

// ─── Analyze Tab Stack ──────────────────────────────

function AnalyzeTabNavigator() {
    return (
        <AnalyzeStack.Navigator
            screenOptions={{
                headerShown: false,
                animation: 'fade',
                contentStyle: { backgroundColor: Colors.neutral[50] },
            }}
        >
            <AnalyzeStack.Screen name="UploadAnalysis" component={UploadAnalysisScreen} />
            <AnalyzeStack.Screen name="ContextQuestions" component={ContextQuestionsScreen} />
            <AnalyzeStack.Screen name="AnalysisLoading" component={AnalysisLoadingScreen} />
            <AnalyzeStack.Screen name="DiagnosisResult" component={DiagnosisResultScreen} />
        </AnalyzeStack.Navigator>
    );
}

// ─── Profile Tab Stack ──────────────────────────────

function ProfileTabNavigator() {
    return (
        <ProfileStack.Navigator
            screenOptions={{
                headerShown: false,
                animation: 'fade',
                contentStyle: { backgroundColor: Colors.neutral[50] },
            }}
        >
            <ProfileStack.Screen name="Profile" component={ProfileScreen} />
            <ProfileStack.Screen name="CookingHistory" component={CookingHistoryScreen} />
            <ProfileStack.Screen name="Settings" component={SettingsScreen} />
        </ProfileStack.Navigator>
    );
}

// ─── Tab Icon Component ─────────────────────────────

function TabIcon({ emoji, focused }: { emoji: string; focused: boolean }) {
    return (
        <View style={[styles.tabIcon, focused && styles.tabIconActive]}>
            <Text style={styles.tabEmoji}>{emoji}</Text>
        </View>
    );
}

// ─── Main Tab Navigator (4 tabs) ────────────────────

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
                    tabBarLabel: 'Cook',
                    tabBarIcon: ({ focused }) => <TabIcon emoji="🍳" focused={focused} />,
                }}
            />
            <MainTab.Screen
                name="AnalyzeTab"
                component={AnalyzeTabNavigator}
                options={{
                    tabBarLabel: 'Analyze',
                    tabBarIcon: ({ focused }) => <TabIcon emoji="🔬" focused={focused} />,
                }}
            />
            <MainTab.Screen
                name="HistoryTab"
                component={CookingHistoryScreen}
                options={{
                    tabBarLabel: 'History',
                    tabBarIcon: ({ focused }) => <TabIcon emoji="📋" focused={focused} />,
                }}
            />
            <MainTab.Screen
                name="ProfileTab"
                component={ProfileTabNavigator}
                options={{
                    tabBarLabel: 'Profile',
                    tabBarIcon: ({ focused }) => <TabIcon emoji="👤" focused={focused} />,
                }}
            />
        </MainTab.Navigator>
    );
}

// ─── Root Navigator ─────────────────────────────────

export function AppNavigator() {
    return (
        <NavigationContainer>
            <RootStack.Navigator
                screenOptions={{
                    headerShown: false,
                    animation: 'fade',
                    contentStyle: { backgroundColor: Colors.neutral[50] },
                }}
            >
                <RootStack.Screen name="Splash" component={SplashScreen} />
                <RootStack.Screen name="Login" component={LoginScreen} />
                <RootStack.Screen name="Onboarding" component={OnboardingScreen} />
                <RootStack.Screen name="Permissions" component={PermissionsScreen} />
                <RootStack.Screen name="SkillLevel" component={SkillLevelScreen} />
                <RootStack.Screen name="MainTabs" component={MainTabNavigator} />
            </RootStack.Navigator>
        </NavigationContainer>
    );
}

// ─── Styles ─────────────────────────────────────────

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
