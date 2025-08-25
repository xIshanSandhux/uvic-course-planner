import { sql } from "../db.js";

export const extractCourses = async (req, res) =>{
    const { major } = req.body;

    if(!major){
        return res.status(400).json({ error: "Major is required" });
    }
    try{
        const major = await sql`SELECT * FROM majors WHERE major = ${major}`;
        const reqMajor = major[0];
        
    }
    catch{
        return res.status(500).json({ error: "Internal server error" });
    }
}