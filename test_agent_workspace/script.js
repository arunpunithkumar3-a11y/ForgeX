// script.js
// ModernSite Interactivity & Animations
// -------------------------------------
// Navbar, smooth scroll, modal, carousel, fade-in/slide-up

/* Hamburger Navigation for Mobile */
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

/* Smooth Scroll */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const targetId = this.getAttribute('href').slice(1);
    const targetSection = document.getElementById(targetId);
    if(targetSection) {
      e.preventDefault();
      window.scrollTo({
        top: targetSection.offsetTop - 60,
        behavior: "smooth"
      });
      if(navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
      }
    }
  });
});

/* Modal Popup for CTA */
const ctaBtn = document.getElementById('cta-btn');
const ctaModal = document.getElementById('cta-modal');
const closeModal = document.getElementById('closeModal');

ctaBtn.addEventListener('click', () => {
  ctaModal.style.display = 'flex';
});
closeModal.addEventListener('click', () => {
  ctaModal.style.display = 'none';
});
window.addEventListener('click', (e) => {
  if(e.target === ctaModal) {
    ctaModal.style.display = 'none';
  }
});

/* Testimonials Carousel */
const testimonials = document.querySelectorAll('.testimonial');
let currentIdx = 0;
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

function showTestimonial(idx) {
  testimonials.forEach((el, i) => {
    el.classList.remove('active');
    if(i === idx) el.classList.add('active');
  });
}
prevBtn.addEventListener('click', () => {
  currentIdx = (currentIdx - 1 + testimonials.length) % testimonials.length;
  showTestimonial(currentIdx);
});
nextBtn.addEventListener('click', () => {
  currentIdx = (currentIdx + 1) % testimonials.length;
  showTestimonial(currentIdx);
});
showTestimonial(currentIdx);

/* Fade-in / slide-up animations on scroll */
const fadeElems = document.querySelectorAll('.feature-card, .testimonial, .hero-content');

function handleFadeIn(){
  fadeElems.forEach(elem => {
    const rect = elem.getBoundingClientRect();
    if(rect.top < window.innerHeight - 60){
      elem.style.animationPlayState = 'running';
    }
  });
}
window.addEventListener('scroll', handleFadeIn);
window.addEventListener('load', handleFadeIn);
