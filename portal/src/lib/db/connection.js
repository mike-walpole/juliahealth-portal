import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import { DATABASE_URL } from '$env/static/private';

// Create connection
const sql = postgres(DATABASE_URL);
export const db = drizzle(sql);

// Export sql for cleanup if needed
export { sql }; 