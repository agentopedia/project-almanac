"use client"

import { useState } from 'react';
import { useRouter } from 'next/navigation';

const SkateSpotApp = () => {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        age: '',
        skillLevel: 'beginner',
        favoriteSpot: '',
        buttonName: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleButtonClick = async (buttonName) => {
        setLoading(true);
        setError(null);

        try {
            const res = await fetch('/api/swe_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'navigate',
                    buttonName: buttonName,
                    formData: formData
                }),
            });

            if (!res.ok) {
                throw new Error('Failed to perform action');
            }

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const res = await fetch('/api/swe_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'navigate',
                    ...formData,
                }),
            });

            if (!res.ok) {
                throw new Error('Failed to submit form');
            }


        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container-fluid">
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                <a className="navbar-brand" href="#">
                    SkateSpot
                </a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ml-auto">
                        <li className="nav-item">
                            <button className="nav-link btn btn-link text-white" onClick={() => handleButtonClick('find_spots')}>Find Spots</button>
                        </li>
                        <li className="nav-item">
                            <button className="nav-link btn btn-link text-white" onClick={() => handleButtonClick('trick_tutorials')}>Trick Tutorials</button>
                        </li>
                        <li className="nav-item">
                            <button className="nav-link btn btn-link text-white" onClick={() => handleButtonClick('community_feed')}>Community Feed</button>
                        </li>
                        <li className="nav-item">
                            <button className="nav-link btn btn-link text-white" onClick={() => handleButtonClick('progress_tracker')}>Progress Tracker</button>
                        </li>
                    </ul>
                </div>
            </nav>

            <div className="jumbotron bg-light text-center py-5">
                <h1 className="display-4">Welcome to SkateSpot</h1>
                <p className="lead">Discover, share, and track your skateboarding journey.</p>
                <button className="btn btn-primary btn-lg" onClick={() => handleButtonClick('get_started')}>Get Started</button>
            </div>

            <div className="container mt-4">
                <div className="row">
                    <div className="col-md-4">
                        <div className="card shadow-sm">
                            <div className="card-body">
                                <h5 className="card-title">Explore Skate Spots</h5>
                                <p className="card-text">Find the best skate spots in your city and around the world.</p>
                                <button className="btn btn-success" onClick={() => handleButtonClick('explore_spots')}>Explore Now</button>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="card shadow-sm">
                            <div className="card-body">
                                <h5 className="card-title">Learn New Tricks</h5>
                                <p className="card-text">Access a library of trick tutorials to improve your skills.</p>
                                <button className="btn btn-info text-white" onClick={() => handleButtonClick('learn_tricks')}>Learn More</button>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="card shadow-sm">
                            <div className="card-body">
                                <h5 className="card-title">Connect with Community</h5>
                                <p className="card-text">Share your progress and connect with fellow skaters.</p>
                                <button className="btn btn-warning" onClick={() => handleButtonClick('join_community')}>Join Now</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="container mt-5">
                <h2>Sign Up</h2>
                {error && <div className="alert alert-danger">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="username" className="form-label">Username</label>
                        <input
                            type="text"
                            className="form-control"
                            id="username"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">Email</label>
                        <input
                            type="email"
                            className="form-control"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="age" className="form-label">Age</label>
                        <input
                            type="number"
                            className="form-control"
                            id="age"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="skillLevel" className="form-label">Skill Level</label>
                        <select
                            className="form-control"
                            id="skillLevel"
                            name="skillLevel"
                            value={formData.skillLevel}
                            onChange={handleChange}
                        >
                            <option value="beginner">Beginner</option>
                            <option value="intermediate">Intermediate</option>
                            <option value="advanced">Advanced</option>
                        </select>
                    </div>

                    <div className="mb-3">
                        <label htmlFor="favoriteSpot" className="form-label">Favorite Spot</label>
                        <input
                            type="text"
                            className="form-control"
                            id="favoriteSpot"
                            name="favoriteSpot"
                            value={formData.favoriteSpot}
                            onChange={handleChange}
                        />
                    </div>
                    <button type="submit" className="btn btn-success" disabled={loading}>
                        {loading ? 'Signing Up...' : 'Sign Up'}
                    </button>
                </form>
            </div>

            <footer className="footer mt-auto py-3 bg-dark text-white text-center">
                <div className="container">
                    <span className="text-muted">SkateSpot - Connecting Skaters Worldwide &copy; {new Date().getFullYear()}</span>
                </div>
            </footer>
            <div className="flex justify-center mt-8 mb-8">
                <button
                    className="btn btn-secondary"
                    onClick={() => router.push("/swe")}
                >
                    Back to SWE Agent
                </button>
            </div>
        </div>
    );
};

export default SkateSpotApp;