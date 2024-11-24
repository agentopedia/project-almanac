// pages/api/submit-form.ts
// import type { NextRequest, NextResponse } from 'next';
import {NextRequest, NextResponse } from 'next/server';

let lastMessage = null; // in-memory storage

export async function POST(req: NextRequest) {
  if (req.method == 'POST') {
    const {query} = await req.json();
    // console.log(query);
    const flaskResponse = await fetch('http://localhost:5000/design_input', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ query })}); //test
    // return NextResponse.json({"message": "Form submitted successfully"}, {"status": 200})
    if (!flaskResponse.ok) {
      return NextResponse.json({ message: 'Error from Flask server' }, { status: flaskResponse.status });
    }

    const data = await flaskResponse.json();
    lastMessage = data.result; // store last message in memory
    return NextResponse.json({ message: 'Form submitted successfully', result: data.result }, { status: 200 });
  } 
}