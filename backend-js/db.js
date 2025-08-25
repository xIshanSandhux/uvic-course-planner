import postgres from 'postgres';

/* 
    creating sql connection with the supabase url 
    and exporting it for other files to use.
*/
const connectionString = process.env.DATABASE_URL;
if(!connectionString){
    throw new Error("DATABASE_URL is not set");
}
export const sql = postgres(connectionString);
