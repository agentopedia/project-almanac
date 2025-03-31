"use client"

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const CosmicCompanion = () => {
    const router = useRouter();
    const [location, setLocation] = useState<{ latitude: number | null; longitude: number | null }>({
        latitude: null,
        longitude: null,
      });
    const [skyData, setSkyData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        favoriteObject: '',
    });

    useEffect(() => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setLocation({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                    });
                },
                (error) => {
                    console.error("Error getting location:", error);
                    setError("Failed to get location. Please enable location services.");
                }
            );
        } else {
            setError("Geolocation is not supported by this browser.");
        }
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const fetchSkyData = async () => {
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
                    buttonName: 'Fetch Sky Data',
                    formData: {
                        latitude: location.latitude,
                        longitude: location.longitude
                    }
                }),
            });

            if (!res.ok) {
                throw new Error('Failed to fetch sky data');
            }

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleButtonClick = async (buttonName: string) => {
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
                throw new Error('Navigation failed');
            }

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container-fluid bg-dark text-light p-5">
            <div className="row">
                <div className="col-md-8">
                    <h1 className="display-4">Explore the Cosmos with Cosmic Companion</h1>
                    <p className="lead">Your personal guide to the night sky. Discover stars, planets, and constellations in real-time.</p>
                    <hr className="my-4" style={{ borderColor: '#fff' }} />
                    {error && <div className="alert alert-danger">{error}</div>}
                    {location.latitude && location.longitude ? (
                        <>
                            <p>Your location: Latitude {location.latitude.toFixed(2)}, Longitude {location.longitude.toFixed(2)}</p>
                            <button className="btn btn-outline-info btn-lg" onClick={fetchSkyData} disabled={loading}>
                                {loading ? 'Loading sky data...' : 'View Sky Data'}
                            </button>
                        </>
                    ) : (
                        <p>Waiting for location...</p>
                    )}

                    {skyData && (
                        <div className="mt-4">
                            <h2>Sky Data</h2>
                            <pre>{JSON.stringify(skyData, null, 2)}</pre>
                        </div>
                    )}
                </div>

                <div className="col-md-4">
                    <div className="card bg-secondary text-white">
                        <img
                            src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Night_sky.jpg/800px-Night_sky.jpg"
                            className="card-img-top"
                            alt="Night Sky"
                            style={{ maxHeight: '200px', objectFit: 'cover' }}
                        />
                        <div className="card-body">
                            <h5 className="card-title">Discover a Universe of Information</h5>
                            <p className="card-text">Dive deep into our comprehensive database of celestial objects.</p>
                            <button onClick={() => handleButtonClick('object_database')} className="btn btn-primary">Explore Now</button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row mt-5">
                <div className="col-md-6">
                    <h2 className="mb-4">Stay Updated on Astronomical Events</h2>
                    <p>Never miss a meteor shower or lunar eclipse. Our calendar keeps you informed.</p>
                    <button onClick={() => handleButtonClick('astronomical_events')} className="btn btn-success btn-lg">View Calendar</button>
                </div>

                <div className="col-md-6">
                    <h2 className="mb-4">Personalize Your Experience</h2>
                    <form>
                        <div className="mb-3">
                            <label htmlFor="username" className="form-label">Username</label>
                            <input type="text" className="form-control" id="username" name="username" value={formData.username} onChange={handleChange} />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="email" className="form-label">Email address</label>
                            <input type="email" className="form-control" id="email" name="email" value={formData.email} onChange={handleChange} />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="favoriteObject" className="form-label">Favorite Celestial Object</label>
                            <input type="text" className="form-control" id="favoriteObject" name="favoriteObject" value={formData.favoriteObject} onChange={handleChange} />
                        </div>
                        <button type="button" className="btn btn-warning" onClick={() => handleButtonClick('personalize')}>Save Preferences</button>
                    </form>
                </div>
            </div>

            <footer className="mt-5 text-center">
                <p>&copy; 2024 Cosmic Companion. All rights reserved.</p>
                <a href="https://www.nasa.gov/" className="text-info" target="_blank" rel="noopener noreferrer">Learn more about NASA</a>
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

export default CosmicCompanion;