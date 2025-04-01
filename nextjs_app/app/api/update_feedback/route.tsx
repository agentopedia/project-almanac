import {NextRequest, NextResponse } from 'next/server';
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


export async function POST(req: NextRequest) {
  if (req.method == 'POST') {
    const {feedback} = await req.json();
    const port = getAlmanacPortFromFile();
    const flaskResponse = await fetch(`http://localhost:${port}/update_feedback`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ feedback })}); 
    if (!flaskResponse.ok) {
      return NextResponse.json({ message: 'Error from Flask server' }, { status: flaskResponse.status });
    }

    const data = await flaskResponse.json();
    return NextResponse.json({ message: 'Form submitted successfully' }, { status: 200 });
  }
}