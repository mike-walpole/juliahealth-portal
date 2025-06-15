<script>
	export let data;
	
	function getRiskBadgeColor(risk) {
		if (risk >= 0.8) return 'bg-red-100 text-red-800';
		if (risk >= 0.6) return 'bg-amber-100 text-amber-800';
		if (risk >= 0.4) return 'bg-blue-100 text-blue-800';
		return 'bg-green-100 text-green-800';
	}
	
	function getRiskLabel(risk) {
		if (risk >= 0.8) return 'Critical';
		if (risk >= 0.6) return 'Elevated';
		if (risk >= 0.4) return 'Moderate';
		return 'Stable';
	}
	
	function formatDate(dateStr) {
		return new Date(dateStr).toLocaleDateString();
	}
	
	function getRiskDistribution() {
		// Get all risk scores from all patients' latest data
		const allRiskScores = data.riskTrends
			.filter(patient => patient.riskTrend && patient.riskTrend.length > 0)
			.map(patient => patient.riskTrend[patient.riskTrend.length - 1].risk_score);
		
		const total = allRiskScores.length;
		if (total === 0) return { stable: 0, moderate: 0, elevated: 0, critical: 0 };
		
		const counts = allRiskScores.reduce((acc, risk) => {
			if (risk >= 0.8) acc.critical++;
			else if (risk >= 0.6) acc.elevated++;
			else if (risk >= 0.4) acc.moderate++;
			else acc.stable++;
			return acc;
		}, { stable: 0, moderate: 0, elevated: 0, critical: 0 });
		
		return {
			stable: Math.round((counts.stable / total) * 100),
			moderate: Math.round((counts.moderate / total) * 100),
			elevated: Math.round((counts.elevated / total) * 100),
			critical: Math.round((counts.critical / total) * 100)
		};
	}
	
	$: riskDistribution = getRiskDistribution();
</script>

