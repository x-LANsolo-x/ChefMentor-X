/**
 * ChefMentor X – Login Screen
 * Matches stitch design: chefmentor_x_login
 *
 * Layout: Back button, orange logo circle, "Welcome Back" Playfair title,
 * Google Sign-In button, Apple Sign-In button, "or" divider,
 * "Continue as Guest" link, Terms footer.
 *
 * Preserves existing Google OAuth logic from the previous implementation.
 */

import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    ActivityIndicator,
    StatusBar,
} from 'react-native';
import * as Google from 'expo-auth-session/providers/google';
import * as WebBrowser from 'expo-web-browser';
import { Colors, Typography, Spacing, BorderRadius, Shadows } from '../constants/theme';
import { useAuthStore } from '../stores/authStore';
import { apiClient } from '../services/apiClient';
import { ENV } from '../config/env';

WebBrowser.maybeCompleteAuthSession();

export default function LoginScreen({ navigation }: any) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const { setUser, setDemo } = useAuthStore();

    const [request, response, promptAsync] = Google.useAuthRequest({
        clientId: ENV.GOOGLE_CLIENT_ID,
        iosClientId: 'YOUR_IOS_CLIENT_ID',
        androidClientId: 'YOUR_ANDROID_CLIENT_ID',
        redirectUri: 'https://auth.expo.io/@chefmentorx/chefmentor-x',
    });

    useEffect(() => {
        if (response?.type === 'success') {
            const { id_token } = response.params;
            handleGoogleLogin(id_token);
        }
    }, [response]);

    const handleGoogleLogin = async (idToken: string) => {
        setLoading(true);
        setError(null);
        try {
            const { data } = await apiClient.post('/auth/google', { token: idToken });
            const user = {
                id: data.user_id,
                email: data.email,
                name: data.name,
                skillLevel: 'beginner' as const,
                createdAt: new Date().toISOString(),
            };
            await setUser(user, data.access_token, data.refresh_token);
            navigation.replace('Permissions');
        } catch (err: any) {
            setError(err.message || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleGuestLogin = () => {
        setDemo();
        navigation.replace('MainTabs');
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="dark-content" backgroundColor="transparent" translucent />

            {/* Decorative blob */}
            <View style={styles.blobTopRight} />

            {/* Header with back button */}
            <View style={styles.header}>
                <TouchableOpacity
                    style={styles.backBtn}
                    onPress={() => navigation.goBack()}
                    activeOpacity={0.7}
                >
                    <Text style={styles.backIcon}>←</Text>
                </TouchableOpacity>
            </View>

            {/* ── Content ── */}
            <View style={styles.content}>
                {/* Orange logo circle */}
                <View style={styles.logoCircle}>
                    <Text style={{ fontSize: 40 }}>🍴</Text>
                </View>

                {/* Title */}
                <Text style={styles.title}>Welcome Back</Text>
                <Text style={styles.subtitle}>
                    Sign in to access your{'\n'}cooking journey
                </Text>

                {/* Auth buttons */}
                <View style={styles.btnGroup}>
                    {/* Google */}
                    <TouchableOpacity
                        style={styles.googleBtn}
                        onPress={() => promptAsync()}
                        disabled={!request || loading}
                        activeOpacity={0.85}
                    >
                        {loading ? (
                            <ActivityIndicator color={Colors.textMain} />
                        ) : (
                            <>
                                <Text style={styles.googleIcon}>G</Text>
                                <Text style={styles.googleText}>Continue with Google</Text>
                            </>
                        )}
                    </TouchableOpacity>

                    {/* Apple */}
                    <TouchableOpacity style={styles.appleBtn} activeOpacity={0.85}>
                        <Text style={{ fontSize: 20, color: Colors.white }}>🍎</Text>
                        <Text style={styles.appleText}>Continue with Apple</Text>
                    </TouchableOpacity>
                </View>

                {/* OR divider */}
                <View style={styles.divider}>
                    <View style={styles.dividerLine} />
                    <Text style={styles.dividerLabel}>OR</Text>
                    <View style={styles.dividerLine} />
                </View>

                {/* Guest */}
                <TouchableOpacity onPress={handleGuestLogin} activeOpacity={0.7}>
                    <Text style={styles.guestLabel}>Continue as Guest</Text>
                </TouchableOpacity>

                {/* Error message */}
                {error ? <Text style={styles.errorMsg}>{error}</Text> : null}
            </View>

            {/* Footer */}
            <View style={styles.footer}>
                <Text style={styles.terms}>
                    By continuing, you agree to our{' '}
                    <Text style={styles.termsLink}>Terms</Text> &{' '}
                    <Text style={styles.termsLink}>Privacy Policy</Text>
                </Text>
            </View>
        </View>
    );
}

/* ─── Styles ─────────────────────────────────────────── */
const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: Colors.surfaceLight,
    },

    /* Background blob */
    blobTopRight: {
        position: 'absolute',
        top: -60,
        right: -60,
        width: 250,
        height: 250,
        borderRadius: 125,
        backgroundColor: 'rgba(255,239,235,0.8)',
    },

    /* Header */
    header: {
        paddingHorizontal: Spacing[6],
        paddingTop: 56,
        paddingBottom: 8,
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
    backIcon: {
        fontSize: 18,
        color: Colors.textMain,
    },

    /* Content */
    content: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        paddingHorizontal: 32,
        paddingBottom: 40,
    },
    logoCircle: {
        width: 96,
        height: 96,
        borderRadius: 48,
        backgroundColor: Colors.brand.orange,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 28,
        ...Shadows.glow,
    },
    title: {
        fontFamily: 'PlayfairDisplay-Bold',
        fontSize: 36,
        fontWeight: '700',
        color: Colors.textMain,
        marginBottom: 10,
        letterSpacing: -0.5,
    },
    subtitle: {
        fontFamily: 'DMSans',
        fontSize: Typography.fontSize.lg,
        fontWeight: '500',
        color: Colors.textSub,
        textAlign: 'center',
        lineHeight: 26,
        marginBottom: 36,
    },

    /* Buttons */
    btnGroup: {
        width: '100%',
        gap: 14,
    },
    googleBtn: {
        width: '100%',
        height: 56,
        backgroundColor: Colors.white,
        borderWidth: 1,
        borderColor: Colors.neutral[200],
        borderRadius: BorderRadius.lg,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 10,
        ...Shadows.sm,
    },
    googleIcon: {
        fontSize: 20,
        fontWeight: '700',
        color: Colors.textMain,
    },
    googleText: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: 17,
        fontWeight: '600',
        color: Colors.textMain,
    },
    appleBtn: {
        width: '100%',
        height: 56,
        backgroundColor: Colors.black,
        borderRadius: BorderRadius.lg,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 10,
        ...Shadows.md,
    },
    appleText: {
        fontFamily: 'DMSans-SemiBold',
        fontSize: 17,
        fontWeight: '600',
        color: Colors.white,
    },

    /* Divider */
    divider: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 16,
        marginVertical: 28,
        width: '100%',
    },
    dividerLine: {
        flex: 1,
        height: 1,
        backgroundColor: Colors.neutral[200],
    },
    dividerLabel: {
        fontFamily: 'DMSans-Medium',
        fontSize: Typography.fontSize.sm,
        fontWeight: '500',
        color: Colors.neutral[400],
        letterSpacing: 1.5,
    },

    /* Guest */
    guestLabel: {
        fontFamily: 'DMSans-Bold',
        fontSize: Typography.fontSize.lg,
        fontWeight: '700',
        color: Colors.brand.orange,
    },

    /* Error */
    errorMsg: {
        fontFamily: 'DMSans',
        fontSize: Typography.fontSize.sm,
        color: Colors.error,
        marginTop: 16,
        textAlign: 'center',
    },

    /* Footer */
    footer: {
        paddingHorizontal: Spacing[6],
        paddingBottom: 36,
        alignItems: 'center',
    },
    terms: {
        fontFamily: 'DMSans',
        fontSize: Typography.fontSize.xs,
        color: Colors.textSub,
        textAlign: 'center',
        lineHeight: 18,
    },
    termsLink: {
        color: Colors.textMain,
        fontWeight: '600',
        textDecorationLine: 'underline',
        textDecorationColor: Colors.brand.orange,
    },
});