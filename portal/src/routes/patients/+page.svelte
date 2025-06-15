<script>
	export let data;
	
	let selectedPatient = null;
	
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
	
	function getStatusColor(status) {
		if (status === 'Active Treatment') return 'bg-blue-100 text-blue-800';
		if (status === 'Maintenance') return 'bg-green-100 text-green-800';
		if (status === 'At Risk') return 'bg-amber-100 text-amber-800';
		return 'bg-gray-100 text-gray-800';
	}
	
	function getTreatmentStatus(patient) {
		if (!patient.inTreatment) return 'Inactive';
		if (patient.currentRisk >= 0.6) return 'At Risk';
		if (patient.medicationAdherence >= 0.8 && patient.meetingAttendance >= 3) return 'Maintenance';
		return 'Active Treatment';
	}
	
	function formatDate(dateStr) {
		return new Date(dateStr).toLocaleDateString();
	}
	
	function openPatientDetail(patient) {
		selectedPatient = patient;
	}
	
	function closePatientDetail() {
		selectedPatient = null;
	}
</script>

<svelte:head>
	<title>Patients - JuliaHealth Clinician Portal</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	<!-- Header -->
	<div class="bg-white border-b border-gray-200">
		<div class="px-6 py-6">
			<h1 class="text-2xl font-semibold text-gray-900">Patient Management</h1>
			<p class="mt-1 text-sm text-gray-600">Comprehensive view of all patients in your care</p>
		</div>
	</div>

	<!-- Content -->
	<div class="px-6 py-6">
		<!-- Summary Stats -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">{data.patients.length}</div>
				<div class="text-sm text-gray-600">Total Patients</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">
					{data.patients.filter(p => getTreatmentStatus(p) === 'Active Treatment').length}
				</div>
				<div class="text-sm text-gray-600">Active Treatment</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">
					{data.patients.filter(p => p.currentRisk >= 0.6).length}
				</div>
				<div class="text-sm text-gray-600">Need Attention</div>
			</div>
			<div class="bg-white rounded-lg p-4 border border-gray-200">
				<div class="text-2xl font-semibold text-gray-900">
					{Math.round(data.patients.reduce((sum, p) => sum + p.daysSober, 0) / data.patients.length)}
				</div>
				<div class="text-sm text-gray-600">Avg Days Sober</div>
			</div>
		</div>

		<!-- Patient Grid -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
			{#each data.patients as patient}
				<div class="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-sm transition-shadow cursor-pointer"
					 on:click={() => openPatientDetail(patient)}
					 on:keydown={(e) => e.key === 'Enter' && openPatientDetail(patient)}
					 role="button"
					 tabindex="0">
					
					<!-- Patient Header -->
					<div class="flex items-start justify-between mb-4">
						<div class="flex items-center space-x-3">
							<div class="h-12 w-12 rounded-full bg-gray-200 flex items-center justify-center">
								<span class="text-lg font-medium text-gray-700">
									{patient.name.split(' ').map(n => n[0]).join('')}
								</span>
							</div>
							<div>
								<h3 class="text-lg font-medium text-gray-900">{patient.name}</h3>
								<div class="flex items-center space-x-2 mt-1">
									<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getRiskBadgeColor(patient.currentRisk)}">
										{getRiskLabel(patient.currentRisk)}
									</span>
									<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getStatusColor(getTreatmentStatus(patient))}">
										{getTreatmentStatus(patient)}
									</span>
								</div>
							</div>
						</div>
						<svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
						</svg>
					</div>

					<!-- Recovery Stats -->
					<div class="grid grid-cols-2 gap-4 mb-4">
						<div class="text-center p-3 bg-gray-50 rounded-lg">
							<div class="text-2xl font-bold text-gray-900">{patient.daysSober}</div>
							<div class="text-xs text-gray-600">Days Sober</div>
						</div>
						<div class="text-center p-3 bg-gray-50 rounded-lg">
							<div class="text-2xl font-bold text-gray-900">{(patient.currentRisk * 100).toFixed(0)}%</div>
							<div class="text-xs text-gray-600">Risk Score</div>
						</div>
					</div>

					<!-- Biometric Data -->
					<div class="space-y-3 mb-4">
						<h4 class="text-sm font-medium text-gray-900">Recent Biometrics</h4>
						<div class="grid grid-cols-2 gap-3 text-sm">
							<div class="flex justify-between">
								<span class="text-gray-600">Stress Level</span>
								<span class="font-medium text-gray-900">{patient.currentStress?.toFixed(1) || 'N/A'}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Heart Rate</span>
								<span class="font-medium text-gray-900">{patient.restingHR?.toFixed(0) || 'N/A'} bpm</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">HRV</span>
								<span class="font-medium text-gray-900">{patient.hrv?.toFixed(0) || 'N/A'} ms</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Sleep</span>
								<span class="font-medium text-gray-900">{patient.sleepHours?.toFixed(1) || 'N/A'} hrs</span>
							</div>
						</div>
					</div>

					<!-- Mental Health -->
					<div class="space-y-3 mb-4">
						<h4 class="text-sm font-medium text-gray-900">Mental Health</h4>
						<div class="grid grid-cols-2 gap-3 text-sm">
							<div class="flex justify-between">
								<span class="text-gray-600">Mood</span>
								<span class="font-medium text-gray-900">{patient.currentMood?.toFixed(1) || 'N/A'}/10</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Anxiety</span>
								<span class="font-medium text-gray-900">{patient.currentAnxiety?.toFixed(1) || 'N/A'}/10</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Cravings</span>
								<span class="font-medium text-gray-900">{patient.currentCravings?.toFixed(1) || 'N/A'}/10</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">PHQ-5</span>
								<span class="font-medium text-gray-900">{patient.phq5Score !== null ? patient.phq5Score : 'N/A'}</span>
							</div>
						</div>
					</div>

					<!-- Engagement -->
					<div class="flex items-center justify-between pt-3 border-t border-gray-200">
						<div class="flex items-center space-x-4 text-sm text-gray-600">
							<span>{patient.totalChats || 0} messages</span>
							<span>•</span>
							<span>Last update: {formatDate(patient.lastUpdate)}</span>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
