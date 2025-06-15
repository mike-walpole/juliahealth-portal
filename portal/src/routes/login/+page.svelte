<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore, authService } from '$lib/auth.js';
  
  let email = '';
  let password = '';
  let newPassword = '';
  let confirmPassword = '';
  let loading = false;
  let error = '';
  let requiresNewPassword = false;
  let signInResult = null;
  
  // Check if already authenticated
  onMount(() => {
    // First check auth state
    authService.checkAuthState();
    
    const unsubscribe = authStore.subscribe(auth => {
      if (auth.isAuthenticated) {
        console.log('✅ User is authenticated, redirecting to dashboard...');
        goto('/');
      }
    });
    
    return unsubscribe;
  });
  
  async function handleLogin() {
    if (!email || !password) {
      error = 'Please enter both email and password';
      return;
    }
    
    // Check if already authenticated
    if ($authStore.isAuthenticated) {
      console.log('Already authenticated, redirecting...');
      goto('/');
      return;
    }
    
    loading = true;
    error = '';
    
    const result = await authService.login(email, password);
    
    if (result.success) {
      goto('/');
    } else if (result.requiresNewPassword) {
      requiresNewPassword = true;
      signInResult = result.signInResult;
    } else {
      error = result.error || 'Login failed';
    }
    
    loading = false;
  }
  
  async function handleNewPassword() {
    if (!newPassword || !confirmPassword) {
      error = 'Please enter and confirm your new password';
      return;
    }
    
    if (newPassword !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }
    
    if (newPassword.length < 12) {
      error = 'Password must be at least 12 characters long';
      return;
    }
    
    loading = true;
    error = '';
    
    const result = await authService.confirmNewPassword(newPassword, signInResult);
    
    if (result.success) {
      goto('/');
    } else {
      error = result.error || 'Password update failed';
    }
    
    loading = false;
  }
  
  function handleKeyPress(event) {
    if (event.key === 'Enter') {
      if (requiresNewPassword) {
        handleNewPassword();
      } else {
        handleLogin();
      }
    }
  }
</script>

<svelte:head>
  <title>JuliaHealth - Clinician Portal</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-md w-full space-y-8">
    <!-- Header -->
    <div class="text-center">
      <div class="mx-auto h-16 w-16 bg-blue-600 rounded-full flex items-center justify-center">
        <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
        JuliaHealth Portal
      </h2>
      <p class="mt-2 text-sm text-gray-600">
        {requiresNewPassword ? 'Set your new password' : 'Sign in to your clinician account'}
      </p>
    </div>

    <!-- Login Form -->
    {#if !requiresNewPassword}
      <form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              bind:value={email}
              on:keypress={handleKeyPress}
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="dr.martinez@juliahealth.eu"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              bind:value={password}
              on:keypress={handleKeyPress}
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Enter your password"
            />
          </div>
        </div>

        {#if error}
          <div class="bg-red-50 border border-red-200 rounded-lg p-3">
            <div class="flex">
              <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="ml-2 text-sm text-red-700">{error}</p>
            </div>
          </div>
        {/if}

        <div>
          <button
            type="submit"
            disabled={loading}
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {#if loading}
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            {:else}
              Sign in
            {/if}
          </button>
        </div>
      </form>
    {/if}

    <!-- New Password Form -->
    {#if requiresNewPassword}
      <form class="mt-8 space-y-6" on:submit|preventDefault={handleNewPassword}>
        <div class="rounded-md shadow-sm space-y-4">
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
            <div class="flex">
              <svg class="h-5 w-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
              <p class="ml-2 text-sm text-yellow-700">
                This is your first login. Please set a new password.
              </p>
            </div>
          </div>
          
          <div>
            <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-1">
              New Password
            </label>
            <input
              id="newPassword"
              name="newPassword"
              type="password"
              required
              bind:value={newPassword}
              on:keypress={handleKeyPress}
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Enter new password (min 12 characters)"
            />
          </div>
          
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              required
              bind:value={confirmPassword}
              on:keypress={handleKeyPress}
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Confirm new password"
            />
          </div>
        </div>

        <div class="text-xs text-gray-600 bg-gray-50 p-3 rounded-lg">
          <p class="font-medium mb-1">Password requirements:</p>
          <ul class="list-disc list-inside space-y-1">
            <li>At least 12 characters long</li>
            <li>Contains uppercase and lowercase letters</li>
            <li>Contains at least one number</li>
            <li>Contains at least one special character</li>
          </ul>
        </div>

        {#if error}
          <div class="bg-red-50 border border-red-200 rounded-lg p-3">
            <div class="flex">
              <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="ml-2 text-sm text-red-700">{error}</p>
            </div>
          </div>
        {/if}

        <div>
          <button
            type="submit"
            disabled={loading}
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {#if loading}
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Setting password...
            {:else}
              Set New Password
            {/if}
          </button>
        </div>
      </form>
    {/if}

    <!-- Footer -->
    <div class="text-center">
      <p class="text-xs text-gray-500">
        JuliaHealth Patient Recovery Platform<br>
        Secure clinician access only
      </p>
    </div>
  </div>
</div>

<style>
  /* Additional custom styles if needed */
</style> 