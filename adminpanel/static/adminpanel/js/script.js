            tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'shipzoid-teal': '#4ECDC4',
                        'shipzoid-teal-light': '#7EDDD6',
                        'shipzoid-teal-dark': '#3BB5AF',
                        'shipzoid-navy': '#1e3a8a',
                        'shipzoid-navy-light': '#3b82f6',
                        'shipzoid-navy-dark': '#1e40af',
                        'shipzoid-navy-darker': '#1e293b',
                    },
                    fontFamily: {
                        'inter': ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
                    },
                    animation: {
                        'fadeIn': 'fadeIn 0.6s ease-out',
                        'slideIn': 'slideIn 0.8s ease-out',
                        'float': 'float 3s ease-in-out infinite',
                        'pulse': 'pulse 2s infinite',
                        'countUp': 'countUp 0.8s ease-out',
                        'slideUp': 'slideUp 0.6s ease-out',
                        'shimmer': 'shimmer 3s linear infinite',
                    },
                    keyframes: {
                        fadeIn: {
                            'from': { opacity: '0', transform: 'translateY(20px)' },
                            'to': { opacity: '1', transform: 'translateY(0)' }
                        },
                        slideIn: {
                            'from': { opacity: '0', transform: 'translateX(-30px)' },
                            'to': { opacity: '1', transform: 'translateX(0)' }
                        },
                        float: {
                            '0%, 100%': { transform: 'translateY(0px)' },
                            '50%': { transform: 'translateY(-10px)' }
                        },
                        countUp: {
                            'from': { opacity: '0', transform: 'scale(0.5)' },
                            'to': { opacity: '1', transform: 'scale(1)' }
                        },
                        slideUp: {
                            'from': { opacity: '0', transform: 'translateY(30px)' },
                            'to': { opacity: '1', transform: 'translateY(0)' }
                        },
                        shimmer: {
                            '0%': { 'background-position': '-200% 0' },
                            '100%': { 'background-position': '200% 0' }
                        }
                    }
                }
            }
        }



        window.addEventListener("load", function () {
            const loader = document.getElementById("page-loader");
            if (loader) {
            loader.classList.add("opacity-0", "pointer-events-none");
            setTimeout(() => loader.remove(), 500); // Remove from DOM after fade
            }
        });
        
        // Dashboard Controller
        class ShipzoidDashboard {
            constructor() {
                this.init();
                this.setupEventListeners();
                this.initializeCharts();
                this.startRealTimeUpdates();
            }

            init() {
                this.sidebar = document.getElementById('sidebar');
                this.mainContent = document.getElementById('main-content');
                this.mobileOverlay = document.getElementById('mobile-overlay');
                this.mobileMenuBtn = document.getElementById('mobile-menu-btn');
                this.breadcrumbCurrent = document.getElementById('breadcrumb-current');
                
                this.currentPage = 'overview';
                this.isMobile = window.innerWidth <= 1024;
                this.sidebarOpen = false;
                
                this.charts = {};
                this.realTimeInterval = null;
            }

            setupEventListeners() {
                // Mobile menu toggle
                this.mobileMenuBtn.addEventListener('click', () => this.toggleMobileSidebar());
                
                // Mobile overlay click
                this.mobileOverlay.addEventListener('click', () => this.closeMobileSidebar());

                // Navigation items
                // document.querySelectorAll('[data-page]').forEach(item => {
                //     item.addEventListener('click', (e) => {
                //         e.preventDefault();
                //         this.navigateToPage(item.dataset.page, item);
                //     });
                // });

                // Search functionality
                document.getElementById('sidebar-search').addEventListener('input', (e) => {
                    this.filterNavigation(e.target.value);
                });

                // Window resize
                window.addEventListener('resize', () => {
                    this.isMobile = window.innerWidth <= 1024;
                    if (!this.isMobile) {
                        this.closeMobileSidebar();
                    }
                    this.resizeCharts();
                });

                // Chart period changes
                document.getElementById('chart-period').addEventListener('change', () => {
                    this.updateShipmentChart();
                });

                document.getElementById('performance-period').addEventListener('change', () => {
                    this.updatePerformanceChart();
                });

                // Quick actions
                // document.querySelectorAll('[data-action]').forEach(btn => {
                //     btn.addEventListener('click', (e) => {
                //         e.preventDefault();
                //         this.handleQuickAction(btn.dataset.action);
                //     });
                // });
            }

            toggleMobileSidebar() {
                this.sidebarOpen = !this.sidebarOpen;
                
                if (this.sidebarOpen) {
                    this.sidebar.classList.remove('-translate-x-full');
                    this.sidebar.classList.add('translate-x-0');
                    this.mobileOverlay.classList.remove('opacity-0', 'invisible');
                    this.mobileOverlay.classList.add('opacity-100', 'visible');
                    document.body.style.overflow = 'hidden';
                } else {
                    this.closeMobileSidebar();
                }
            }

            closeMobileSidebar() {
                this.sidebarOpen = false;
                this.sidebar.classList.add('-translate-x-full');
                this.sidebar.classList.remove('translate-x-0');
                this.mobileOverlay.classList.add('opacity-0', 'invisible');
                this.mobileOverlay.classList.remove('opacity-100', 'visible');
                document.body.style.overflow = '';
            }

            navigateToPage(page, navItem) {
                // Update active state
                document.querySelectorAll('.nav-item.active').forEach(item => {
                    item.classList.remove('active', 'bg-gradient-to-r', 'from-shipzoid-teal', 'to-shipzoid-teal-dark', 'text-white', 'border-shipzoid-teal-light', 'shadow-lg', 'shadow-shipzoid-teal/30');
                });
                navItem.classList.add('active', 'bg-gradient-to-r', 'from-shipzoid-teal', 'to-shipzoid-teal-dark', 'text-white', 'border-shipzoid-teal-light', 'shadow-lg', 'shadow-shipzoid-teal/30');

                // Update breadcrumb
                this.breadcrumbCurrent.textContent = this.getPageTitle(page);

                // Close mobile sidebar if open
                if (this.isMobile && this.sidebarOpen) {
                    this.closeMobileSidebar();
                }

                this.currentPage = page;
                
                // Here you would typically load different content based on the page
                console.log(`Navigated to: ${page}`);
            }

            getPageTitle(page) {
                const titles = {
                    'overview': 'Dashboard Overview',
                    'analytics': 'Advanced Analytics',
                    'realtime': 'Real-time Monitoring',
                    'shipments': 'Shipment Management',
                    'tracking': 'Live Tracking',
                    'routes': 'Route Planning',
                    'warehouses': 'Warehouse Management',
                    'orders': 'Order Management',
                    'pending': 'Pending Orders',
                    'processing': 'Processing Orders',
                    'delivered': 'Delivered Orders',
                    'customers': 'Customer Management',
                    'reports': 'Reports & Analytics',
                    'billing': 'Billing & Payments',
                    'settings': 'System Settings'
                };
                return titles[page] || 'Dashboard';
            }

            filterNavigation(query) {
                const navItems = document.querySelectorAll('.nav-item');
                const sections = document.querySelectorAll('nav > div > div');

                if (!query) {
                    navItems.forEach(item => item.style.display = '');
                    sections.forEach(section => section.style.display = '');
                    return;
                }

                const searchTerm = query.toLowerCase();

                navItems.forEach(item => {
                    const text = item.textContent.toLowerCase();
                    const matches = text.includes(searchTerm);
                    item.style.display = matches ? '' : 'none';
                });

                sections.forEach(section => {
                    const visibleItems = section.querySelectorAll('.nav-item:not([style*="display: none"])');
                    section.style.display = visibleItems.length > 0 ? '' : 'none';
                });
            }

            initializeCharts() {
                this.initShipmentChart();
                this.initPerformanceChart();
                this.initRevenueChart();
            }

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

            initPerformanceChart() {
                const ctx = document.getElementById('performanceChart').getContext('2d');
                
                this.charts.performance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['On Time', 'Delayed', 'Lost', 'Returned'],
                        datasets: [{
                            label: 'Delivery Status',
                            data: [85, 10, 2, 3],
                            backgroundColor: [
                                '#4ECDC4',
                                '#f59e0b',
                                '#ef4444',
                                '#6b7280'
                            ],
                            borderColor: [
                                '#3BB5AF',
                                '#d97706',
                                '#dc2626',
                                '#4b5563'
                            ],
                            borderWidth: 2,
                            borderRadius: 8,
                            borderSkipped: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: false
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
                        animation: {
                            duration: 2000,
                            easing: 'easeInOutCubic'
                        }
                    }
                });
            }

            initRevenueChart() {
                const ctx = document.getElementById('revenueChart').getContext('2d');
                
                this.charts.revenue = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Express', 'Standard', 'Economy', 'International'],
                        datasets: [{
                            data: [40, 30, 20, 10],
                            backgroundColor: [
                                '#4ECDC4',
                                '#1e3a8a',
                                '#f59e0b',
                                '#10b981'
                            ],
                            borderColor: '#ffffff',
                            borderWidth: 3,
                            hoverOffset: 10
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '60%',
                        plugins: {
                            legend: {
                                position: 'bottom',
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

            updatePerformanceChart() {
                const period = document.getElementById('performance-period').value;
                let newData;

                switch(period) {
                    case 'weekly':
                        newData = [85, 10, 2, 3];
                        break;
                    case 'monthly':
                        newData = [88, 8, 2, 2];
                        break;
                    case 'quarterly':
                        newData = [90, 6, 2, 2];
                        break;
                }

                this.charts.performance.data.datasets[0].data = newData;
                this.charts.performance.update('active');
            }

            resizeCharts() {
                Object.values(this.charts).forEach(chart => {
                    chart.resize();
                });
            }

            startRealTimeUpdates() {
                this.realTimeInterval = setInterval(() => {
                    this.updateStats();
                }, 30000); // Update every 30 seconds
            }

            updateStats() {
                // Simulate real-time stat updates
                const revenue = document.getElementById('revenue-value');
                const shipments = document.getElementById('shipments-value');
                const sidebarRevenue = document.getElementById('sidebar-revenue');
                const sidebarShipments = document.getElementById('sidebar-shipments');

                // Add small random variations to stats
                const currentRevenue = parseFloat(revenue.textContent.replace('$', '').replace('K', '')) * 1000;
                const currentShipments = parseInt(shipments.textContent.replace(',', ''));

                const newRevenue = currentRevenue + (Math.random() - 0.5) * 1000;
                const newShipments = currentShipments + Math.floor((Math.random() - 0.5) * 10);

                revenue.textContent = '$' + (newRevenue / 1000).toFixed(1) + 'K';
                shipments.textContent = newShipments.toLocaleString();
                sidebarRevenue.textContent = '$' + (newRevenue / 1000).toFixed(1) + 'K';
                sidebarShipments.textContent = newShipments.toLocaleString();
            }

            handleQuickAction(action) {
                console.log(`Quick action: ${action}`);
                // Here you would implement the actual functionality for each action
                
                // Show a simple notification for demo purposes
                const notification = document.createElement('div');
                notification.className = 'fixed top-4 right-4 bg-shipzoid-teal text-white px-6 py-3 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300';
                notification.textContent = `Action: ${action.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}`;
                
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.classList.remove('translate-x-full');
                }, 100);
                
                setTimeout(() => {
                    notification.classList.add('translate-x-full');
                    setTimeout(() => {
                        document.body.removeChild(notification);
                    }, 300);
                }, 3000);
            }
        }

        // Initialize the dashboard when the page loads
        document.addEventListener('DOMContentLoaded', () => {
            new ShipzoidDashboard();
        });