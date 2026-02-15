/**
 * ChefMentor X – Settings Screen
 *
 * Stitch ref: chefmentor_x_settings
 * Features:
 *  - User card (avatar + name + Edit)
 *  - PREFERENCES section (Voice Guidance Speed, Beginner Mode toggle, Wake Word toggle)
 *  - NOTIFICATIONS section (Push Notifications toggle, Weekly Meal Plan toggle)
 *  - GENERAL section (Privacy & Security, Help & Support)
 *  - DANGER ZONE (Delete Account in red)
 *  - Version footer
 */

import React, { useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    Switch,
    Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors, Typography, Spacing, BorderRadius, Shadows } from '../constants/theme';
import { useAuthStore } from '../stores/authStore';
import { useSettingsStore } from '../stores/settingsStore';
import { observer } from 'mobx-react-lite';
import { voiceService } from '../services/voiceService';

const SettingsScreen = observer(({ navigation }: any) => {
    const { user, logout } = useAuthStore();
    const settings = useSettingsStore();

    // Sync voice speed with voice service
    useEffect(() => {
        const speedMap = { Slow: 0.8, Normal: 1.0, Fast: 1.3 };
        voiceService.setRate(speedMap[settings.voiceSpeed]);
    }, [settings.voiceSpeed]);

    const handleEditProfile = () => {
        Alert.alert('Edit Profile', 'Profile editing coming soon!');
    };

    const handlePrivacy = () => {
        Alert.alert('Privacy & Security', 'Your data is encrypted and secure.');
    };

    const handleHelp = () => {
        Alert.alert('Help & Support', 'Contact us at support@chefmentorx.com');
    };

    const handleDeleteAccount = () => {
        Alert.alert(
            'Delete Account',
            'Are you sure? This action cannot be undone.',
            [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'Delete',
                    style: 'destructive',
                    onPress: async () => {
                        await logout();
                        navigation.reset({ index: 0, routes: [{ name: 'Splash' }] });
                    },
                },
            ]
        );
    };

    return (
        <SafeAreaView style={styles.container} edges={['top']}>
            {/* Header */}
            <View style={styles.header}>
                <TouchableOpacity
                    style={styles.backBtn}
                    onPress={() => navigation.goBack()}
                >
                    <Text style={styles.backIcon}>←</Text>
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Settings</Text>
                <View style={{ width: 40 }} />
            </View>

            <ScrollView
                showsVerticalScrollIndicator={false}
                contentContainerStyle={styles.scroll}
            >
                {/* User card */}
                <View style={styles.userCard}>
                    <View style={styles.ucAvatar}>
                        <Text style={{ fontSize: 28 }}>👨‍🍳</Text>
                    </View>
                    <View style={styles.ucInfo}>
                        <Text style={styles.ucName}>{user?.name || 'Chef'}</Text>
                        <Text style={styles.ucEmail}>{user?.email || 'guest@chefmentorx.app'}</Text>
                    </View>
                    <TouchableOpacity onPress={handleEditProfile}>
                        <Text style={styles.editLink}>Edit</Text>
                    </TouchableOpacity>
                </View>

                {/* ── PREFERENCES ── */}
                <Text style={styles.sectionLabel}>PREFERENCES</Text>
                <View style={styles.card}>
                    {/* Voice Guidance Speed */}
                    <View style={styles.row}>
                        <View style={styles.rowLeft}>
                            <Text style={styles.rowIcon}>🗣</Text>
                            <View>
                                <Text style={styles.rowTitle}>Voice Guidance Speed</Text>
                                <Text style={styles.rowSub}>Adjust how fast the voice speaks</Text>
                            </View>
                        </View>
                    </View>
                    <View style={styles.speedRow}>
                        {(['Slow', 'Normal', 'Fast'] as const).map((speed) => (
                            <TouchableOpacity
                                key={speed}
                                style={[
                                    styles.speedPill,
                                    settings.voiceSpeed === speed && styles.speedPillActive,
                                ]}
                                onPress={() => settings.setVoiceSpeed(speed)}
                            >
                                <Text
                                    style={[
                                        styles.speedLabel,
                                        settings.voiceSpeed === speed && styles.speedLabelActive,
                                    ]}
                                >
                                    {speed}
                                </Text>
                            </TouchableOpacity>
                        ))}
                    </View>

                    <View style={styles.divider} />

                    {/* Beginner Mode */}
                    <View style={styles.row}>
                        <View style={styles.rowLeft}>
                            <Text style={styles.rowIcon}>🌱</Text>
                            <View>
                                <Text style={styles.rowTitle}>Beginner Mode</Text>
                                <Text style={styles.rowSub}>Show extra guidance and tips</Text>
                            </View>
                        </View>
                        <Switch
                            value={settings.beginnerMode}
                            onValueChange={settings.setBeginnerMode}
                            trackColor={{ false: Colors.neutral[200], true: Colors.brand.orange }}
                            thumbColor={Colors.white}
                        />
                    </View>

                    <View style={styles.divider} />

                    {/* Wake Word */}
                    <View style={styles.row}>
                        <View style={styles.rowLeft}>
                            <Text style={styles.rowIcon}>🎙️</Text>
                            <View>
                                <Text style={styles.rowTitle}>Wake Word</Text>
                                <Text style={styles.rowSub}>Say "Hey Chef" to activate</Text>
                            </View>
                        </View>
                        <Switch
                            value={settings.wakeWordEnabled}
                            onValueChange={settings.setWakeWordEnabled}
                            trackColor={{ false: Colors.neutral[200], true: Colors.brand.orange }}
                            thumbColor={Colors.white}
                        />
                    </View>
                </View>

                {/* ── NOTIFICATIONS ── */}
                <Text style={styles.sectionLabel}>NOTIFICATIONS</Text>
                <View style={styles.card}>
                    <View style={styles.row}>
                        <View style={styles.rowLeft}>
                            <Text style={styles.rowIcon}>🔔</Text>
                            <View>
                                <Text style={styles.rowTitle}>Push Notifications</Text>
                                <Text style={styles.rowSub}>Get cooking reminders</Text>
                            </View>
                        </View>
                        <Switch
                            value={settings.pushNotifications}
                            onValueChange={settings.setPushNotifications}
                            trackColor={{ false: Colors.neutral[200], true: Colors.brand.orange }}
                            thumbColor={Colors.white}
                        />
                    </View>

                    <View style={styles.divider} />

                    <View style={styles.row}>
                        <View style={styles.rowLeft}>
                            <Text style={styles.rowIcon}>📅</Text>
                            <View>
                                <Text style={styles.rowTitle}>Weekly Meal Plan</Text>
                                <Text style={styles.rowSub}>Receive weekly recipe suggestions</Text>
                            </View>
                        </View>
                        <Switch
                            value={settings.weeklyMealPlan}
                            onValueChange={settings.setWeeklyMealPlan}
                            trackColor={{ false: Colors.neutral[200], true: Colors.brand.orange }}
                            thumbColor={Colors.white}
                        />
                    </View>
                </View>

                {/* ── GENERAL ── */}
                <Text style={styles.sectionLabel}>GENERAL</Text>
                <View style={styles.card}>
                    <TouchableOpacity style={styles.row} onPress={handlePrivacySecurity}>
                        <View style={styles.rowLeft}>
                            <Text style={styles.rowIcon}>🔒</Text>
                            <Text style={styles.rowTitle}>Privacy & Security</Text>
                        </View>
                        <Text style={styles.rowArrow}>›</Text>
                    </TouchableOpacity>

                    <View style={styles.divider} />

                    <TouchableOpacity style={styles.row} onPress={handleHelpSupport}>
                        <View style={styles.rowLeft}>
                            <Text style={styles.rowIcon}>❓</Text>
                            <Text style={styles.rowTitle}>Help & Support</Text>
                        </View>
                        <Text style={styles.rowArrow}>›</Text>
                    </TouchableOpacity>
                </View>

                {/* ── DANGER ZONE ── */}
                <Text style={[styles.sectionLabel, { color: Colors.error }]}>DANGER ZONE</Text>
                <View style={[styles.card, styles.dangerCard]}>
                    <TouchableOpacity style={styles.row} onPress={handleDeleteAccount}>
                        <View style={styles.rowLeft}>
                            <Text style={styles.rowIcon}>🗑️</Text>
                            <View>
                                <Text style={[styles.rowTitle, { color: Colors.error }]}>
                                    Delete Account
                                </Text>
                                <Text style={styles.rowSub}>
                                    Permanently remove your account and data
                                </Text>
                            </View>
                        </View>
                        <Text style={[styles.rowArrow, { color: Colors.error }]}>›</Text>
                    </TouchableOpacity>
                </View>

                {/* Version */}
                <Text style={styles.version}>ChefMentor X v1.0.0</Text>
            </ScrollView>
        </SafeAreaView>
    );
});