<svelte:head>
	<title>Risk Analysis - JuliaHealth Clinician Portal</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	<!-- Header -->
	<div class="bg-white border-b border-gray-200">
		<div class="px-6 py-6">
			<h1 class="text-2xl font-semibold text-gray-900">Risk Analysis</h1>
			<p class="mt-1 text-sm text-gray-600">Monitor patient risk patterns and trends</p>
		</div>
	</div>

	<!-- Content -->
	<div class="px-6 py-6">
		<!-- Summary Stats -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.riskStats.totalPatients}</div>
				<div class="text-sm text-gray-600">Total Patients</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.riskStats.avgRisk.toFixed(2)}</div>
				<div class="text-sm text-gray-600">Average Risk Score</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.riskStats.highRiskCount}</div>
				<div class="text-sm text-gray-600">Need Attention</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.relapseEvents.length}</div>
				<div class="text-sm text-gray-600">Recent Events</div>
			</div>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<!-- Risk Distribution -->
			<div class="bg-white rounded-lg border border-gray-200">
				<div class="px-6 py-4 border-b border-gray-200">
					<h2 class="text-lg font-medium text-gray-900">Risk Distribution</h2>
					<p class="text-sm text-gray-600">Current patient risk levels</p>
				</div>
				<div class="p-6">
					<div class="space-y-4">
						<div class="flex items-center justify-between">
							<div class="flex items-center space-x-3">
								<div class="w-3 h-3 rounded-full bg-green-400"></div>
								<span class="text-sm font-medium text-gray-700">Stable (0-39%)</span>
							</div>
							<span class="text-lg font-semibold text-gray-900">{riskDistribution.stable}%</span>
						</div>
						<div class="flex items-center justify-between">
							<div class="flex items-center space-x-3">
								<div class="w-3 h-3 rounded-full bg-blue-400"></div>
								<span class="text-sm font-medium text-gray-700">Moderate (40-59%)</span>
							</div>
							<span class="text-lg font-semibold text-gray-900">{riskDistribution.moderate}%</span>
						</div>
						<div class="flex items-center justify-between">
							<div class="flex items-center space-x-3">
								<div class="w-3 h-3 rounded-full bg-amber-400"></div>
								<span class="text-sm font-medium text-gray-700">Elevated (60-79%)</span>
							</div>
							<span class="text-lg font-semibold text-gray-900">{riskDistribution.elevated}%</span>
						</div>
						<div class="flex items-center justify-between">
							<div class="flex items-center space-x-3">
								<div class="w-3 h-3 rounded-full bg-red-400"></div>
								<span class="text-sm font-medium text-gray-700">Critical (80%+)</span>
							</div>
							<span class="text-lg font-semibold text-gray-900">{riskDistribution.critical}%</span>
						</div>
					</div>
				</div>
			</div>

			<!-- High Risk Patients -->
			<div class="bg-white rounded-lg border border-gray-200">
				<div class="px-6 py-4 border-b border-gray-200">
					<h2 class="text-lg font-medium text-gray-900">Patients Needing Attention</h2>
					<p class="text-sm text-gray-600">Risk score ≥ 60%</p>
				</div>
				<div class="p-6">
					{#if data.highRiskPatients.length > 0}
						<div class="space-y-3">
							{#each data.highRiskPatients.slice(0, 5) as patient}
								<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
									<div class="flex items-center space-x-3">
										<div class="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
											<span class="text-xs font-medium text-gray-700">
												{patient.name.split(' ').map(n => n[0]).join('')}
											</span>
										</div>
										<div>
											<h3 class="text-sm font-medium text-gray-900">{patient.name}</h3>
											<p class="text-xs text-gray-600">{patient.days_sober} days sober</p>
										</div>
									</div>
									<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getRiskBadgeColor(patient.risk_score)}">
										{(patient.risk_score * 100).toFixed(0)}%
									</span>
								</div>
							{/each}
						</div>
					{:else}
						<div class="text-center py-8">
							<svg class="mx-auto h-12 w-12 text-green-400" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
							<h3 class="mt-2 text-sm font-medium text-gray-900">All Patients Stable</h3>
							<p class="mt-1 text-sm text-gray-500">No patients currently need immediate attention.</p>
						</div>
					{/if}
				</div>
			</div>
		</div>

		<!-- Risk Trends -->
		<div class="mt-6 bg-white rounded-lg border border-gray-200">
			<div class="px-6 py-4 border-b border-gray-200">
				<h2 class="text-lg font-medium text-gray-900">Patient Risk Overview</h2>
				<p class="text-sm text-gray-600">Current risk status for all patients</p>
			</div>
			<div class="p-6">
				{#if data.riskTrends.length > 0}
					<div class="space-y-4">
						{#each data.riskTrends as patient}
							{@const latestRisk = patient.riskTrend && patient.riskTrend.length > 0 ? patient.riskTrend[patient.riskTrend.length - 1] : null}
							{#if latestRisk}
								<div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
									<div class="flex items-center space-x-4">
										<div class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
											<span class="text-sm font-medium text-gray-700">
												{patient.name.split(' ').map(n => n[0]).join('')}
											</span>
										</div>
										<div>
											<h3 class="text-sm font-medium text-gray-900">{patient.name}</h3>
											<div class="flex items-center space-x-4 text-xs text-gray-600">
												<span>{latestRisk.days_sober} days sober</span>
												<span>•</span>
												<span>{formatDate(latestRisk.date)}</span>
											</div>
										</div>
									</div>
									<div class="flex items-center space-x-3">
										<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getRiskBadgeColor(latestRisk.risk_score)}">
											{getRiskLabel(latestRisk.risk_score)}
										</span>
										<span class="text-sm font-medium text-gray-900">{(latestRisk.risk_score * 100).toFixed(1)}%</span>
									</div>
								</div>
							{/if}
						{/each}
					</div>
				{:else}
					<div class="text-center py-8">
						<svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
						</svg>
						<h3 class="mt-2 text-sm font-medium text-gray-900">No Risk Data</h3>
						<p class="mt-1 text-sm text-gray-500">Risk trend data is not available.</p>
					</div>
				{/if}
			</div>
		</div>

		<!-- Recent Events -->
		{#if data.relapseEvents.length > 0}
			<div class="mt-6 bg-white rounded-lg border border-gray-200">
				<div class="px-6 py-4 border-b border-gray-200">
					<h2 class="text-lg font-medium text-gray-900">Recent Relapse Events</h2>
					<p class="text-sm text-gray-600">Events requiring clinical attention</p>
				</div>
				<div class="p-6">
					<div class="space-y-4">
						{#each data.relapseEvents as event}
							<div class="flex items-start space-x-4 p-4 bg-red-50 border border-red-200 rounded-lg">
								<div class="flex-shrink-0">
									<svg class="h-5 w-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
										<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
									</svg>
								</div>
								<div class="flex-1">
									<h3 class="text-sm font-medium text-red-800">{event.name}</h3>
									<p class="text-sm text-red-700 mt-1">
										Relapse event on {formatDate(event.date)} • Reset to {event.days_sober} days sober
									</p>
									<p class="text-xs text-red-600 mt-2">
										Current risk: {(event.risk_score * 100).toFixed(1)}% • Requires immediate attention
									</p>
								</div>
							</div>
						{/each}
					</div>
				</div>
			</div>
		{/if}
	</div>
</div> 