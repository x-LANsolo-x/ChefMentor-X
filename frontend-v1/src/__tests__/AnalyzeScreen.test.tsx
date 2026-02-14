/**
 * Tests for AnalyzeScreen - Camera and image upload functionality
 */
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import AnalyzeScreen from '../screens/AnalyzeScreen';
import * as ImagePicker from 'expo-image-picker';

// Mock dependencies
jest.mock('expo-image-picker');
jest.mock('../services/analysisService');

describe('AnalyzeScreen', () => {
  const mockNavigation = {
    navigate: jest.fn(),
    goBack: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders correctly', () => {
    const { getByText } = render(<AnalyzeScreen navigation={mockNavigation} />);
    expect(getByText(/Analyze Failed Dish/i)).toBeTruthy();
  });

  it('handles camera permission request', async () => {
    const mockRequestPermission = jest.fn().mockResolvedValue({ status: 'granted' });
    (ImagePicker.requestCameraPermissionsAsync as jest.Mock) = mockRequestPermission;

    const { getByText } = render(<AnalyzeScreen navigation={mockNavigation} />);
    const cameraButton = getByText(/Take Photo/i);
    
    fireEvent.press(cameraButton);
    
    await waitFor(() => {
      expect(mockRequestPermission).toHaveBeenCalled();
    });
  });

  it('handles image selection from library', async () => {
    const mockLaunchImageLibrary = jest.fn().mockResolvedValue({
      canceled: false,
      assets: [{ uri: 'file://test-image.jpg' }],
    });
    (ImagePicker.launchImageLibraryAsync as jest.Mock) = mockLaunchImageLibrary;

    const { getByText } = render(<AnalyzeScreen navigation={mockNavigation} />);
    const uploadButton = getByText(/Upload Photo/i);
    
    fireEvent.press(uploadButton);
    
    await waitFor(() => {
      expect(mockLaunchImageLibrary).toHaveBeenCalled();
    });
  });

  it('shows permission denied message when camera access is denied', async () => {
    const mockRequestPermission = jest.fn().mockResolvedValue({ status: 'denied' });
    (ImagePicker.requestCameraPermissionsAsync as jest.Mock) = mockRequestPermission;

    const { getByText } = render(<AnalyzeScreen navigation={mockNavigation} />);
    const cameraButton = getByText(/Take Photo/i);
    
    fireEvent.press(cameraButton);
    
    await waitFor(() => {
      expect(getByText(/Permission/i)).toBeTruthy();
    });
  });
});
