"use client"

import Link from "next/link";
import { usePathname } from "next/navigation";
import './styles/agents.css';

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const pathname = usePathname();
  const isGeneratedMVP = pathname === "/generatedmvp";

  return (
    <html lang="en">
      <body className={isGeneratedMVP ? "generatedmvp-body" : "min-h-screen"}>
        {/* Navbar hidden for generatedMVP */}
        {!isGeneratedMVP && (
          <header className="navbar">
            <nav className="navbar-links">
              <Link href="/">Home</Link>
              <Link href="/about">About</Link>
              <Link href="/agents">Agents</Link>
            </nav>
          </header>
        )}
        <div className={isGeneratedMVP ? "generatedmvp-container" : "container min-h-screen flex flex-col justify-center items-center"}>
          {children}
        </div>
      </body>
    </html>
  );
}