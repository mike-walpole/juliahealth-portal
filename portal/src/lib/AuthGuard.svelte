<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore, authService } from '$lib/auth.js';
  
  export let requireAuth = true;
  
  onMount(() => {
    // Check auth state when component mounts
    if (requireAuth) {
      authService.checkAuthState();
    }
  });
  
  // Redirect to login if not authenticated
  $: if (requireAuth && !$authStore.isAuthenticated) {
    goto('/login');
  }
</script>

{#if !requireAuth || $authStore.isAuthenticated}
  <!-- Render content -->
  <slot />
{:else}
  <!-- Not authenticated - will redirect to login -->
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="text-center">
      <p class="text-gray-600">Redirecting to login...</p>
    </div>
  </div>
{/if} 