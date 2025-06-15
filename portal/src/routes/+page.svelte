<script>
	export let data;
	import { authStore } from '$lib/auth.js';
	
	let expandedPatient = null;
	
	function getRiskColor(risk) {
		if (risk >= 0.8) return 'bg-red-50 border-red-200 text-red-700'; // Only for critical
		if (risk >= 0.6) return 'bg-amber-50 border-amber-200 text-amber-700';
		if (risk >= 0.4) return 'bg-blue-50 border-blue-200 text-blue-700';
		return 'bg-green-50 border-green-200 text-green-700';
	}
	
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
	
	function getWeeklySummary(patient) {
		// AI-generated placeholder summaries
		const summaries = {
			'Sarah Chen': 'Strong week with consistent engagement. Stress levels elevated due to work deadlines but coping strategies effective. Sleep quality improving.',
			'Marcus Rodriguez': 'Excellent stability continues. Regular meeting attendance and positive mood trends. No concerning indicators this week.',
			'Jessica Thompson': 'Mixed week with some anxiety around midterm exams. Increased chat activity shows good help-seeking behavior. Monitor stress levels.',
			'Robert Williams': 'Steady progress with improved mood diary consistency. Medication adherence good. Consider increasing social activities.'
		};
		return summaries[patient.name] || 'Weekly summary not available.';
	}
	
	function togglePatientDetail(patient) {
		if (expandedPatient?.name === patient.name) {
			expandedPatient = null;
		} else {
			expandedPatient = patient;
		}
	}
</script>

