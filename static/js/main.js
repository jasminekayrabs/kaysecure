// document.addEventListener('DOMContentLoaded', function() {
//     let slideIndex = 1;
//     showSlides(slideIndex);

//     document.querySelector('.prev').addEventListener('click', function() {
//         showSlides(--slideIndex);
//     });

//     document.querySelector('.next').addEventListener('click', function() {
//         showSlides(++slideIndex);
//     });

//     function showSlides(n) {
//         let slides = document.getElementsByClassName("card");
//         if (n > slides.length) { slideIndex = 1 }
//         if (n < 1) { slideIndex = slides.length }
//         Array.from(slides).forEach(card => card.style.display = "none");
//         slides[slideIndex - 1].style.display = "block";
//     }
// });