export default SettingsScreen;

/* ─── Styles ─────────────────────────────────────────── */
const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: Colors.neutral[50] },

    /* Header */
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: Spacing[6],
        paddingVertical: Spacing[3],
    },
    backBtn: {
        width: 40,
        height: 40,
        borderRadius: 20,
        borderWidth: 1,
        borderColor: Colors.neutral[200],
        alignItems: 'center',
        justifyContent: 'center',
    },
    backIcon: { fontSize: 18, color: Colors.textMain },
    headerTitle: {
        fontFamily: 'DMSans-Bold',
        fontSize: Typography.fontSize.xl,
        fontWeight: '700',
        color: Colors.textMain,
    },

    scroll: { paddingHorizontal: Spacing[6], paddingBottom: 60 },

    /* User card */
    userCard: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Colors.white,
        padding: Spacing[4],
        borderRadius: BorderRadius.xl,
        ...Shadows.sm,
        borderWidth: 1,
        borderColor: Colors.neutral[100],
        marginBottom: Spacing[6],
        marginTop: Spacing[2],
    },
    ucAvatar: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: Colors.brand.peach,
        alignItems: 'center',
        justifyContent: 'center',
        marginRight: 12,
    },
    ucInfo: { flex: 1 },
    ucName: {
        fontFamily: 'DMSans-Bold',
        fontSize: Typography.fontSize.base,
        fontWeight: '700',
        color: Colors.textMain,
    },
    ucEmail: {
        fontFamily: 'DMSans',
        fontSize: Typography.fontSize.xs,
        color: Colors.textSub,
    },
    editLink: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: Typography.fontSize.sm,
        fontWeight: '600',
        color: Colors.brand.orange,
    },

    /* Section label */
    sectionLabel: {
        fontFamily: 'DMSans-Bold',
        fontSize: Typography.fontSize.xs,
        fontWeight: '700',
        color: Colors.textSub,
        letterSpacing: 1.5,
        marginBottom: 10,
    },

    /* Card */
    card: {
        backgroundColor: Colors.white,
        borderRadius: BorderRadius.xl,
        padding: Spacing[4],
        ...Shadows.sm,
        borderWidth: 1,
        borderColor: Colors.neutral[100],
        marginBottom: Spacing[5],
    },
    dangerCard: {
        borderColor: 'rgba(220,38,38,0.2)',
        backgroundColor: 'rgba(254,226,226,0.3)',
    },

    /* Row */
    row: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingVertical: 10,
    },
    rowLeft: { flexDirection: 'row', alignItems: 'center', flex: 1, gap: 12 },
    rowIcon: { fontSize: 18 },
    rowTitle: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: Typography.fontSize.base,
        fontWeight: '600',
        color: Colors.textMain,
    },
    rowSub: {
        fontFamily: 'DMSans',
        fontSize: Typography.fontSize.xs,
        color: Colors.textSub,
        marginTop: 2,
    },
    rowArrow: {
        fontSize: 22,
        color: Colors.neutral[400],
    },

    divider: {
        height: 1,
        backgroundColor: Colors.neutral[100],
        marginVertical: 4,
    },

    /* Speed pills */
    speedRow: {
        flexDirection: 'row',
        gap: 8,
        paddingBottom: 8,
        paddingLeft: 42,
    },
    speedPill: {
        paddingHorizontal: 16,
        paddingVertical: 6,
        borderRadius: BorderRadius.full,
        backgroundColor: Colors.neutral[100],
    },
    speedPillActive: {
        backgroundColor: Colors.brand.orange,
    },
    speedLabel: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: Typography.fontSize.xs,
        fontWeight: '600',
        color: Colors.textSub,
    },
    speedLabelActive: {
        color: Colors.white,
    },

    /* Version */
    version: {
        fontFamily: 'DMSans',
        fontSize: Typography.fontSize.xs,
        color: Colors.neutral[400],
        textAlign: 'center',
        marginTop: Spacing[4],
        marginBottom: Spacing[4],
    },
});
