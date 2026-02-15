/**
 * ChefMentor X – Completion Screen
 *
 * Stitch ref: chefmentor_x_completion
 * Features:
 *  - Animated confetti (RN Animated circles)
 *  - Dish emoji with pulsing glow
 *  - "Well Done!" heading
 *  - Stats grid (Time, Level, Earned)
 *  - "How was the result?" emoji feedback grid
 *  - "Back to Recipes" primary CTA
 */

import React, { useRef, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    Animated,
    Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors, Typography, Spacing, BorderRadius, Shadows } from '../constants/theme';

const { width: SCREEN_W } = Dimensions.get('window');

// ─── Confetti piece component ───────────────────────

const CONFETTI_COLORS = ['#FF6B4A', '#8EA68B', '#FFD166', '#60A5FA', '#F472B6'];

function ConfettiPiece({ index }: { index: number }) {
    const fall = useRef(new Animated.Value(-20)).current;
    const opacity = useRef(new Animated.Value(1)).current;
    const rotate = useRef(new Animated.Value(0)).current;

    useEffect(() => {
        const delay = index * 200;
        Animated.loop(
            Animated.parallel([
                Animated.timing(fall, {
                    toValue: Dimensions.get('window').height * 0.5,
                    duration: 3500 + index * 300,
                    delay,
                    useNativeDriver: true,
                }),
                Animated.timing(opacity, {
                    toValue: 0,
                    duration: 3500 + index * 300,
                    delay,
                    useNativeDriver: true,
                }),
                Animated.timing(rotate, {
                    toValue: 1,
                    duration: 3500 + index * 300,
                    delay,
                    useNativeDriver: true,
                }),
            ])
        ).start();
    }, []);

    const left = (index * 37 + 13) % 90;
    const spin = rotate.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '360deg'] });

    return (
        <Animated.View
            style={[
                styles.confetti,
                {
                    left: `${left}%`,
                    backgroundColor: CONFETTI_COLORS[index % CONFETTI_COLORS.length],
                    transform: [{ translateY: fall }, { rotate: spin }],
                    opacity,
                },
            ]}
        />
    );
}

// ─── Stats data ─────────────────────────────────────

const STATS = [
    { icon: '⏱', label: 'TIME', value: '12m', bg: '#E9F0E8' },
    { icon: '📊', label: 'LEVEL', value: 'Easy', bg: '#E9F0E8' },
    { icon: '🏆', label: 'EARNED', value: 'Gold', bg: '#E9F0E8' },
];

const FEEDBACK = [
    { emoji: '😋', label: 'Great', sub: 'Tasty!' },
    { emoji: '😐', label: 'Okay', sub: 'Edible' },
    { emoji: '🥴', label: 'Failed', sub: 'Burnt it' },
    { emoji: '📝', label: 'Add Note', sub: 'Optional' },
];

