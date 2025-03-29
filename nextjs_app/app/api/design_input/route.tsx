// pages/api/submit-form.ts
// import type { NextRequest, NextResponse } from 'next';
import {NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// const dataFilePath = path.join(process.cwd(), 'data', 'lastMessage.json'); // data/lastMessage.json is where the info is being stored

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

// function saveLastMessage(message: any) {
//   try {
//     fs.writeFileSync(dataFilePath, JSON.stringify(message, null, 2)); //might need to remove stringify
//   } catch (error) {
//     console.error("Error saving message:", error);
//   }
// }


// function getLastMessageFromFile() {
//   try {
//     const data = fs.readFileSync(dataFilePath, 'utf-8');
//     return JSON.parse(data); //so this data.result becomes a json
//   } catch (error) {
//     console.error("Error reading message:", error);
//     return null;
//   }
// }


export async function POST(req: NextRequest) {
  if (req.method == 'POST') {
    const {query} = await req.json();
    const port = getAlmanacPortFromFile();
    console.log("Using Flask port:", port);
    const flaskResponse = await fetch(`http://localhost:${port}/design_input`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ query })}); //test
    if (!flaskResponse.ok) {
      return NextResponse.json({ message: 'Error from Flask server' }, { status: flaskResponse.status });
    }

    const data = await flaskResponse.json();
    console.log('data.result type in api post: ', typeof data.result);
    // saveLastMessage(data.result); not using this anymore
    return NextResponse.json({ message: 'Form submitted successfully', result: data.result }, { status: 200 });
  }
}

export async function GET() {
  // const lastMessage = getLastMessageFromFile();
  // return NextResponse.json({ result: lastMessage }); //put a json in another json
  const port = getAlmanacPortFromFile();
  console.log("Using Flask port:", port);
  const flaskResponse = await fetch(`http://localhost:${port}/design_backtracking`, {method: "GET"});
  if (!flaskResponse.ok) {
    return NextResponse.json({ message: 'Error from Flask server' }, { status: flaskResponse.status });
  }

  const data = await flaskResponse.json();

  // Return the response to the client
  return NextResponse.json({result: data.result});
}
