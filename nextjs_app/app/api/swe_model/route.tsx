// /api/swe_model/route.tsx
import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const dataFilePath = path.join(process.cwd(), 'data', 'sweOutput.json');

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

function saveSweOutput(data: any) {
  try {
    fs.writeFileSync(dataFilePath, JSON.stringify(data, null, 2));
  } catch (error) {
    console.error("Error saving SWE output:", error);
  }
}

function getSweOutputFromFile() {
  try {
    if (fs.existsSync(dataFilePath)) {
      const data = fs.readFileSync(dataFilePath, 'utf-8');
      return JSON.parse(data);
    }
    return null;
  } catch (error) {
    console.error("Error reading SWE output:", error);
    return null;
  }
}

export async function POST(req: NextRequest) {
  try {
    const { action, data } = await req.json();
    const port = getAlmanacPortFromFile();
    
    if (!port) {
      return NextResponse.json({ error: "Could not determine Flask port" }, { status: 500 });
    }

    // Different actions the SWE agent can perform
    switch (action) {
      case 'generate':
        // Generate product UI based on PRD
        const flaskResponse = await fetch(`http://localhost:${port}/generate_mvp`, {
          method: 'GET'
        });
        
        if (!flaskResponse.ok) {
          return NextResponse.json(
            { error: 'Error from Flask server' }, 
            { status: flaskResponse.status }
          );
        }
        
        const responseData = await flaskResponse.json();
        saveSweOutput(responseData.result);
        return NextResponse.json({ 
          message: 'SWE agent generated product successfully', 
          result: responseData.result 
        });
        
      case 'customize':
        // Customize existing product (for future implementation)
        if (!data) {
          return NextResponse.json({ error: "No customization data provided" }, { status: 400 });
        }
        
        // This would call a customization endpoint on the Flask backend
        // For now, we'll just save the customized data
        saveSweOutput(data);
        return NextResponse.json({ 
          message: 'Product customized successfully', 
          result: data 
        });
        
      default:
        return NextResponse.json({ error: "Unknown action" }, { status: 400 });
    }
  } catch (error) {
    console.error("Error in SWE agent API:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

export async function GET() {
  const sweOutput = getSweOutputFromFile();
  
  if (!sweOutput) {
    // If no SWE output exists yet, trigger the Flask endpoint to generate it
    try {
      const port = getAlmanacPortFromFile();
      if (!port) {
        return NextResponse.json({ error: "Could not determine Flask port" }, { status: 500 });
      }
      
      const flaskResponse = await fetch(`http://localhost:${port}/swe_model`, {
        method: 'GET'
      });
      
      if (!flaskResponse.ok) {
        return NextResponse.json(
          { error: 'Error from Flask server' }, 
          { status: flaskResponse.status }
        );
      }
      
      const responseData = await flaskResponse.json();
      saveSweOutput(responseData.result);
      return NextResponse.json({ result: responseData.result });
    } catch (error) {
      console.error("Error fetching from Flask:", error);
      return NextResponse.json({ error: "Could not generate SWE output" }, { status: 500 });
    }
  }
  
  return NextResponse.json({ result: sweOutput });
}