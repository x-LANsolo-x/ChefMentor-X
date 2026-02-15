/**
 * ChefMentor X – Analysis Loading Screen
 *
 * Stitch ref: chefmentor_x_analysis_loading
 * Features:
 *  - Progress bar (3 of 4 steps filled)
 *  - Dish preview circle with pulsing glow
 *  - "Analyzing Your Dish..." heading
 *  - Circular progress ring (animated 0→100%)
 *  - Step checklist (✓ done, spinner active, ○ pending)
 *  - "Usually takes 5–10 seconds" hint
 *  - Auto-navigate to DiagnosisResult after simulated delay
 */

import React, { useRef, useEffect, useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    Animated,
    Easing,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Colors, Typography, Spacing, BorderRadius, Shadows } from '../constants/theme';

const STEPS = [
    { label: 'Detecting ingredients...', delay: 0 },
    { label: 'Evaluating color...', delay: 1500 },
    { label: 'Checking texture...', delay: 3000 },
    { label: 'Generating diagnosis...', delay: 4500 },
];

export default function AnalysisLoadingScreen({ navigation, route }: any) {
    const { imageUri, context } = route?.params || {};
    const [completedSteps, setCompletedSteps] = useState(0);
    const [error, setError] = useState<string | null>(null);
    const pulseAnim = useRef(new Animated.Value(0.5)).current;
    const spinAnim = useRef(new Animated.Value(0)).current;
    const fadeIn = useRef(new Animated.Value(0)).current;
    const progressAnim = useRef(new Animated.Value(0)).current;

    // Pulse glow
    useEffect(() => {
        Animated.loop(
            Animated.sequence([
                Animated.timing(pulseAnim, { toValue: 1, duration: 1500, useNativeDriver: true }),
                Animated.timing(pulseAnim, { toValue: 0.5, duration: 1500, useNativeDriver: true }),
            ])
        ).start();
    }, []);

    // Spin
    useEffect(() => {
        Animated.loop(
            Animated.timing(spinAnim, { toValue: 1, duration: 3000, easing: Easing.linear, useNativeDriver: true })
        ).start();
    }, []);

    // Fade in
    useEffect(() => {
        Animated.timing(fadeIn, { toValue: 1, duration: 600, useNativeDriver: true }).start();
    }, []);

    // Upload image and analyze
    useEffect(() => {
        const analyzeImage = async () => {
            try {
                // Animate progress
                Animated.timing(progressAnim, {
                    toValue: 100,
                    duration: 6000,
                    easing: Easing.out(Easing.cubic),
                    useNativeDriver: false,
                }).start();

                // Step through checklist
                STEPS.forEach((step, i) => {
                    setTimeout(() => setCompletedSteps(i + 1), step.delay + 1200);
                });

                if (!imageUri) {
                    setError('No image provided');
                    return;
                }

                // Create form data for image upload
                const formData = new FormData();
                
                // Extract filename from URI
                const filename = imageUri.split('/').pop() || 'photo.jpg';
                const match = /\.(\w+)$/.exec(filename);
                const type = match ? `image/${match[1]}` : 'image/jpeg';

                formData.append('image', {
                    uri: imageUri,
                    name: filename,
                    type: type,
                } as any);

                // Add context data
                if (context) {
                    formData.append('heat_level', context.heat_level || '');
                    formData.append('timing', context.timing || '');
                    formData.append('modifications', JSON.stringify(context.modifications || []));
                    formData.append('notes', context.notes || '');
                }

                // Call the backend API
                const response = await fetch('http://localhost:8000/api/v1/failure/analyze', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Analysis failed');
                }

                const result = await response.json();

                // Navigate to results
                setTimeout(() => {
                    navigation.replace('DiagnosisResult', { analysis: result });
                }, 6500);

            } catch (err: any) {
                console.error('Analysis error:', err);
                setError(err.message || 'Failed to analyze image');
                setTimeout(() => {
                    navigation.goBack();
                }, 3000);
            }
        };

        analyzeImage();
    }, [imageUri, context]);

    const spin = spinAnim.interpolate({
        inputRange: [0, 1],
        outputRange: ['0deg', '360deg'],
    });

    const progressPercent = progressAnim.interpolate({
        inputRange: [0, 100],
        outputRange: ['0%', '100%'],
    });

    return (
        <SafeAreaView style={styles.container} edges={['top']}>
            {/* Progress bar */}
            <View style={styles.progressRow}>
                <View style={[styles.progressBar, styles.progressActive]} />
                <View style={[styles.progressBar, styles.progressActive]} />
                <View style={[styles.progressBar, styles.progressActive]} />
                <View style={styles.progressBar} />
            </View>

            <Animated.View style={[styles.content, { opacity: fadeIn }]}>
                {/* Dish preview */}
                <View style={styles.dishWrap}>
                    <Animated.View style={[styles.dishGlow, { opacity: pulseAnim }]} />
                    <View style={styles.dishCircle}>
                        <Text style={styles.dishEmoji}>🍳</Text>
                    </View>
                </View>

                {/* Heading */}
                <Text style={styles.heading}>Analyzing Your Dish...</Text>
                <Text style={styles.subheading}>Our AI chef is identifying ingredients</Text>

                {/* Progress ring */}
                <View style={styles.ringWrap}>
                    {/* Background ring */}
                    <View style={styles.ringBg} />
                    {/* Foreground ring (simplified — using Animated width bar instead of SVG) */}
                    <View style={styles.ringCenter}>
                        <Animated.Text style={styles.ringPercent}>
                            {progressAnim.interpolate({
                                inputRange: [0, 100],
                                outputRange: ['0', '100'],
                                extrapolate: 'clamp',
                            })}
                        </Animated.Text>
                        <Text style={styles.ringLabel}>%</Text>
                    </View>
                    {/* Spinning dot */}
                    <Animated.View style={[styles.spinDot, { transform: [{ rotate: spin }] }]}>
                        <View style={styles.spinDotInner} />
                    </Animated.View>
                </View>

                {/* Step checklist */}
                <View style={styles.stepList}>
                    {STEPS.map((step, i) => {
                        const isDone = completedSteps > i;
                        const isActive = completedSteps === i;
                        return (
                            <View key={step.label} style={styles.stepRow}>
                                <View
                                    style={[
                                        styles.stepIcon,
                                        isDone && styles.stepIconDone,
                                        isActive && styles.stepIconActive,
                                        !isDone && !isActive && styles.stepIconPending,
                                    ]}
                                >
                                    <Text style={styles.stepIconText}>
                                        {isDone ? '✓' : isActive ? '◌' : '○'}
                                    </Text>
                                </View>
                                <Text
                                    style={[
                                        styles.stepLabel,
                                        isDone && styles.stepLabelDone,
                                        isActive && styles.stepLabelActive,
                                    ]}
                                >
                                    {step.label}
                                </Text>
                            </View>
                        );
                    })}
                </View>

                {/* Hint */}
                <View style={styles.hintCard}>
                    <Text style={{ fontSize: 18, marginRight: 10 }}>⏱</Text>
                    <Text style={styles.hintText}>
                        Usually takes <Text style={styles.hintBold}>5–10 seconds</Text>. Hang tight!
                    </Text>
                </View>
            </Animated.View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#FDFCF8' },

    // Progress
    progressRow: {
        flexDirection: 'row',
        paddingHorizontal: Spacing[6],
        gap: 6,
        paddingVertical: Spacing[2],
    },
    progressBar: {
        flex: 1,
        height: 4,
        borderRadius: 2,
        backgroundColor: Colors.neutral[200],
    },
    progressActive: { backgroundColor: Colors.brand.orange },

    // Content
    content: {
        flex: 1,
        alignItems: 'center',
        paddingTop: Spacing[8],
        paddingHorizontal: Spacing[6],
    },

    // Dish preview
    dishWrap: {
        marginBottom: Spacing[6],
        alignItems: 'center',
        justifyContent: 'center',
    },
    dishGlow: {
        position: 'absolute',
        width: 120,
        height: 120,
        borderRadius: 60,
        backgroundColor: 'rgba(255,107,74,0.2)',
    },
    dishCircle: {
        width: 80,
        height: 80,
        borderRadius: 40,
        backgroundColor: Colors.white,
        alignItems: 'center',
        justifyContent: 'center',
        borderWidth: 4,
        borderColor: Colors.white,
        ...Shadows.lg,
    },
    dishEmoji: { fontSize: 36 },

    // Heading
    heading: {
        fontSize: Typography.fontSize['2xl'],
        fontWeight: Typography.fontWeight.bold,
        color: Colors.brand.orange,
        marginBottom: Spacing[2],
        textAlign: 'center',
    },
    subheading: {
        fontSize: Typography.fontSize.sm,
        color: Colors.neutral[500],
        textAlign: 'center',
        marginBottom: Spacing[10],
    },

    // Ring
    ringWrap: {
        width: 180,
        height: 180,
        marginBottom: Spacing[10],
        alignItems: 'center',
        justifyContent: 'center',
    },
    ringBg: {
        position: 'absolute',
        width: 180,
        height: 180,
        borderRadius: 90,
        borderWidth: 10,
        borderColor: Colors.neutral[100],
    },
    ringCenter: {
        flexDirection: 'row',
        alignItems: 'flex-end',
    },
    ringPercent: {
        fontSize: 42,
        fontWeight: Typography.fontWeight.extrabold,
        color: '#8EA68B',
    },
    ringLabel: {
        fontSize: Typography.fontSize.lg,
        fontWeight: Typography.fontWeight.medium,
        color: Colors.neutral[500],
        marginBottom: 6,
        marginLeft: 2,
    },
    spinDot: {
        position: 'absolute',
        width: 180,
        height: 180,
        alignItems: 'center',
    },
    spinDotInner: {
        width: 14,
        height: 14,
        borderRadius: 7,
        backgroundColor: Colors.brand.orange,
        borderWidth: 2,
        borderColor: Colors.white,
        marginTop: -3,
        ...Shadows.sm,
    },

    // Steps
    stepList: {
        width: '100%',
        maxWidth: 280,
        gap: 14,
        marginBottom: Spacing[10],
    },
    stepRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 14,
    },
    stepIcon: {
        width: 32,
        height: 32,
        borderRadius: 16,
        alignItems: 'center',
        justifyContent: 'center',
    },
    stepIconDone: { backgroundColor: '#8EA68B' },
    stepIconActive: { backgroundColor: '#FFF0ED', borderWidth: 2, borderColor: 'rgba(255,107,74,0.2)' },
    stepIconPending: { backgroundColor: Colors.neutral[100] },
    stepIconText: { fontSize: 14, fontWeight: Typography.fontWeight.bold, color: Colors.white },
    stepLabel: {
        fontSize: Typography.fontSize.base,
        fontWeight: Typography.fontWeight.medium,
        color: Colors.neutral[900],
    },
    stepLabelDone: { color: Colors.neutral[900] },
    stepLabelActive: { color: Colors.neutral[900] },

    // Hint
    hintCard: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Colors.neutral[50],
        borderRadius: BorderRadius.lg + 4,
        padding: Spacing[4],
        borderWidth: 1,
        borderColor: Colors.neutral[100],
        width: '100%',
    },
    hintText: {
        fontSize: Typography.fontSize.sm,
        color: Colors.neutral[500],
        flex: 1,
    },
    hintBold: {
        color: Colors.neutral[900],
        fontWeight: Typography.fontWeight.semibold,
    },
});
