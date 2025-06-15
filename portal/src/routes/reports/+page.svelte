<script>
	let selectedReportType = 'patient-summary';
	let selectedFormat = 'pdf';
	let dateRange = '30';
	let selectedPatients = [];
	let isGenerating = false;
	
	const reportTypes = [
		{ id: 'patient-summary', name: 'Patient Summary Report', description: 'Comprehensive overview of patient progress and metrics' },
		{ id: 'risk-analysis', name: 'Risk Analysis Report', description: 'Detailed risk assessment and trend analysis' },
		{ id: 'engagement-metrics', name: 'Engagement Metrics', description: 'Communication and app usage statistics' },
		{ id: 'clinical-outcomes', name: 'Clinical Outcomes', description: 'Treatment effectiveness and recovery milestones' },
		{ id: 'compliance-report', name: 'Compliance Report', description: 'Medication adherence and appointment attendance' }
	];
	
	const exportFormats = [
		{ id: 'pdf', name: 'PDF Document', icon: '📄' },
		{ id: 'csv', name: 'CSV Spreadsheet', icon: '📊' },
		{ id: 'excel', name: 'Excel Workbook', icon: '📈' },
		{ id: 'json', name: 'JSON Data', icon: '💾' }
	];
	
	const dateRanges = [
		{ id: '7', name: 'Last 7 days' },
		{ id: '30', name: 'Last 30 days' },
		{ id: '90', name: 'Last 3 months' },
		{ id: '365', name: 'Last year' },
		{ id: 'custom', name: 'Custom range' }
	];
	
	async function generateReport() {
		isGenerating = true;
		
		// Simulate report generation
		await new Promise(resolve => setTimeout(resolve, 2000));
		
		// In a real app, this would make an API call to generate the report
		console.log('Generating report:', {
			type: selectedReportType,
			format: selectedFormat,
			dateRange,
			patients: selectedPatients
		});
		
		isGenerating = false;
		
		// Show success message or download file
		alert('Report generated successfully!');
	}
	
	function togglePatientSelection(patientId) {
		if (selectedPatients.includes(patientId)) {
			selectedPatients = selectedPatients.filter(id => id !== patientId);
		} else {
			selectedPatients = [...selectedPatients, patientId];
		}
	}
</script>

