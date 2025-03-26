'use client';

import { useEffect, useState } from 'react';
import Navbar from '../ui/components/Navbar';
import styles from '../ui/styles/dashboard.module.css';
// for charts
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend
);

// Simulating an API response or JSON object
const mockTips = {
    tips: [
        'Consider a bigger pot',
        'Water the plant more',
        'It is dead, buy a new one',
    ],
};

export default function Dashboard() {
    const [tips, setTips] = useState([]);
    const [metrics, setMetrics] = useState(null);
    const [healthStatus, setHealthStatus] = useState('loading');

    // Simulated data fetching (replace with actual API call)
    const fetchData = async () => {
        // Replace this with an actual API call:
        // const res = await fetch('/api/metrics');
        // return await res.json();

        return {
            water: [20, 35, 50, 65, 80, 90],
            temp: [22, 23, 24, 26, 28, 29],
            light: [100, 120, 130, 140, 150, 160],
            labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'],
        };
    };

    useEffect(() => {
        // Imagine this being a fetch call to your backend:
        // fetch('/api/tips').then(res => res.json()).then(data => setTips(data.tips));
        const getMetrics = async () => {
            const data = await fetchData();
            setMetrics(data);
        };
        getMetrics();
        setTips(mockTips.tips);

        // Simulated AI health check response (replace with OpenAI API call)
        const aiHealthResponse = 'good'; // This would be dynamic based on the response from OpenAI
        setHealthStatus(aiHealthResponse);
    }, []);

    // Chart Options
    const options = {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: { enabled: true },
        },
    };

    // Graph Data
    const getChartData = (label, data) => ({
        labels: metrics?.labels,
        datasets: [
            {
                label,
                data,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4,
            },
        ],
    });

    return (
        <div>
            <Navbar />
            <div className={styles.dashboardContainer}>
                <h1 className={styles.header}>Dashboard</h1>

                {/* Metrics */}
                <div className={styles.metricCard}>
                    <h3>Water</h3>
                    {metrics ? (
                        <Line
                            data={getChartData('Water', metrics.water)}
                            options={options}
                        />
                    ) : (
                        <p>Loading...</p>
                    )}
                </div>

                <div className={styles.metricCard}>
                    <h3>Temperature</h3>
                    {metrics ? (
                        <Line
                            data={getChartData('Temperature', metrics.temp)}
                            options={options}
                        />
                    ) : (
                        <p>Loading...</p>
                    )}
                </div>

                <div className={styles.metricCard}>
                    <h3>Light</h3>
                    {metrics ? (
                        <Line
                            data={getChartData('Light', metrics.light)}
                            options={options}
                        />
                    ) : (
                        <p>Loading...</p>
                    )}
                </div>

                {/* Tips & Health Check */}
                <div className={styles.tips}>
                    <h3>Tips suggested by AI:</h3>
                    {tips.length > 0 ? (
                        <ul className={styles.bulletPoints}>
                            {tips.map((tip, index) => (
                                <li key={index}>{tip}</li>
                            ))}
                        </ul>
                    ) : (
                        <p>Loading tips...</p>
                    )}
                </div>

                <div
                    className={`${styles.healthCheck} ${healthStatus === 'good' ? styles.good : styles.bad}`}
                >
                    {healthStatus === 'loading'
                        ? 'Loading Health Status...'
                        : healthStatus === 'good'
                          ? 'Good'
                          : 'Bad'}
                </div>
            </div>
        </div>
    );
}
