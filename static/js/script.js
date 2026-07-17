document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // 1. Form Validation for Prediction Page
    // ----------------------------------------------------
    const predictForm = document.getElementById('predictForm');
    if (predictForm) {
        const readingInput = document.getElementById('reading_score');
        const writingInput = document.getElementById('writing_score');

        // Real-time validation for scores (0-100)
        [readingInput, writingInput].forEach(input => {
            if (input) {
                input.addEventListener('input', () => {
                    const value = parseInt(input.value);
                    if (isNaN(value) || value < 0 || value > 100) {
                        input.setCustomValidity('Score must be between 0 and 100.');
                    } else {
                        input.setCustomValidity('');
                    }
                });
            }
        });

        predictForm.addEventListener('submit', (event) => {
            let isValid = predictForm.checkValidity();
            
            // Extra check for scores
            if (readingInput && (parseInt(readingInput.value) < 0 || parseInt(readingInput.value) > 100)) {
                isValid = false;
                readingInput.classList.add('is-invalid');
            }
            if (writingInput && (parseInt(writingInput.value) < 0 || parseInt(writingInput.value) > 100)) {
                isValid = false;
                writingInput.classList.add('is-invalid');
            }

            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            predictForm.classList.add('was-validated');
        }, false);
    }

    // ----------------------------------------------------
    // 2. Prediction Results Page Visuals and Animations
    // ----------------------------------------------------
    const resultsDataEl = document.getElementById('results-data');
    if (resultsDataEl) {
        // Retrieve raw score predicted by model
        const rawScore = parseFloat(resultsDataEl.getAttribute('data-score'));
        
        // Clamp for UI rendering (progress circle is 0 - 100)
        const uiScore = Math.max(0, Math.min(100, Math.round(rawScore * 10) / 10)); 
        
        // Set up references
        const numberEl = document.getElementById('progressScoreNumber');
        const circleValEl = document.getElementById('progressCircleVal');
        const badgeEl = document.getElementById('performanceBadge');
        
        // 2a. Determine performance badge and colors
        let performanceClass = 'needs-improvement';
        let performanceText = 'Needs Improvement';
        let circleColor = 'var(--accent-rose)';
        
        if (uiScore >= 85) {
            performanceClass = 'excellent';
            performanceText = 'Excellent';
            circleColor = 'var(--accent-emerald)';
        } else if (uiScore >= 70) {
            performanceClass = 'good';
            performanceText = 'Good';
            circleColor = 'var(--accent-cyan)';
        } else if (uiScore >= 50) {
            performanceClass = 'average';
            performanceText = 'Average';
            circleColor = 'var(--accent-amber)';
        }
        
        // Apply badge details
        if (badgeEl) {
            badgeEl.className = `performance-badge ${performanceClass} fade-in-up delay-2`;
            badgeEl.textContent = performanceText;
        }
        
        // 2b. Set progress stroke color
        if (circleValEl) {
            circleValEl.style.stroke = circleColor;
        }

        // 2c. Animate score number counter
        if (numberEl) {
            let currentCount = 0;
            const duration = 2000; // 2 seconds to match circle animation
            const intervalTime = 30; // ms
            const step = (rawScore / (duration / intervalTime));
            
            const counter = setInterval(() => {
                currentCount += step;
                if (currentCount >= rawScore) {
                    clearInterval(counter);
                    numberEl.textContent = Math.round(rawScore); // display rounded integer
                } else {
                    numberEl.textContent = Math.round(currentCount);
                }
            }, intervalTime);
        }

        // 2d. Animate SVG circle stroke dashoffset
        // Radius of circle is 90, Circumference = 2 * PI * r = ~565.48
        if (circleValEl) {
            const circumference = 565.48;
            const strokeOffset = circumference - (circumference * uiScore) / 100;
            
            // Set after a brief delay to ensure DOM render has finished for transition animation
            setTimeout(() => {
                circleValEl.style.strokeDashoffset = strokeOffset;
            }, 100);
        }
    }
});
