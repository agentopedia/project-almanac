export default function Navbar() {
    // return <nav className="nav">
    //     <a href="/" className="site-title">Agentopedia</a>
    //     <ul>
    //         <li>
    //             <a href="/about">About</a>
    //         </li>
    //         <li>
    //             <a href="/agents">Agents</a>
    //         </li>
    //     </ul>
    // </nav>
    return <header className="navbar">
        <div className="navbar-start"> </div>
            <div className="px-3">Home</div>
            <div className="px-3">About</div>
            <div className="px-3">Agents</div>
    </header>
}