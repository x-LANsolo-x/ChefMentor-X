import create from 'zustand';
import { persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

type VoiceSpeed = 'Slow' | 'Normal' | 'Fast';

interface SettingsState {
  voiceSpeed: VoiceSpeed;
  beginnerMode: boolean;
  wakeWordEnabled: boolean;
  pushNotifications: boolean;
  weeklyMealPlan: boolean;

  setVoiceSpeed: (speed: VoiceSpeed) => void;
  setBeginnerMode: (enabled: boolean) => void;
  setWakeWordEnabled: (enabled: boolean) => void;
  setPushNotifications: (enabled: boolean) => void;
  setWeeklyMealPlan: (enabled: boolean) => void;
  resetToDefaults: () => void;
}

export const useSettingsStore = create<SettingsState>(
  persist(
    (set) => ({
      voiceSpeed: 'Normal',
      beginnerMode: false,
      wakeWordEnabled: true,
      pushNotifications: true,
      weeklyMealPlan: false,

      setVoiceSpeed: (speed) => set({ voiceSpeed: speed }),
      setBeginnerMode: (enabled) => set({ beginnerMode: enabled }),
      setWakeWordEnabled: (enabled) => set({ wakeWordEnabled: enabled }),
      setPushNotifications: (enabled) => set({ pushNotifications: enabled }),
      setWeeklyMealPlan: (enabled) => set({ weeklyMealPlan: enabled }),

      resetToDefaults: () => set({
        voiceSpeed: 'Normal',
        beginnerMode: false,
        wakeWordEnabled: true,
        pushNotifications: true,
        weeklyMealPlan: false,
      }),
    }),
    {
      name: 'app_settings',
      getStorage: () => AsyncStorage,
    }
  )
);
