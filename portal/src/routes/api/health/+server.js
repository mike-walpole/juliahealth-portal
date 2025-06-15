import { db } from '$lib/db/connection.js';
import { personas } from '$lib/db/schema.js';
import { json } from '@sveltejs/kit';

export async function GET() {
	try {
		// Simple query to test database connection
		await db.select().from(personas).limit(1);
		
		return json({
			status: 'healthy',
			database: 'connected',
			timestamp: new Date().toISOString()
		});
	} catch (error) {
		console.error('Health check failed:', error);
		
		return json({
			status: 'error',
			database: 'disconnected',
			error: error.message,
			timestamp: new Date().toISOString()
		}, { status: 500 });
	}
} 