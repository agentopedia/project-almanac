import { NextResponse } from "next/server";

export async function GET() {
    // Forward the GET request to the Flask server 
    console.log("in backtracking route")
    const flaskResponse = await fetch("http://localhost:5000/design_backtracking", {method: "GET"});
    console.log("Done fetching response");
    console.log(flaskResponse)
    if (!flaskResponse.ok) {
        return NextResponse.json({ message: 'Error from Flask server' }, { status: flaskResponse.status });
    }

    const data = await flaskResponse.json();

    // Return the response to the client
    return NextResponse.json(data);
}
