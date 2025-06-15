<script>
	import '../app.css';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import AuthGuard from '$lib/AuthGuard.svelte';
	import { authStore, authService } from '$lib/auth.js';
	
	let sidebarOpen = false;
	let connectionStatus = 'checking';
	let lastUpdated = new Date().toLocaleTimeString();
	
	onMount(async () => {
		try {
			const response = await fetch('/api/health');
			connectionStatus = response.ok ? 'connected' : 'error';
		} catch (error) {
			connectionStatus = 'error';
		}
		
		// Update timestamp every minute
		setInterval(() => {
			lastUpdated = new Date().toLocaleTimeString();
		}, 60000);
	});
	
	function toggleSidebar() {
		sidebarOpen = !sidebarOpen;
	}
	
	function closeSidebar() {
		sidebarOpen = false;
	}
	
	$: currentPath = $page.url.pathname;
	$: isLoginPage = currentPath === '/login';
	
	async function handleLogout() {
		await authService.logout();
		closeSidebar();
	}
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Mobile sidebar backdrop -->
	{#if sidebarOpen}
		<div class="fixed inset-0 z-40 lg:hidden">
			<div class="fixed inset-0 bg-black bg-opacity-25" on:click={closeSidebar} on:keydown={(e) => e.key === 'Escape' && closeSidebar()} role="button" tabindex="0"></div>
		</div>
	{/if}

	<!-- Sidebar -->
	<div class="fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 transform {sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:inset-0">
		<div class="flex flex-col h-full">
			<!-- Logo -->
			<div class="flex items-center justify-between h-16 px-6 border-b border-gray-200">
				<div class="flex items-center">
					<div class="flex-shrink-0">
						<h1 class="text-xl font-semibold text-gray-900">JuliaHealth</h1>
						<p class="text-xs text-gray-500">Clinician Portal</p>
					</div>
				</div>
				<button class="lg:hidden text-gray-400 hover:text-gray-600" on:click={closeSidebar}>
					<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>

			<!-- Navigation -->
			<nav class="flex-1 px-4 py-6 space-y-2">
				<a 
					href="/" 
					class="flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors {currentPath === '/' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}"
					on:click={closeSidebar}
				>
					<svg class="mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
					</svg>
					Dashboard
				</a>
				
				<a 
					href="/patients" 
					class="flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors {currentPath === '/patients' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}"
					on:click={closeSidebar}
				>
					<svg class="mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
					</svg>
					Patients
				</a>
				
				<a 
					href="/risk" 
					class="flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors {currentPath === '/risk' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}"
					on:click={closeSidebar}
				>
					<svg class="mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
					</svg>
					Risk Analysis
				</a>
				
				<a 
					href="/reports" 
					class="flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors {currentPath === '/reports' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}"
					on:click={closeSidebar}
				>
					<svg class="mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
					</svg>
					Reports
				</a>
			</nav>

			<!-- User Info & Logout -->
			{#if $authStore.isAuthenticated && $authStore.user}
				<div class="px-4 py-4 border-t border-gray-200">
					<div class="flex items-center justify-between">
						<div class="flex-1 min-w-0">
							<p class="text-sm font-medium text-gray-900 truncate">
								{$authStore.user.name}
							</p>
							<p class="text-xs text-gray-500 truncate">
								{$authStore.user.department}
							</p>
						</div>
						<button
							on:click={handleLogout}
							class="ml-2 p-1 text-gray-400 hover:text-gray-600 rounded-md"
							title="Sign out"
						>
							<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
							</svg>
						</button>
					</div>
				</div>
			{/if}

			<!-- Connection Status -->
			<div class="px-4 py-4 border-t border-gray-200">
				<div class="flex items-center text-xs text-gray-500">
					<div class="flex items-center">
						<div class="h-2 w-2 rounded-full mr-2 {connectionStatus === 'connected' ? 'bg-green-400' : connectionStatus === 'error' ? 'bg-red-400' : 'bg-yellow-400'}"></div>
						<span>
							{connectionStatus === 'connected' ? 'Database Connected' : connectionStatus === 'error' ? 'Connection Error' : 'Checking...'}
						</span>
					</div>
				</div>
				<div class="text-xs text-gray-400 mt-1">
					Updated: {lastUpdated}
				</div>
			</div>
		</div>
	</div>

	<!-- Main content -->
	<div class="lg:pl-64">
		<!-- Top bar -->
		<div class="sticky top-0 z-10 bg-white border-b border-gray-200 lg:hidden">
			<div class="flex items-center justify-between h-16 px-4">
				<button
					type="button"
					class="text-gray-500 hover:text-gray-600"
					on:click={toggleSidebar}
				>
					<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
					</svg>
				</button>
				<h1 class="text-lg font-semibold text-gray-900">JuliaHealth</h1>
				<div class="w-6"></div>
			</div>
		</div>

		<!-- Page content -->
		<main>
			<AuthGuard requireAuth={!isLoginPage}>
				<slot />
			</AuthGuard>
		</main>
	</div>
</div>
