import Link from 'next/link';
import './styles/agents.css';

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-start"></div>
      <div className="px-3">
        <Link href="/">Home</Link>
      </div>
      <div className="px-3">
        <Link href="./about">About</Link>
      </div>
      <div className="px-3">
        <Link href="/agents">Agents</Link>
      </div>
    </header>
  );
}