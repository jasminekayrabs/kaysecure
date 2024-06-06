document.addEventListener("DOMContentLoaded", function() {
    let slides = document.querySelectorAll('.slide');
    let currentSlide = 0;
    showSlides(currentSlide); // Initially show the first slide

    function showSlides(n) {
        // Hide all slides
        for (let slide of slides) {
            slide.style.display = "none";
        }
        // Show the correct slide
        slides[n].style.display = "block";
    }

    // Next/previous controls
    document.getElementById('nextBtn').addEventListener('click', function() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlides(currentSlide);
    });

    document.getElementById('prevBtn').addEventListener('click', function() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlides(currentSlide);
    });
});