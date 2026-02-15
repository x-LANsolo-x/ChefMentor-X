import { makeAutoObservable } from 'mobx';
import AsyncStorage from '@react-native-async-storage/async-storage';

type VoiceSpeed = 'Slow' | 'Normal' | 'Fast';

class SettingsStore {
  // Voice Settings
  voiceSpeed: VoiceSpeed = 'Normal';
  beginnerMode: boolean = false;
  wakeWordEnabled: boolean = true;
  
  // Notifications
  pushNotifications: boolean = true;
  weeklyMealPlan: boolean = false;

  constructor() {
    makeAutoObservable(this);
    this.loadSettings();
  }

  // Voice Speed
  setVoiceSpeed = (speed: VoiceSpeed) => {
    this.voiceSpeed = speed;
    this.saveSettings();
  };

  // Beginner Mode
  setBeginnerMode = (enabled: boolean) => {
    this.beginnerMode = enabled;
    this.saveSettings();
  };

  // Wake Word
  setWakeWordEnabled = (enabled: boolean) => {
    this.wakeWordEnabled = enabled;
    this.saveSettings();
  };

  // Push Notifications
  setPushNotifications = (enabled: boolean) => {
    this.pushNotifications = enabled;
    this.saveSettings();
  };

  // Weekly Meal Plan
  setWeeklyMealPlan = (enabled: boolean) => {
    this.weeklyMealPlan = enabled;
    this.saveSettings();
  };

  // Persistence
  private async saveSettings() {
    try {
      const settings = {
        voiceSpeed: this.voiceSpeed,
        beginnerMode: this.beginnerMode,
        wakeWordEnabled: this.wakeWordEnabled,
        pushNotifications: this.pushNotifications,
        weeklyMealPlan: this.weeklyMealPlan,
      };
      await AsyncStorage.setItem('app_settings', JSON.stringify(settings));
    } catch (error) {
      console.error('Failed to save settings:', error);
    }
  }

  private async loadSettings() {
    try {
      const stored = await AsyncStorage.getItem('app_settings');
      if (stored) {
        const settings = JSON.parse(stored);
        this.voiceSpeed = settings.voiceSpeed || 'Normal';
        this.beginnerMode = settings.beginnerMode || false;
        this.wakeWordEnabled = settings.wakeWordEnabled ?? true;
        this.pushNotifications = settings.pushNotifications ?? true;
        this.weeklyMealPlan = settings.weeklyMealPlan || false;
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  }

  // Reset to defaults
  resetToDefaults = () => {
    this.voiceSpeed = 'Normal';
    this.beginnerMode = false;
    this.wakeWordEnabled = true;
    this.pushNotifications = true;
    this.weeklyMealPlan = false;
    this.saveSettings();
  };
}

export const settingsStore = new SettingsStore();
export const useSettingsStore = () => settingsStore;