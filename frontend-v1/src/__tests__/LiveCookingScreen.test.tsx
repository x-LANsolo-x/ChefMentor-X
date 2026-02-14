/**
 * Tests for LiveCookingScreen - Voice commands and step navigation
 */
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import LiveCookingScreen from '../screens/LiveCookingScreen';
import { voiceService } from '../services/voiceService';

// Mock dependencies
jest.mock('../services/voiceService');

describe('LiveCookingScreen', () => {
  const mockNavigation = {
    navigate: jest.fn(),
    goBack: jest.fn(),
  };

  const mockRoute = {
    params: {
      recipeId: 'test-recipe-1',
      recipeName: 'Test Recipe',
    },
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders correctly with initial step', () => {
    const { getByText } = render(
      <LiveCookingScreen navigation={mockNavigation} route={mockRoute} />
    );
    expect(getByText(/Step 1/i)).toBeTruthy();
  });

  it('advances to next step when next button is pressed', () => {
    const { getByText } = render(
      <LiveCookingScreen navigation={mockNavigation} route={mockRoute} />
    );
    
    const nextButton = getByText(/Next Step/i);
    fireEvent.press(nextButton);
    
    expect(getByText(/Step 2/i)).toBeTruthy();
  });

  it('handles voice command button press', async () => {
    const mockStartListening = jest.fn().mockResolvedValue(true);
    (voiceService.startListening as jest.Mock) = mockStartListening;

    const { getByText } = render(
      <LiveCookingScreen navigation={mockNavigation} route={mockRoute} />
    );
    
    const voiceButton = getByText(/Voice/i);
    fireEvent.press(voiceButton);
    
    await waitFor(() => {
      expect(mockStartListening).toHaveBeenCalled();
    });
  });

  it('handles timer start and countdown', async () => {
    const { getByText } = render(
      <LiveCookingScreen navigation={mockNavigation} route={mockRoute} />
    );
    
    const timerButton = getByText(/Tap to start timer/i);
    fireEvent.press(timerButton);
    
    await waitFor(() => {
      expect(getByText(/Tap to pause/i)).toBeTruthy();
    });
  });

  it('navigates to completion screen on last step', () => {
    const { getByText } = render(
      <LiveCookingScreen navigation={mockNavigation} route={mockRoute} />
    );
    
    // Advance through all steps to the last one
    const nextButton = getByText(/Next Step/i);
    
    // Press next multiple times (assuming 3 steps in test recipe)
    fireEvent.press(nextButton); // Step 2
    fireEvent.press(nextButton); // Step 3
    
    // Last step should show "Finish" button
    const finishButton = getByText(/Finish/i);
    fireEvent.press(finishButton);
    
    expect(mockNavigation.navigate).toHaveBeenCalledWith('Completion', expect.any(Object));
  });
});