export default function CompletionScreen({ navigation }: any) {
    const scaleAnim = useRef(new Animated.Value(0.5)).current;
    const fadeIn = useRef(new Animated.Value(0)).current;

    useEffect(() => {
        Animated.parallel([
            Animated.spring(scaleAnim, { toValue: 1, friction: 4, tension: 50, useNativeDriver: true }),
            Animated.timing(fadeIn, { toValue: 1, duration: 600, delay: 300, useNativeDriver: true }),
        ]).start();
    }, []);

    const handleBackToRecipes = () => {
        navigation.popToTop();
    };

    return (
        <View style={styles.container}>
            {/* Confetti */}
            <View style={styles.confettiWrap} pointerEvents="none">
                {Array.from({ length: 10 }).map((_, i) => (
                    <ConfettiPiece key={i} index={i} />
                ))}
            </View>

            <SafeAreaView style={styles.safeArea} edges={['top']}>
                <ScrollView
                    showsVerticalScrollIndicator={false}
                    contentContainerStyle={styles.scrollContent}
                >
                    {/* Dish circle */}
                    <Animated.View style={[styles.dishWrap, { transform: [{ scale: scaleAnim }] }]}>
                        <View style={styles.dishGlow} />
                        <View style={styles.dishCircle}>
                            <Text style={styles.dishEmoji}>🍳</Text>
                            {/* Check badge */}
                            <View style={styles.checkBadge}>
                                <Text style={styles.checkIcon}>✓</Text>
                            </View>
                        </View>
                    </Animated.View>

                    {/* Heading */}
                    <Animated.View style={[styles.headingWrap, { opacity: fadeIn }]}>
                        <Text style={styles.heading}>Well Done!</Text>
                        <Text style={styles.subheading}>
                            You cooked{' '}
                            <Text style={styles.recipeName}>Classic Scrambled Eggs</Text>
                        </Text>
                    </Animated.View>

                    {/* Stats grid */}
                    <Animated.View style={[styles.statsRow, { opacity: fadeIn }]}>
                        {STATS.map((stat) => (
                            <View key={stat.label} style={[styles.statCard, { backgroundColor: stat.bg }]}>
                                <View style={styles.statIconCircle}>
                                    <Text style={{ fontSize: 14 }}>{stat.icon}</Text>
                                </View>
                                <Text style={styles.statLabel}>{stat.label}</Text>
                                <Text style={styles.statValue}>{stat.value}</Text>
                            </View>
                        ))}
                    </Animated.View>

                    {/* Feedback */}
                    <Animated.View style={[styles.feedbackSection, { opacity: fadeIn }]}>
                        <Text style={styles.feedbackTitle}>How was the result?</Text>
                        <View style={styles.feedbackGrid}>
                            {FEEDBACK.map((fb, i) => (
                                <TouchableOpacity
                                    key={fb.label}
                                    style={[
                                        styles.feedbackCard,
                                        i === 3 && styles.feedbackCardDashed,
                                    ]}
                                    activeOpacity={0.85}
                                    accessibilityLabel={`Rate as ${fb.label}`}
                                >
                                    <Text style={styles.feedbackEmoji}>
                                        {i === 3 ? '📝' : fb.emoji}
                                    </Text>
                                    <Text style={styles.feedbackLabel}>{fb.label}</Text>
                                    <Text style={styles.feedbackSub}>{fb.sub}</Text>
                                </TouchableOpacity>
                            ))}
                        </View>
                    </Animated.View>
                </ScrollView>

                {/* CTA */}
                <View style={styles.ctaWrap}>
                    <TouchableOpacity
                        style={styles.ctaBtn}
                        onPress={handleBackToRecipes}
                        activeOpacity={0.9}
                        accessibilityRole="button"
                    >
                        <Text style={styles.ctaText}>Back to Recipes</Text>
                        <Text style={styles.ctaArrow}>→</Text>
                    </TouchableOpacity>

                    {/* Post-cook → Analyze link */}
                    <TouchableOpacity
                        style={styles.analyzeLink}
                        onPress={() => navigation.getParent()?.navigate('AnalyzeTab')}
                        activeOpacity={0.85}
                    >
                        <Text style={styles.analyzeLinkText}>
                            🔬 Something went wrong? Analyze your dish
                        </Text>
                    </TouchableOpacity>
                </View>
            </SafeAreaView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#FDFCF8' },
    safeArea: { flex: 1 },
    scrollContent: {
        paddingHorizontal: Spacing[6],
        paddingBottom: 120,
        alignItems: 'center',
    },

    // ─── Confetti ─────────────────────
    confettiWrap: {
        ...StyleSheet.absoluteFillObject,
        zIndex: 5,
        overflow: 'hidden',
        height: '50%',
    },
    confetti: {
        position: 'absolute',
        width: 10,
        height: 10,
        borderRadius: 2,
        top: -10,
    },

    // ─── Dish circle ──────────────────
    dishWrap: {
        marginTop: Spacing[10],
        marginBottom: Spacing[6],
        alignItems: 'center',
        justifyContent: 'center',
    },
    dishGlow: {
        position: 'absolute',
        width: 210,
        height: 210,
        borderRadius: 105,
        backgroundColor: Colors.brand.peach,
        opacity: 0.4,
    },
    dishCircle: {
        width: 180,
        height: 180,
        borderRadius: 90,
        backgroundColor: Colors.white,
        alignItems: 'center',
        justifyContent: 'center',
        borderWidth: 4,
        borderColor: Colors.white,
        ...Shadows.base,
    },
    dishEmoji: { fontSize: 80 },
    checkBadge: {
        position: 'absolute',
        bottom: 12,
        right: 12,
        width: 36,
        height: 36,
        borderRadius: 18,
        backgroundColor: Colors.brand.orange,
        alignItems: 'center',
        justifyContent: 'center',
        ...Shadows.md,
    },
    checkIcon: { color: Colors.white, fontSize: 20, fontWeight: Typography.fontWeight.bold },

    // ─── Heading ──────────────────────
    headingWrap: { alignItems: 'center', marginBottom: Spacing[8] },
    heading: {
        fontSize: Typography.fontSize['3xl'],
        fontWeight: Typography.fontWeight.extrabold,
        color: Colors.neutral[900],
        marginBottom: Spacing[2],
    },
    subheading: {
        fontSize: Typography.fontSize.lg,
        color: Colors.neutral[500],
        fontWeight: Typography.fontWeight.medium,
    },
    recipeName: { color: Colors.brand.orange, fontWeight: Typography.fontWeight.semibold },

    // ─── Stats ────────────────────────
    statsRow: {
        flexDirection: 'row',
        gap: 10,
        width: '100%',
        marginBottom: Spacing[10],
    },
    statCard: {
        flex: 1,
        aspectRatio: 1,
        borderRadius: BorderRadius.lg + 4,
        alignItems: 'center',
        justifyContent: 'center',
        padding: Spacing[3],
        ...Shadows.sm,
    },
    statIconCircle: {
        width: 32,
        height: 32,
        borderRadius: 16,
        backgroundColor: Colors.white,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: Spacing[2],
        ...Shadows.sm,
    },
    statLabel: {
        fontSize: 10,
        fontWeight: Typography.fontWeight.semibold,
        color: Colors.neutral[500],
        letterSpacing: 0.5,
        marginBottom: 2,
    },
    statValue: {
        fontSize: Typography.fontSize.sm,
        fontWeight: Typography.fontWeight.bold,
        color: Colors.neutral[800],
    },

    // ─── Feedback ─────────────────────
    feedbackSection: { width: '100%' },
    feedbackTitle: {
        fontSize: Typography.fontSize.lg,
        fontWeight: Typography.fontWeight.bold,
        color: Colors.neutral[900],
        textAlign: 'center',
        marginBottom: Spacing[4],
    },
    feedbackGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 12,
    },
    feedbackCard: {
        width: (SCREEN_W - 48 - 12) / 2,
        backgroundColor: Colors.white,
        borderRadius: BorderRadius.lg + 4,
        padding: Spacing[4],
        alignItems: 'center',
        justifyContent: 'center',
        ...Shadows.base,
        borderWidth: 2,
        borderColor: 'transparent',
    },
    feedbackCardDashed: {
        backgroundColor: Colors.neutral[50],
        borderStyle: 'dashed',
        borderColor: Colors.neutral[200],
    },
    feedbackEmoji: { fontSize: 36, marginBottom: Spacing[2] },
    feedbackLabel: {
        fontSize: Typography.fontSize.base,
        fontWeight: Typography.fontWeight.bold,
        color: Colors.neutral[800],
    },
    feedbackSub: {
        fontSize: Typography.fontSize.xs,
        color: Colors.neutral[400],
        marginTop: 2,
    },

    // ─── CTA ──────────────────────────
    ctaWrap: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        padding: Spacing[6],
        paddingTop: Spacing[4],
        paddingBottom: 40,
        backgroundColor: 'rgba(253,252,248,0.95)',
    },
    ctaBtn: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 10,
        backgroundColor: Colors.brand.orange,
        paddingVertical: 18,
        borderRadius: BorderRadius.lg + 4,
        ...Shadows.glow,
    },
    ctaText: { fontSize: Typography.fontSize.lg, fontWeight: Typography.fontWeight.bold, color: Colors.white },
    ctaArrow: { fontSize: 20, color: Colors.white },

    // ── Analyze Link ─────────────────
    analyzeLink: {
        marginTop: 12,
        paddingVertical: 12,
        alignItems: 'center',
    },
    analyzeLinkText: {
        fontSize: Typography.fontSize.sm,
        fontWeight: Typography.fontWeight.semibold,
        color: Colors.brand.orange,
        textDecorationLine: 'underline',
    },
});
