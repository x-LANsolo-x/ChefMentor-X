/**
 * ChefMentor X – Profile Screen
 *
 * Stitch ref: chefmentor_x_profile
 * Features:
 *  - Avatar with orange ring and green online dot
 *  - Name, email, "Pro Chef" badge
 *  - 3 stat circles (Recipes, Mastered, Success Rate)
 *  - Cooking Profile section (difficulty, dietary, avg time)
 *  - Quick Actions list
 *  - Sign Out button
 */

import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    Modal,
    Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors, Typography, Spacing, BorderRadius, Shadows } from '../constants/theme';
import { useAuthStore } from '../stores/authStore';
import { useProfileStore } from '../stores/profileStore';
import FadeIn from '../components/FadeIn';
import { TextInput, Button } from '../components';

const STATS = [
    { value: '24', label: 'Recipes\nAttempted', color: Colors.brand.peach },
    { value: '18', label: 'Recipes\nMastered', color: '#E9F0E8' },
    { value: '75%', label: 'Success\nRate', color: '#DBEAFE' },
];

const PROFILE_ITEMS = [
    { label: 'Difficulty Level', value: 'Intermediate', icon: '🔥' },
    { label: 'Dietary Preference', value: 'No Restrictions', icon: '🥗' },
    { label: 'Avg Cooking Time', value: '22 minutes', icon: '⏱' },
];

const QUICK_ACTIONS = [
    { label: 'Cooking History', icon: '📋', screen: 'CookingHistory' },
    { label: 'Share Progress', icon: '↗️', screen: null },
    { label: 'Settings', icon: '⚙️', screen: 'Settings' },
];

