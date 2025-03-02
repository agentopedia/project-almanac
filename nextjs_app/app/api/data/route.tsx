import {NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const dataFilePath = path.join(process.cwd(), 'data', 'lastMessage.json'); // data/lastMessage.json is where the info is being stored

function getLastMessageFromFile() {
  try {
    const data = fs.readFileSync(dataFilePath, 'utf-8');
    return JSON.parse(data); //so this data.result becomes a json
  } catch (error) {
    console.error("Error reading message:", error);
    return null;
  }
}

export function GET() {
  const lastMessage = getLastMessageFromFile();
  return NextResponse.json({ result: lastMessage }); //put a json in another json
}
