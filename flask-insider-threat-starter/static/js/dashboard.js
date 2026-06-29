document.addEventListener('DOMContentLoaded', function() {
    // Global Chart Defaults for Dark Theme
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', -apple-system, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.9)';
    Chart.defaults.plugins.tooltip.titleColor = '#f8fafc';
    Chart.defaults.plugins.tooltip.bodyColor = '#e2e8f0';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(56, 189, 248, 0.2)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    
    // Theme Colors
    const colors = {
        primary: '#00ffff',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
        info: '#00ffff',
        purple: '#b300ff'
    };

    // 1. Threat Trend Analysis (Line Chart)
    const threatLineCtx = document.getElementById('threatLineChart');
    if (threatLineCtx) {
        // Dummy historical data for demonstration of line chart
        const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        
        // Creating a gradient for the line chart fill
        const gradient = threatLineCtx.getContext('2d').createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(179, 0, 255, 0.4)');
        gradient.addColorStop(1, 'rgba(179, 0, 255, 0.0)');

        new Chart(threatLineCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Threats Detected',
                    data: [12, 19, 15, 25, 22, 30, Math.max(...threatTrendsData) || 28], // using backend data for the last day
                    borderColor: colors.purple,
                    backgroundColor: gradient,
                    borderWidth: 2,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: '#05060A',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: colors.primary,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4 // smooth curves
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)',
                            drawBorder: false
                        },
                        border: { display: false }
                    },
                    x: {
                        grid: { display: false },
                        border: { display: false }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
            }
        });
    }

    // 2. Risk Distribution (Doughnut Chart)
    const riskDoughnutCtx = document.getElementById('riskDoughnutChart');
    if (riskDoughnutCtx && typeof riskDistributionData !== 'undefined') {
        new Chart(riskDoughnutCtx, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: riskDistributionData,
                    backgroundColor: [
                        colors.success,
                        colors.warning,
                        colors.danger
                    ],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%', // thin ring
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            boxWidth: 8,
                            font: { size: 11 }
                        }
                    }
                }
            }
        });
    }

    // Initialize tooltips and popovers if any
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
});
