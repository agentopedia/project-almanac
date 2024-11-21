import { NextResponse } from "next/server";

export async function GET() {
    // Forward the GET request to the Flask server 
    // console.log("In viability agent route");
    const flaskResponse = await fetch("http://localhost:5000/viability", {method: "GET"});
    // console.log("Done fetching response");
    if (!flaskResponse.ok) {
        return NextResponse.json({ message: 'Error from Flask server' }, { status: flaskResponse.status });
    }

    const data = await flaskResponse.json();

    // Return the response to the client
    return NextResponse.json(data);
}
