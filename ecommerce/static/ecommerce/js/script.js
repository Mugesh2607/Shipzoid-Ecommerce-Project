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
                        'slideUp': 'slideUp 0.6s ease-out',
                        'scaleIn': 'scaleIn 0.3s ease-out',
                        'bounce-slow': 'bounce 2s infinite',
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
                        slideUp: {
                            'from': { opacity: '0', transform: 'translateY(30px)' },
                            'to': { opacity: '1', transform: 'translateY(0)' }
                        },
                        scaleIn: {
                            'from': { opacity: '0', transform: 'scale(0.9)' },
                            'to': { opacity: '1', transform: 'scale(1)' }
                        }
                    }
                }
            }
        }



        