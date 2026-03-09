// Mobile nav toggle
document.addEventListener('DOMContentLoaded', () => {
  // Close mobile nav on link click
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      document.querySelector('.nav-links').classList.remove('open');
    });
  });

  // Reading progress bar
  const progressBar = document.getElementById('reading-progress');
  if (progressBar) {
    window.addEventListener('scroll', () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = progress + '%';
    });
  }

  // Cross-promo banner rotation (leaderboard & footer)
  function rotatePromos(prefix) {
    const el1 = document.getElementById(prefix + '-1');
    const el2 = document.getElementById(prefix + '-2');
    if (!el1 || !el2) return;
    let showing = 1;
    setInterval(() => {
      if (showing === 1) {
        el1.style.opacity = '0';
        setTimeout(() => { el1.style.display = 'none'; el2.style.display = 'flex'; setTimeout(() => { el2.style.opacity = '1'; }, 50); }, 300);
        showing = 2;
      } else {
        el2.style.opacity = '0';
        setTimeout(() => { el2.style.display = 'none'; el1.style.display = 'flex'; setTimeout(() => { el1.style.opacity = '1'; }, 50); }, 300);
        showing = 1;
      }
    }, 8000);
  }
  rotatePromos('promo-leaderboard');
  rotatePromos('promo-footer');

  // Close nav on outside click
  document.addEventListener('click', (e) => {
    const nav = document.querySelector('.nav-links');
    const toggle = document.querySelector('.nav-toggle');
    if (nav && toggle && !nav.contains(e.target) && !toggle.contains(e.target)) {
      nav.classList.remove('open');
    }
  });
});

// Lazy load fade-in
document.querySelectorAll('img[loading="lazy"]').forEach(function(img) {
  if (img.complete) { img.style.opacity = '1'; }
  else { img.addEventListener('load', function() { this.style.opacity = '1'; }); }
});
