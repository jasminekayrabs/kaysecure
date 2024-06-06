document.addEventListener("DOMContentLoaded", function() {
    var slides = document.querySelectorAll('.slide');
    var currentSlide = 0;
    var slideContainer = document.getElementById('slide-container');
    var prevBtn = document.getElementById('prevBtn');
    var nextBtn = document.getElementById('nextBtn');
    var startQuizBtn = document.getElementById('startQuizBtn');
    var quizForm = document.getElementById('quiz-form');
    var quizTimer = document.getElementById('quizTimer');

    function updateSlideView(slideId) {
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams({ slide_id: slideId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.all_slides_viewed) {
                startQuizBtn.disabled = false;
            }
        })
        .catch(error => console.error('Error:', error));
    }

    if (slides.length > 0) {
        slides[currentSlide].style.display = 'block'; // Show the first slide
        updateSlideView(slides[currentSlide].dataset.slideId);
    }

    function changeSlide(step) {
        slides[currentSlide].style.display = 'none'; // Hide the current slide
        currentSlide = (currentSlide + step + slides.length) % slides.length; // Calculate the new index
        slides[currentSlide].style.display = 'block'; // Show the new slide
        updateSlideView(slides[currentSlide].dataset.slideId);
    }

    prevBtn.addEventListener('click', function() {
        changeSlide(-1);
    });

    nextBtn.addEventListener('click', function() {
        changeSlide(1);
    });

    startQuizBtn.addEventListener('click', function() {
        slideContainer.style.display = 'none'; // Hide the slides
        prevBtn.style.display = 'none'; // Hide the 'Previous' button
        nextBtn.style.display = 'none'; // Hide the 'Next' button
        startQuizBtn.style.display = 'none'; // Hide the 'Start Quiz' button
        
        quizForm.style.display = 'block'; // Show the quiz form
        quizTimer.style.display = 'block'; // Display the timer
        startTimer(); // Start the countdown timer

        var quizQuestions = document.querySelectorAll('.quiz-question');
        quizQuestions.forEach(function(question, index) {
            setTimeout(function() {
                question.classList.remove('hidden');
            }, index * 100); // Delay each question's appearance
        });
    });

    

    function startTimer() {
        let timeLeft = 300; // 300 seconds = 5 minutes
        var timerInterval = setInterval(function() {
            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            quizTimer.textContent = `Time left: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            timeLeft--;
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                quizForm.submit(); // Automatically submit the quiz when time is up
            }
        }, 1000);
    }

    quizForm.onsubmit = function(e) {
        e.preventDefault();
        console.log('Form submitted');
        var formData = new FormData(this);
        
        // Collect answers in the expected format
        var userAnswers = [];
        for (var pair of formData.entries()) {
            if (pair[0].startsWith('question_')) {
                userAnswers.push(pair[1]);
            }
        }
        console.log('User answers:', userAnswers);

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(response => {
            console.log('Raw response:', response);

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                return response.text().then(text => {
                    console.error('Response is not in JSON format. Response text:', text);
                    throw new Error('Response is not in JSON format');
                });
            }
        })
        .then(data => {
            console.log('Parsed response data:', data);
            alert(data.message);
            if (data.success) {
                window.location.href = data.next_url;
            } else {
                // alert('Failed to pass the quiz. Try again!');
                window.location.reload(); // Reload the page to retake the quiz
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Error submitting the quiz.');
        });
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
