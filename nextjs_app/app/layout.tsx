"use client"

import "bootstrap/dist/css/bootstrap.min.css";
import InstallBootstrap from "./components/InstallBootstrap";
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
      <body className="min-h-screen">
        {/* conditional navbar */}
        {!isGeneratedMVP && (
          <header className="navbar">
            <nav className="navbar-links">
              <Link href="/">Home</Link>
              <Link href="/about">About</Link>
              <Link href="/agents">Agents</Link>
            </nav>
          </header>
        )}
        <InstallBootstrap />
        <div className="container min-h-screen flex flex-col justify-center items-center">
          {children}
        </div>
      </body>
    </html>
  );
}