<svelte:head>
	<title>Reports - JuliaHealth Clinician Portal</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	<!-- Header -->
	<div class="bg-white border-b border-gray-200">
		<div class="px-6 py-6">
			<h1 class="text-2xl font-semibold text-gray-900">Reports & Analytics</h1>
			<p class="mt-1 text-sm text-gray-600">Generate comprehensive reports for clinical analysis</p>
		</div>
	</div>

	<!-- Content -->
	<div class="px-6 py-6">
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Report Configuration -->
			<div class="lg:col-span-2 space-y-6">
				<!-- Report Type Selection -->
				<div class="bg-white rounded-lg border border-gray-200">
					<div class="px-6 py-4 border-b border-gray-200">
						<h2 class="text-lg font-medium text-gray-900">Report Type</h2>
						<p class="text-sm text-gray-600">Choose the type of report to generate</p>
					</div>
					<div class="p-6">
						<div class="space-y-3">
							{#each reportTypes as reportType}
								<label class="flex items-start space-x-3 p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors {selectedReportType === reportType.id ? 'border-blue-500 bg-blue-50' : ''}">
									<input
										type="radio"
										bind:group={selectedReportType}
										value={reportType.id}
										class="mt-1 text-blue-600 focus:ring-blue-500"
									/>
									<div class="flex-1">
										<h3 class="text-sm font-medium text-gray-900">{reportType.name}</h3>
										<p class="text-sm text-gray-600 mt-1">{reportType.description}</p>
									</div>
								</label>
							{/each}
						</div>
					</div>
				</div>

				<!-- Export Format -->
				<div class="bg-white rounded-lg border border-gray-200">
					<div class="px-6 py-4 border-b border-gray-200">
						<h2 class="text-lg font-medium text-gray-900">Export Format</h2>
						<p class="text-sm text-gray-600">Select your preferred file format</p>
					</div>
					<div class="p-6">
						<div class="grid grid-cols-2 md:grid-cols-4 gap-3">
							{#each exportFormats as format}
								<label class="flex flex-col items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors {selectedFormat === format.id ? 'border-blue-500 bg-blue-50' : ''}">
									<input
										type="radio"
										bind:group={selectedFormat}
										value={format.id}
										class="sr-only"
									/>
									<div class="text-2xl mb-2">{format.icon}</div>
									<span class="text-sm font-medium text-gray-900">{format.name}</span>
								</label>
							{/each}
						</div>
					</div>
				</div>

				<!-- Date Range -->
				<div class="bg-white rounded-lg border border-gray-200">
					<div class="px-6 py-4 border-b border-gray-200">
						<h2 class="text-lg font-medium text-gray-900">Date Range</h2>
						<p class="text-sm text-gray-600">Specify the time period for your report</p>
					</div>
					<div class="p-6">
						<div class="grid grid-cols-1 md:grid-cols-3 gap-3">
							{#each dateRanges as range}
								<label class="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors {dateRange === range.id ? 'border-blue-500 bg-blue-50' : ''}">
									<input
										type="radio"
										bind:group={dateRange}
										value={range.id}
										class="text-blue-600 focus:ring-blue-500 mr-3"
									/>
									<span class="text-sm font-medium text-gray-900">{range.name}</span>
								</label>
							{/each}
						</div>
						
						{#if dateRange === 'custom'}
							<div class="mt-4 grid grid-cols-2 gap-4">
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
									<input
										type="date"
										class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
									/>
								</div>
								<div>
									<label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
									<input
										type="date"
										class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
									/>
								</div>
							</div>
						{/if}
					</div>
				</div>
			</div>

			<!-- Report Preview & Actions -->
			<div class="space-y-6">
				<!-- Quick Stats -->
				<div class="bg-white rounded-lg border border-gray-200">
					<div class="px-6 py-4 border-b border-gray-200">
						<h2 class="text-lg font-medium text-gray-900">Report Preview</h2>
					</div>
					<div class="p-6">
						<div class="space-y-4">
							<div class="flex justify-between items-center">
								<span class="text-sm text-gray-600">Report Type</span>
								<span class="text-sm font-medium text-gray-900">
									{reportTypes.find(r => r.id === selectedReportType)?.name}
								</span>
							</div>
							<div class="flex justify-between items-center">
								<span class="text-sm text-gray-600">Format</span>
								<span class="text-sm font-medium text-gray-900">
									{exportFormats.find(f => f.id === selectedFormat)?.name}
								</span>
							</div>
							<div class="flex justify-between items-center">
								<span class="text-sm text-gray-600">Date Range</span>
								<span class="text-sm font-medium text-gray-900">
									{dateRanges.find(d => d.id === dateRange)?.name}
								</span>
							</div>
							<div class="flex justify-between items-center">
								<span class="text-sm text-gray-600">Patients</span>
								<span class="text-sm font-medium text-gray-900">
									{selectedPatients.length > 0 ? `${selectedPatients.length} selected` : 'All patients'}
								</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Generate Report -->
				<div class="bg-white rounded-lg border border-gray-200">
					<div class="p-6">
						<button
							on:click={generateReport}
							disabled={isGenerating}
							class="w-full bg-blue-600 text-white px-4 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
						>
							{#if isGenerating}
								<div class="flex items-center justify-center">
									<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
										<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
										<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
									</svg>
									Generating Report...
								</div>
							{:else}
								Generate Report
							{/if}
						</button>
						
						<div class="mt-4 text-center">
							<p class="text-xs text-gray-500">
								Reports are generated securely and comply with HIPAA regulations
							</p>
						</div>
					</div>
				</div>

				<!-- Recent Reports -->
				<div class="bg-white rounded-lg border border-gray-200">
					<div class="px-6 py-4 border-b border-gray-200">
						<h2 class="text-lg font-medium text-gray-900">Recent Reports</h2>
					</div>
					<div class="p-6">
						<div class="space-y-3">
							<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
								<div>
									<h3 class="text-sm font-medium text-gray-900">Patient Summary</h3>
									<p class="text-xs text-gray-600">Generated 2 hours ago</p>
								</div>
								<button class="text-blue-600 hover:text-blue-700 text-sm font-medium">
									Download
								</button>
							</div>
							<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
								<div>
									<h3 class="text-sm font-medium text-gray-900">Risk Analysis</h3>
									<p class="text-xs text-gray-600">Generated yesterday</p>
								</div>
								<button class="text-blue-600 hover:text-blue-700 text-sm font-medium">
									Download
								</button>
							</div>
							<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
								<div>
									<h3 class="text-sm font-medium text-gray-900">Engagement Metrics</h3>
									<p class="text-xs text-gray-600">Generated 3 days ago</p>
								</div>
								<button class="text-blue-600 hover:text-blue-700 text-sm font-medium">
									Download
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Advanced Options -->
		<div class="mt-6 bg-white rounded-lg border border-gray-200">
			<div class="px-6 py-4 border-b border-gray-200">
				<h2 class="text-lg font-medium text-gray-900">Advanced Options</h2>
				<p class="text-sm text-gray-600">Customize your report with additional settings</p>
			</div>
			<div class="p-6">
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
					<div>
						<h3 class="text-sm font-medium text-gray-900 mb-3">Include Sections</h3>
						<div class="space-y-2">
							<label class="flex items-center">
								<input type="checkbox" checked class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Executive Summary</span>
							</label>
							<label class="flex items-center">
								<input type="checkbox" checked class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Patient Demographics</span>
							</label>
							<label class="flex items-center">
								<input type="checkbox" checked class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Risk Analysis</span>
							</label>
							<label class="flex items-center">
								<input type="checkbox" class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Detailed Charts</span>
							</label>
						</div>
					</div>
					
					<div>
						<h3 class="text-sm font-medium text-gray-900 mb-3">Data Privacy</h3>
						<div class="space-y-2">
							<label class="flex items-center">
								<input type="checkbox" checked class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Anonymize patient names</span>
							</label>
							<label class="flex items-center">
								<input type="checkbox" class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Exclude sensitive data</span>
							</label>
							<label class="flex items-center">
								<input type="checkbox" checked class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">HIPAA compliant format</span>
							</label>
						</div>
					</div>
					
					<div>
						<h3 class="text-sm font-medium text-gray-900 mb-3">Delivery Options</h3>
						<div class="space-y-2">
							<label class="flex items-center">
								<input type="radio" name="delivery" checked class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Download immediately</span>
							</label>
							<label class="flex items-center">
								<input type="radio" name="delivery" class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Email when ready</span>
							</label>
							<label class="flex items-center">
								<input type="radio" name="delivery" class="text-blue-600 focus:ring-blue-500 mr-2" />
								<span class="text-sm text-gray-700">Schedule for later</span>
							</label>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div> 