<svelte:head>
	<title>Dashboard - JuliaHealth Clinician Portal</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	<!-- Header -->
	<div class="bg-white border-b border-gray-200">
		<div class="px-6 py-6">
			{#if $authStore.user}
				<div class="flex items-center justify-between">
					<div>
						<h1 class="text-2xl font-semibold text-gray-900">
							Welcome back, {$authStore.user.name.split(' ')[0]}
						</h1>
						<p class="mt-1 text-sm text-gray-600">
							{$authStore.user.department} • Monitor your patients' recovery progress
						</p>
					</div>
					<div class="text-right">
						<div class="text-sm text-gray-500">Clinician ID</div>
						<div class="text-sm font-medium text-gray-900">{$authStore.user.clinicianId}</div>
					</div>
				</div>
			{:else}
				<h1 class="text-2xl font-semibold text-gray-900">Patient Overview</h1>
				<p class="mt-1 text-sm text-gray-600">Monitor your patients' recovery progress</p>
			{/if}
		</div>
	</div>

	<!-- Summary Stats -->
	<div class="px-6 py-6">
		<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.summary.totalPatients}</div>
				<div class="text-sm text-gray-600">Total Patients</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.summary.avgRisk.toFixed(2)}</div>
				<div class="text-sm text-gray-600">Average Risk Score</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.summary.highRiskCount}</div>
				<div class="text-sm text-gray-600">Patients Need Attention</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.chatStats.reduce((sum, stat) => sum + stat.totalChats, 0)}</div>
				<div class="text-sm text-gray-600">Messages This Week</div>
			</div>
		</div>

		<!-- Patient List -->
		<div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
			<div class="px-6 py-4 border-b border-gray-200">
				<h2 class="text-lg font-medium text-gray-900">Patients</h2>
			</div>
			
			<div class="divide-y divide-gray-200">
				{#each data.patients as patient}
					<!-- Patient Row -->
					<div class="transition-colors">
						<div 
							class="px-6 py-4 hover:bg-gray-50 cursor-pointer"
							on:click={() => togglePatientDetail(patient)}
							on:keydown={(e) => e.key === 'Enter' && togglePatientDetail(patient)}
							role="button"
							tabindex="0"
						>
							<div class="flex items-center justify-between">
								<div class="flex items-center space-x-4">
									<!-- Avatar -->
									<div class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
										<span class="text-sm font-medium text-gray-700">
											{patient.name.split(' ').map(n => n[0]).join('')}
										</span>
									</div>
									
									<!-- Patient Info -->
									<div class="flex-1">
										<div class="flex items-center space-x-3">
											<h3 class="text-sm font-medium text-gray-900">{patient.name}</h3>
											<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getRiskBadgeColor(patient.currentRisk)}">
												{getRiskLabel(patient.currentRisk)}
											</span>
										</div>
										<div class="mt-1 flex items-center space-x-4 text-xs text-gray-500">
											<span>{patient.daysSober} days sober</span>
											<span>•</span>
											<span>Risk: {(patient.currentRisk * 100).toFixed(0)}%</span>
											<span>•</span>
											<span>Last update: {formatDate(patient.lastUpdate)}</span>
										</div>
									</div>
								</div>
								
								<!-- Quick Stats -->
								<div class="flex items-center space-x-6 text-sm">
									<div class="text-center">
										<div class="font-medium text-gray-900">{data.chatStats.find(s => s.name === patient.name)?.totalChats || 0}</div>
										<div class="text-xs text-gray-500">Messages</div>
									</div>
									<div class="text-center">
										<div class="font-medium text-gray-900">{(patient.currentRisk * 100).toFixed(0)}%</div>
										<div class="text-xs text-gray-500">Risk</div>
									</div>
									<div class="text-center">
										<div class="font-medium text-gray-900">{patient.daysSober}</div>
										<div class="text-xs text-gray-500">Days</div>
									</div>
									<svg 
										class="h-5 w-5 text-gray-400 transition-transform duration-200 {expandedPatient?.name === patient.name ? 'rotate-90' : ''}" 
										fill="none" 
										viewBox="0 0 24 24" 
										stroke-width="1.5" 
										stroke="currentColor"
									>
										<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
									</svg>
								</div>
							</div>
						</div>

						<!-- Expanded Patient Details -->
						{#if expandedPatient?.name === patient.name}
							<div class="px-6 pb-6 bg-gray-50 border-t border-gray-200">
								<div class="pt-6">
									<!-- Detailed Patient Information -->
									<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
										<!-- Recovery Status -->
										<div class="space-y-4">
											<h4 class="text-sm font-semibold text-gray-900 uppercase tracking-wide">Recovery Status</h4>
											
											<div class="space-y-3">
												<div class="bg-white rounded-lg p-4 border border-gray-200">
													<div class="flex items-center justify-between mb-2">
														<span class="text-sm font-medium text-gray-700">Days Sober</span>
														<span class="text-xl font-bold text-gray-900">{patient.daysSober}</span>
													</div>
													<div class="flex items-center justify-between mb-2">
														<span class="text-sm font-medium text-gray-700">Risk Level</span>
														<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getRiskBadgeColor(patient.currentRisk)}">
															{getRiskLabel(patient.currentRisk)} ({(patient.currentRisk * 100).toFixed(1)}%)
														</span>
													</div>
													<div class="flex items-center justify-between">
														<span class="text-sm font-medium text-gray-700">Last Update</span>
														<span class="text-sm text-gray-600">{formatDate(patient.lastUpdate)}</span>
													</div>
												</div>
											</div>
										</div>
										
										<!-- Biometrics & Mental Health -->
										<div class="space-y-4">
											<h4 class="text-sm font-semibold text-gray-900 uppercase tracking-wide">Health Metrics</h4>
											
											<div class="bg-white rounded-lg p-4 border border-gray-200">
												<div class="space-y-3 text-sm">
													<div class="flex justify-between">
														<span class="text-gray-600">Stress Level</span>
														<span class="font-medium text-gray-900">{patient.currentStress?.toFixed(1) || 'N/A'}</span>
													</div>
													<div class="flex justify-between">
														<span class="text-gray-600">Heart Rate</span>
														<span class="font-medium text-gray-900">{patient.restingHR?.toFixed(0) || 'N/A'} bpm</span>
													</div>
													<div class="flex justify-between">
														<span class="text-gray-600">Sleep</span>
														<span class="font-medium text-gray-900">{patient.sleepHours?.toFixed(1) || 'N/A'} hrs</span>
													</div>
													<div class="flex justify-between">
														<span class="text-gray-600">Mood</span>
														<span class="font-medium text-gray-900">{patient.currentMood?.toFixed(1) || 'N/A'}/10</span>
													</div>
													<div class="flex justify-between">
														<span class="text-gray-600">Anxiety</span>
														<span class="font-medium text-gray-900">{patient.currentAnxiety?.toFixed(1) || 'N/A'}/10</span>
													</div>
													<div class="flex justify-between">
														<span class="text-gray-600">PHQ-5</span>
														<span class="font-medium text-gray-900">{patient.phq5Score !== null ? patient.phq5Score : 'N/A'}</span>
													</div>
												</div>
											</div>
										</div>
										
										<!-- Engagement -->
										<div class="space-y-4">
											<h4 class="text-sm font-semibold text-gray-900 uppercase tracking-wide">Engagement</h4>
											
											<div class="bg-white rounded-lg p-4 border border-gray-200">
												<div class="space-y-3">
													<div class="flex items-center justify-between">
														<span class="text-sm font-medium text-gray-700">Messages This Week</span>
														<span class="text-lg font-semibold text-gray-900">
															{data.chatStats.find(s => s.name === patient.name)?.totalChats || 0}
														</span>
													</div>
													<div class="flex items-center justify-between">
														<span class="text-sm font-medium text-gray-700">Sentiment</span>
														<span class="text-sm text-gray-600">
															{(data.chatStats.find(s => s.name === patient.name)?.avgSentiment || 0).toFixed(2)}
														</span>
													</div>
													<div class="flex items-center justify-between">
														<span class="text-sm font-medium text-gray-700">Crisis Alerts</span>
														<span class="text-sm {data.chatStats.find(s => s.name === patient.name)?.crisisIndicators > 0 ? 'text-red-600' : 'text-green-600'}">
															{data.chatStats.find(s => s.name === patient.name)?.crisisIndicators || 0}
														</span>
													</div>
												</div>
											</div>
										</div>
									</div>
									
									<!-- AI Summary -->
									<div class="mt-6">
										<h4 class="text-sm font-semibold text-gray-900 uppercase tracking-wide mb-3">AI Weekly Summary</h4>
										<div class="bg-blue-50 rounded-lg p-4 border border-blue-200">
											<div class="flex items-start space-x-3">
												<div class="h-6 w-6 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0 mt-0.5">
													<svg class="h-3 w-3 text-blue-600" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
														<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09z" />
													</svg>
												</div>
												<p class="text-sm text-blue-900">{getWeeklySummary(patient)}</p>
											</div>
										</div>
									</div>
									
									<!-- Action Buttons -->
									<div class="mt-6 flex flex-wrap gap-3">
										<button class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
											Send Message
										</button>
										<button class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
											View Full History
										</button>
										<button class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
											Update Treatment Plan
										</button>
										{#if patient.currentRisk >= 0.8}
											<button class="bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">
												Emergency Protocol
											</button>
										{/if}
									</div>
								</div>
							</div>
						{/if}
					</div>
				{/each}
			</div>
		</div>

		<!-- AI Weekly Summaries -->
		<div class="mt-8 bg-white rounded-lg border border-gray-200">
			<div class="px-6 py-4 border-b border-gray-200">
				<h2 class="text-lg font-medium text-gray-900">AI Weekly Insights</h2>
				<p class="text-sm text-gray-600">Automated analysis of patient progress and recommendations</p>
			</div>
			
			<div class="p-6 space-y-4">
				{#each data.patients as patient}
					<div class="border border-gray-200 rounded-lg p-4">
						<div class="flex items-start space-x-3">
							<div class="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
								<svg class="h-4 w-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09z" />
								</svg>
							</div>
							<div class="flex-1">
								<div class="flex items-center space-x-2 mb-2">
									<h3 class="text-sm font-medium text-gray-900">{patient.name}</h3>
									<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getRiskBadgeColor(patient.currentRisk)}">
										{getRiskLabel(patient.currentRisk)}
									</span>
								</div>
								<p class="text-sm text-gray-700">{getWeeklySummary(patient)}</p>
								<div class="mt-2 flex items-center space-x-4 text-xs text-gray-500">
									<span>Generated by AI</span>
									<span>•</span>
									<span>Based on 7-day analysis</span>
									<span>•</span>
									<span>Last updated: Today</span>
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>
