import { signIn, signOut, getCurrentUser, fetchAuthSession, confirmSignIn } from 'aws-amplify/auth';
import { writable } from 'svelte/store';
import './amplify.js'; // Initialize Amplify

// Simple auth store - start as not authenticated
export const authStore = writable({
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null
});

class AuthService {
  // Check current authentication state
  async checkAuthState() {
    try {
      const user = await getCurrentUser();
      const session = await fetchAuthSession();
      
      // Check if user is a clinician
      const role = session.tokens?.idToken?.payload['custom:role'];
      
      if (role !== 'clinician') {
        throw new Error('Access denied: Clinicians only');
      }
      
      authStore.set({
        isAuthenticated: true,
        user: {
          id: user.userId,
          email: session.tokens?.idToken?.payload.email,
          name: `${session.tokens?.idToken?.payload.given_name} ${session.tokens?.idToken?.payload.family_name}`,
          role: role,
          clinicianId: session.tokens?.idToken?.payload['custom:clinician_id'],
          department: session.tokens?.idToken?.payload['custom:department']
        },
        loading: false,
        error: null
      });
      
    } catch (error) {
      authStore.set({
        isAuthenticated: false,
        user: null,
        loading: false,
        error: null
      });
    }
  }

  // Sign in
  async login(email, password) {
    try {
      const signInResult = await signIn({
        username: email,
        password: password
      });
      
      // Handle different sign-in states
      if (signInResult.isSignedIn) {
        await this.checkAuthState();
        return { success: true };
      } else if (signInResult.nextStep?.signInStep === 'CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED') {
        return { 
          success: false, 
          requiresNewPassword: true,
          signInResult 
        };
      } else {
        throw new Error('Sign-in incomplete');
      }
      
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message };
    }
  }

  // Confirm sign-in with new password (for first-time users)
  async confirmNewPassword(newPassword, signInResult) {
    try {
      const result = await confirmSignIn({
        challengeResponse: newPassword
      });
      
      if (result.isSignedIn) {
        await this.checkAuthState();
        return { success: true };
      } else {
        throw new Error('Password confirmation failed');
      }
      
    } catch (error) {
      console.error('Password confirmation error:', error);
      return { success: false, error: error.message };
    }
  }

  // Sign out
  async logout() {
    try {
      await signOut();
      authStore.update(state => ({
        ...state,
        isAuthenticated: false,
        user: null,
        loading: false,
        error: null
      }));
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      return { success: false, error: error.message };
    }
  }

  // Get current session
  async getSession() {
    try {
      return await fetchAuthSession();
    } catch (error) {
      console.error('Session error:', error);
      return null;
    }
  }

  // Get auth token for API calls
  async getAuthToken() {
    try {
      const session = await fetchAuthSession();
      return session.tokens?.accessToken?.toString();
    } catch (error) {
      console.error('Token error:', error);
      return null;
    }
  }
}

export const authService = new AuthService();
export default authService; 