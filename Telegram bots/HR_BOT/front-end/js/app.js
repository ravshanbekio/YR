// Shared utility functions
document.addEventListener('DOMContentLoaded', function() {
    updateNavigation();
});

function updateNavigation() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Sample data initialization (optional)
function initializeSampleData() {
    if (!localStorage.getItem('vacancies')) {
        const sampleVacancies = [
            {
                id: 1,
                position: 'Senior Developer',
                department: 'IT',
                salary: '$80,000 - $120,000',
                description: 'Seeking an experienced developer with 5+ years of experience',
                vacancyStatus: 'open'
            },
            {
                id: 2,
                position: 'Marketing Manager',
                department: 'Marketing',
                salary: '$60,000 - $90,000',
                description: 'Lead marketing campaigns and team',
                vacancyStatus: 'open'
            }
        ];
        localStorage.setItem('vacancies', JSON.stringify(sampleVacancies));
    }

    if (!localStorage.getItem('questions')) {
        const sampleQuestions = [
            {
                id: 1,
                questionText: 'What are your greatest strengths?',
                category: 'Behavioral',
                difficulty: 'easy'
            },
            {
                id: 2,
                questionText: 'Tell us about a challenging project you handled',
                category: 'Behavioral',
                difficulty: 'medium'
            }
        ];
        localStorage.setItem('questions', JSON.stringify(sampleQuestions));
    }

    if (!localStorage.getItem('applications')) {
        const sampleApplications = [
            {
                id: 1,
                name: 'John Doe',
                email: 'john@example.com',
                position: 'Senior Developer',
                appliedDate: new Date().toISOString().split('T')[0],
                status: 'new',
                coverLetter: 'I am interested in this position...'
            },
            {
                id: 2,
                name: 'Jane Smith',
                email: 'jane@example.com',
                position: 'Marketing Manager',
                appliedDate: new Date(Date.now() - 86400000).toISOString().split('T')[0],
                status: 'reviewing',
                coverLetter: 'I have 8 years of marketing experience...'
            }
        ];
        localStorage.setItem('applications', JSON.stringify(sampleApplications));
    }
}

// Uncomment to initialize with sample data
// initializeSampleData();