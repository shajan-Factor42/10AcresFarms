// 10 Acre Farms — small site script. No dependencies.
(function () {
  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Forms: point FormSubmit's redirect at our thank-you page on whatever address the site is served from.
  document.querySelectorAll('form[data-thanks]').forEach(function (form) {
    var next = form.querySelector('input[name="_next"]');
    if (next) next.value = new URL(form.getAttribute('data-thanks'), window.location.href).href;
  });

  // Order form: require at least one dozen of something.
  var order = document.getElementById('order-form');
  if (order) {
    order.addEventListener('submit', function (e) {
      var total = 0;
      order.querySelectorAll('input[data-qty]').forEach(function (i) { total += parseInt(i.value || '0', 10) || 0; });
      var err = document.getElementById('order-error');
      if (total < 1) {
        e.preventDefault();
        err.classList.add('show');
        err.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }
      err.classList.remove('show');
      if (window.gtag) window.gtag('event', 'generate_lead', { form: 'order', dozens: total });
    });
  }
  var contact = document.getElementById('contact-form');
  if (contact) contact.addEventListener('submit', function () {
    if (window.gtag) window.gtag('event', 'generate_lead', { form: 'contact' });
  });

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
