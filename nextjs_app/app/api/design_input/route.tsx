// pages/api/submit-form.ts
// import type { NextRequest, NextResponse } from 'next';
import {NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

let lastMessage = null; // in-memory storage

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
    const {query} = await req.json();
    // console.log(query);
    const port = getAlmanacPortFromFile();
    console.log("Using Flask port:", port);
    const flaskResponse = await fetch(`http://localhost:${port}/design_input`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ query })}); //test
    // return NextResponse.json({"message": "Form submitted successfully"}, {"status": 200})
    if (!flaskResponse.ok) {
      return NextResponse.json({ message: 'Error from Flask server' }, { status: flaskResponse.status });
    }

    const data = await flaskResponse.json();
    lastMessage = data.result; // store last message in memory
    return NextResponse.json({ message: 'Form submitted successfully', result: data.result }, { status: 200 });
  } 
}