</div>

<!-- Patient Detail Modal -->
{#if selectedPatient}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
		<div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
			<!-- Modal Header -->
			<div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
				<div>
					<h2 class="text-xl font-semibold text-gray-900">{selectedPatient.name}</h2>
					<p class="text-sm text-gray-600">Complete patient profile</p>
				</div>
				<button 
					on:click={closePatientDetail}
					class="text-gray-400 hover:text-gray-600"
				>
					<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>
			
			<!-- Modal Content -->
			<div class="p-6">
				<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
					<!-- Recovery Overview -->
					<div class="space-y-4">
						<h3 class="text-lg font-medium text-gray-900">Recovery Overview</h3>
						<div class="space-y-3">
							<div class="bg-gray-50 rounded-lg p-4">
								<div class="text-2xl font-bold text-gray-900">{selectedPatient.daysSober}</div>
								<div class="text-sm text-gray-600">Days Sober</div>
							</div>
							<div class="bg-gray-50 rounded-lg p-4">
								<div class="flex items-center justify-between">
									<span class="text-sm font-medium text-gray-700">Risk Level</span>
									<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {getRiskBadgeColor(selectedPatient.currentRisk)}">
										{getRiskLabel(selectedPatient.currentRisk)}
									</span>
								</div>
								<div class="text-lg font-semibold text-gray-900 mt-1">{(selectedPatient.currentRisk * 100).toFixed(1)}%</div>
							</div>
						</div>
					</div>
					
					<!-- Biometrics -->
					<div class="space-y-4">
						<h3 class="text-lg font-medium text-gray-900">Biometric Data</h3>
						<div class="space-y-3">
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<span class="text-sm font-medium text-gray-700">Stress Level</span>
								<span class="text-lg font-semibold text-gray-900">{selectedPatient.currentStress?.toFixed(1) || 'N/A'}</span>
							</div>
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<span class="text-sm font-medium text-gray-700">Heart Rate</span>
								<span class="text-lg font-semibold text-gray-900">{selectedPatient.restingHR?.toFixed(0) || 'N/A'} bpm</span>
							</div>
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<span class="text-sm font-medium text-gray-700">HRV</span>
								<span class="text-lg font-semibold text-gray-900">{selectedPatient.hrv?.toFixed(0) || 'N/A'} ms</span>
							</div>
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<span class="text-sm font-medium text-gray-700">Sleep</span>
								<span class="text-lg font-semibold text-gray-900">{selectedPatient.sleepHours?.toFixed(1) || 'N/A'} hrs</span>
							</div>
						</div>
					</div>
					
					<!-- Mental Health -->
					<div class="space-y-4">
						<h3 class="text-lg font-medium text-gray-900">Mental Health</h3>
						<div class="space-y-3">
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<span class="text-sm font-medium text-gray-700">Mood Rating</span>
								<span class="text-lg font-semibold text-gray-900">{selectedPatient.currentMood?.toFixed(1) || 'N/A'}/10</span>
							</div>
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<span class="text-sm font-medium text-gray-700">Anxiety Level</span>
								<span class="text-lg font-semibold text-gray-900">{selectedPatient.currentAnxiety?.toFixed(1) || 'N/A'}/10</span>
							</div>
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<span class="text-sm font-medium text-gray-700">Craving Intensity</span>
								<span class="text-lg font-semibold text-gray-900">{selectedPatient.currentCravings?.toFixed(1) || 'N/A'}/10</span>
							</div>
							<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
								<span class="text-sm font-medium text-gray-700">PHQ-5 Score</span>
								<span class="text-lg font-semibold text-gray-900">{selectedPatient.phq5Score !== null ? selectedPatient.phq5Score : 'N/A'}</span>
							</div>
						</div>
					</div>
				</div>
				
				<!-- Action Buttons -->
				<div class="mt-6 flex space-x-3">
					<button class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
						Send Message
					</button>
					<button class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
						View Timeline
					</button>
					<button class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
						Update Treatment Plan
					</button>
					{#if selectedPatient.currentRisk >= 0.8}
						<button class="bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">
							Emergency Protocol
						</button>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/if} 