// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('.file-input');
    const fileName = document.querySelector('.file-name');
    const submitBtn = document.querySelector('.submit-btn');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileName.textContent = this.files[0].name;
                submitBtn.disabled = false;
            }
        });
    }

    // Tab switching functionality
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            tab.classList.add('active');

            // Hide all tab contents
            tabContents.forEach(content => content.style.display = 'none');
            // Show selected tab content
            const targetContent = document.querySelector(tab.dataset.target);
            if (targetContent) {
                targetContent.style.display = 'block';
            }
        });
    });

    // Skills input handling
    const skillsInput = document.getElementById('skills');
    const skillsList = document.getElementById('skills-list');
    const addSkillBtn = document.getElementById('add-skill');

    if (addSkillBtn && skillsInput && skillsList) {
        addSkillBtn.addEventListener('click', function() {
            const skill = skillsInput.value.trim();
            if (skill) {
                const skillTag = document.createElement('span');
                skillTag.className = 'skill-tag';
                skillTag.textContent = skill;
                
                const removeBtn = document.createElement('button');
                removeBtn.className = 'remove-skill';
                removeBtn.innerHTML = '&times;';
                removeBtn.onclick = function() {
                    skillTag.remove();
                };
                
                skillTag.appendChild(removeBtn);
                skillsList.appendChild(skillTag);
                skillsInput.value = '';
            }
        });

        skillsInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addSkillBtn.click();
            }
        });
    }

    // Chart initialization
    if (typeof Chart !== 'undefined') {
        // Job Match Distribution Chart
        const matchCtx = document.getElementById('matchChart');
        if (matchCtx) {
            new Chart(matchCtx, {
                type: 'bar',
                data: {
                    labels: window.jobTitles || [],
                    datasets: [{
                        label: 'Match Percentage',
                        data: window.matchScores || [],
                        backgroundColor: '#4a90e2',
                        borderColor: '#357abd',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        // Skills Analysis Chart
        const skillsCtx = document.getElementById('skillsChart');
        if (skillsCtx) {
            new Chart(skillsCtx, {
                type: 'pie',
                data: {
                    labels: window.skillLabels || [],
                    datasets: [{
                        data: window.skillData || [],
                        backgroundColor: [
                            '#4a90e2',
                            '#e74c3c',
                            '#2ecc71',
                            '#f1c40f',
                            '#9b59b6'
                        ]
                    }]
                },
                options: {
                    responsive: true
                }
            });
        }
    }
}); 