export default function ProfileScreen({ navigation }: any) {
    const { user, isDemo, logout } = useAuthStore();
    const profileStore = useProfileStore();
    
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [editingName, setEditingName] = useState(user?.name || '');
    const [editingDifficulty, setEditingDifficulty] = useState('Intermediate');
    const [editingDietary, setEditingDietary] = useState('No Restrictions');

    const handleLogout = async () => {
        await logout();
        navigation.reset({ index: 0, routes: [{ name: 'Splash' }] });
    };

    const handleEditProfile = () => {
        setEditingName(user?.name || '');
        setEditModalVisible(true);
    };

    const handleSaveProfile = async () => {
        try {
            // Update profile in store
            await profileStore.updateProfile({
                name: editingName,
                difficulty: editingDifficulty,
                dietary: editingDietary,
            });
            
            Alert.alert('Success', 'Profile updated successfully!');
            setEditModalVisible(false);
        } catch (error) {
            Alert.alert('Error', 'Failed to update profile. Please try again.');
        }
    };

    return (
        <SafeAreaView style={styles.container} edges={['top']}>
            <ScrollView
                showsVerticalScrollIndicator={false}
                contentContainerStyle={styles.scroll}
            >
                {/* ── Avatar + Identity ── */}
                <FadeIn delay={0}>
                    <View style={styles.avatarSection}>
                        <View style={styles.avatarRing}>
                            <View style={styles.avatar}>
                                <Text style={styles.avatarEmoji}>👨‍🍳</Text>
                            </View>
                            <View style={styles.onlineDot} />
                        </View>
                        <Text style={styles.name}>{user?.name || 'Chef'}</Text>
                        <Text style={styles.email}>{user?.email || 'guest@chefmentorx.app'}</Text>
                        <View style={styles.proBadge}>
                            <Text style={styles.proBadgeText}>🏅 Pro Chef</Text>
                        </View>
                    </View>

                </FadeIn>

                {/* ── Stats Row ── */}
                <FadeIn delay={150}>
                    <View style={styles.statsRow}>
                        {STATS.map((stat, i) => (
                            <View key={i} style={[styles.statCircle, { backgroundColor: stat.color }]}>
                                <Text style={styles.statValue}>{stat.value}</Text>
                                <Text style={styles.statLabel}>{stat.label}</Text>
                            </View>
                        ))}
                    </View>

                </FadeIn>

                {/* ── Cooking Profile ── */}
                <FadeIn delay={300}>
                    <View style={styles.section}>
                        <View style={styles.sectionHeader}>
                            <Text style={styles.sectionTitle}>Cooking Profile</Text>
                            <TouchableOpacity onPress={handleEditProfile}>
                                <Text style={styles.editLink}>Edit</Text>
                            </TouchableOpacity>
                        </View>
                        {PROFILE_ITEMS.map((item, i) => (
                            <View key={i} style={styles.profileRow}>
                                <Text style={styles.profileIcon}>{item.icon}</Text>
                                <Text style={styles.profileLabel}>{item.label}</Text>
                                <Text style={styles.profileValue}>{item.value}</Text>
                            </View>
                        ))}
                    </View>

                </FadeIn>

                {/* ── Quick Actions ── */}
                <FadeIn delay={450}>
                    <View style={styles.section}>
                        <Text style={styles.sectionTitle}>Quick Actions</Text>
                        {QUICK_ACTIONS.map((action, i) => (
                            <TouchableOpacity
                                key={i}
                                style={styles.actionRow}
                                onPress={() => action.screen && navigation.navigate(action.screen)}
                                activeOpacity={0.7}
                            >
                                <Text style={styles.actionIcon}>{action.icon}</Text>
                                <Text style={styles.actionLabel}>{action.label}</Text>
                                <Text style={styles.actionArrow}>›</Text>
                            </TouchableOpacity>
                        ))}
                    </View>

                </FadeIn>

                {/* ── Sign Out ── */}
                <FadeIn delay={600}>
                    <TouchableOpacity
                        style={styles.signOutBtn}
                        onPress={handleLogout}
                        activeOpacity={0.8}
                    >
                        <Text style={styles.signOutLabel}>Sign Out</Text>
                    </TouchableOpacity>

                </FadeIn>

                {/* Footer */}
                <Text style={styles.version}>ChefMentor X v1.0.0</Text>
            </ScrollView>

            {/* ── Edit Profile Modal ── */}
            <Modal
                visible={editModalVisible}
                animationType="slide"
                transparent={true}
                onRequestClose={() => setEditModalVisible(false)}
            >
                <View style={styles.modalOverlay}>
                    <View style={styles.modalContent}>
                        <View style={styles.modalHeader}>
                            <Text style={styles.modalTitle}>Edit Cooking Profile</Text>
                            <TouchableOpacity onPress={() => setEditModalVisible(false)}>
                                <Text style={styles.modalClose}>✕</Text>
                            </TouchableOpacity>
                        </View>

                        <ScrollView showsVerticalScrollIndicator={false}>
                            {/* Name Input */}
                            <View style={styles.inputGroup}>
                                <Text style={styles.inputLabel}>Name</Text>
                                <TextInput
                                    value={editingName}
                                    onChangeText={setEditingName}
                                    placeholder="Enter your name"
                                />
                            </View>

                            {/* Difficulty Level */}
                            <View style={styles.inputGroup}>
                                <Text style={styles.inputLabel}>Difficulty Level</Text>
                                <View style={styles.optionsRow}>
                                    {['Beginner', 'Intermediate', 'Advanced'].map((level) => (
                                        <TouchableOpacity
                                            key={level}
                                            style={[
                                                styles.optionPill,
                                                editingDifficulty === level && styles.optionPillActive,
                                            ]}
                                            onPress={() => setEditingDifficulty(level)}
                                        >
                                            <Text
                                                style={[
                                                    styles.optionText,
                                                    editingDifficulty === level && styles.optionTextActive,
                                                ]}
                                            >
                                                {level}
                                            </Text>
                                        </TouchableOpacity>
                                    ))}
                                </View>
                            </View>

                            {/* Dietary Preference */}
                            <View style={styles.inputGroup}>
                                <Text style={styles.inputLabel}>Dietary Preference</Text>
                                <View style={styles.optionsRow}>
                                    {['No Restrictions', 'Vegetarian', 'Vegan', 'Gluten-Free'].map((diet) => (
                                        <TouchableOpacity
                                            key={diet}
                                            style={[
                                                styles.optionPill,
                                                editingDietary === diet && styles.optionPillActive,
                                            ]}
                                            onPress={() => setEditingDietary(diet)}
                                        >
                                            <Text
                                                style={[
                                                    styles.optionText,
                                                    editingDietary === diet && styles.optionTextActive,
                                                ]}
                                            >
                                                {diet}
                                            </Text>
                                        </TouchableOpacity>
                                    ))}
                                </View>
                            </View>

                            {/* Save Button */}
                            <Button
                                title="Save Changes"
                                onPress={handleSaveProfile}
                                style={styles.saveButton}
                            />
                        </ScrollView>
                    </View>
                </View>
            </Modal>
        </SafeAreaView>
    );
}

