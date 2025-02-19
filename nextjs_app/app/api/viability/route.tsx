import { NextResponse } from "next/server";
import fs from 'fs';
import path from 'path';

function getAlmanacPortFromFile(): string | null {
    try {
      const filePath = path.join(process.cwd(), 'flask_backend', 'flask_port.json');
      const fileData = fs.readFileSync(filePath, 'utf-8');
      const jsonData = JSON.parse(fileData);
      return jsonData.port;
    } catch (error) {
      console.error("Error reading flask_port.json:", error);
      return null;
    }
  }
  

export async function GET() {
    // Forward the GET request to the Flask server 
    // console.log("In viability agent route");
    const port = getAlmanacPortFromFile();
    console.log("Using Flask port:", port);
    const flaskResponse = await fetch(`http://localhost:${port}/viability`, { method: "GET" });

    if (!flaskResponse.ok) {
        return NextResponse.json({ message: 'Error from Flask server' }, { status: flaskResponse.status });
    }

    const data = await flaskResponse.json();

    // Return the response to the client
    return NextResponse.json(data);
}
