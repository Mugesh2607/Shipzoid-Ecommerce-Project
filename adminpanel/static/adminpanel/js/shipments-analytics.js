           
           initShipmentChart() {
                const ctx = document.getElementById('shipmentChart').getContext('2d');
                
                this.charts.shipment = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        datasets: [{
                            label: 'Shipments',
                            data: [120, 190, 300, 500, 200, 300, 450],
                            borderColor: '#4ECDC4',
                            backgroundColor: 'rgba(78, 205, 196, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointBackgroundColor: '#4ECDC4',
                            pointBorderColor: '#ffffff',
                            pointBorderWidth: 2,
                            pointRadius: 6,
                        }, {
                            label: 'Delivered',
                            data: [100, 170, 280, 480, 180, 280, 420],
                            borderColor: '#1e3a8a',
                            backgroundColor: 'rgba(30, 58, 138, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointBackgroundColor: '#1e3a8a',
                            pointBorderColor: '#ffffff',
                            pointBorderWidth: 2,
                            pointRadius: 6,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    usePointStyle: true,
                                    padding: 20,
                                    font: {
                                        family: 'Inter',
                                        size: 12,
                                        weight: '500'
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: {
                                    color: 'rgba(226, 232, 240, 0.5)',
                                },
                                ticks: {
                                    font: {
                                        family: 'Inter',
                                        size: 11
                                    },
                                    color: '#64748b'
                                }
                            },
                            x: {
                                grid: {
                                    display: false,
                                },
                                ticks: {
                                    font: {
                                        family: 'Inter',
                                        size: 11
                                    },
                                    color: '#64748b'
                                }
                            }
                        },
                        elements: {
                            point: {
                                hoverRadius: 8,
                            }
                        },
                        interaction: {
                            intersect: false,
                            mode: 'index',
                        },
                        animation: {
                            duration: 2000,
                            easing: 'easeInOutCubic'
                        }
                    }
                });
            }


                        updateShipmentChart() {
                const period = document.getElementById('chart-period').value;
                let newData, newLabels;

                switch(period) {
                    case '7':
                        newLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
                        newData = [
                            [120, 190, 300, 500, 200, 300, 450],
                            [100, 170, 280, 480, 180, 280, 420]
                        ];
                        break;
                    case '30':
                        newLabels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
                        newData = [
                            [1200, 1890, 2100, 2450],
                            [1100, 1670, 1980, 2320]
                        ];
                        break;
                    case '90':
                        newLabels = ['Month 1', 'Month 2', 'Month 3'];
                        newData = [
                            [8200, 9890, 11200],
                            [7100, 8670, 10180]
                        ];
                        break;
                }

                this.charts.shipment.data.labels = newLabels;
                this.charts.shipment.data.datasets[0].data = newData[0];
                this.charts.shipment.data.datasets[1].data = newData[1];
                this.charts.shipment.update('active');
            }