/* ─── Styles ─────────────────────────────────────────── */
const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: Colors.neutral[50] },
    scroll: { paddingHorizontal: Spacing[6], paddingBottom: 40 },

    /* Avatar */
    avatarSection: { alignItems: 'center', paddingTop: Spacing[6], marginBottom: Spacing[6] },
    avatarRing: {
        width: 100,
        height: 100,
        borderRadius: 50,
        borderWidth: 3,
        borderColor: Colors.brand.orange,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 14,
        position: 'relative',
    },
    avatar: {
        width: 88,
        height: 88,
        borderRadius: 44,
        backgroundColor: Colors.brand.peach,
        alignItems: 'center',
        justifyContent: 'center',
    },
    avatarEmoji: { fontSize: 40 },
    onlineDot: {
        position: 'absolute',
        bottom: 4,
        right: 4,
        width: 18,
        height: 18,
        borderRadius: 9,
        backgroundColor: '#22C55E',
        borderWidth: 3,
        borderColor: Colors.neutral[50],
    },
    name: {
        fontFamily: 'DMSans-Bold',
        fontSize: Typography.fontSize['2xl'],
        fontWeight: '700',
        color: Colors.textMain,
        marginBottom: 2,
    },
    email: {
        fontFamily: 'DMSans',
        fontSize: Typography.fontSize.sm,
        color: Colors.textSub,
        marginBottom: 12,
    },
    proBadge: {
        backgroundColor: Colors.brand.peach,
        paddingHorizontal: 14,
        paddingVertical: 6,
        borderRadius: BorderRadius.full,
    },
    proBadgeText: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: Typography.fontSize.xs,
        fontWeight: '600',
        color: Colors.brand.orange,
    },

    /* Stats */
    statsRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        gap: 10,
        marginBottom: Spacing[6],
    },
    statCircle: {
        flex: 1,
        alignItems: 'center',
        paddingVertical: 20,
        borderRadius: BorderRadius.xl,
    },
    statValue: {
        fontFamily: 'DMSans-Bold',
        fontSize: Typography.fontSize['2xl'],
        fontWeight: '800',
        color: Colors.textMain,
        marginBottom: 4,
    },
    statLabel: {
        fontFamily: 'DMSans',
        fontSize: 11,
        color: Colors.textSub,
        textAlign: 'center',
        lineHeight: 16,
    },

    /* Section */
    section: {
        backgroundColor: Colors.white,
        borderRadius: BorderRadius.xl,
        padding: Spacing[5],
        marginBottom: Spacing[4],
        ...Shadows.sm,
        borderWidth: 1,
        borderColor: Colors.neutral[100],
    },
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 14,
    },
    sectionTitle: {
        fontFamily: 'DMSans-Bold',
        fontSize: Typography.fontSize.lg,
        fontWeight: '700',
        color: Colors.textMain,
    },
    editLink: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: Typography.fontSize.sm,
        fontWeight: '600',
        color: Colors.brand.orange,
    },

    /* Profile items */
    profileRow: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: Colors.neutral[100],
    },
    profileIcon: { fontSize: 18, marginRight: 12 },
    profileLabel: {
        fontFamily: 'DMSans',
        flex: 1,
        fontSize: Typography.fontSize.sm,
        color: Colors.textSub,
    },
    profileValue: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: Typography.fontSize.sm,
        fontWeight: '600',
        color: Colors.textMain,
    },

    /* Quick Actions */
    actionRow: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 14,
        borderBottomWidth: 1,
        borderBottomColor: Colors.neutral[100],
    },
    actionIcon: { fontSize: 18, marginRight: 12 },
    actionLabel: {
        fontFamily: 'DMSans-SemiBold',
        flex: 1,
        fontSize: Typography.fontSize.base,
        fontWeight: '600',
        color: Colors.textMain,
    },
    actionArrow: {
        fontSize: 22,
        color: Colors.neutral[400],
    },

    /* Sign Out */
    signOutBtn: {
        alignItems: 'center',
        paddingVertical: 16,
        borderRadius: BorderRadius.lg,
        borderWidth: 1.5,
        borderColor: Colors.neutral[200],
        marginTop: Spacing[2],
        marginBottom: Spacing[4],
    },
    signOutLabel: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: Typography.fontSize.base,
        fontWeight: '600',
        color: Colors.textSub,
    },

    /* Footer */
    version: {
        fontFamily: 'DMSans',
        fontSize: Typography.fontSize.xs,
        color: Colors.neutral[400],
        textAlign: 'center',
    },
});
