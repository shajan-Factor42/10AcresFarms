// 10 Acre Farms — small site script. No dependencies.
(function () {
  // FormSubmit redirect: send people to our thank-you page on whatever address the site is served from.
  document.querySelectorAll('form[data-thanks]').forEach(function (form) {
    var next = form.querySelector('input[name="_next"]');
    if (next) next.value = new URL(form.getAttribute('data-thanks'), window.location.href).href;
    form.addEventListener('submit', function () {
      if (window.gtag) window.gtag('event', 'generate_lead', { form: form.id });
    });
  });

  // Track order button clicks once analytics is installed (D-012).
  document.querySelectorAll('[data-track]').forEach(function (el) {
    el.addEventListener('click', function () {
      if (window.gtag) window.gtag('event', el.getAttribute('data-track'), { label: el.textContent.trim() });
    });
  });

  // Order form: preselect from ?eggs=, live total, require at least one dozen.
  var order = document.getElementById('order-form');
  if (order) {
    var qs = new URLSearchParams(window.location.search);
    if (qs.get('eggs') === 'duck') { order.querySelector('#chicken').value = 0; order.querySelector('#duck').value = 1; }
    var qty = order.querySelectorAll('input[data-qty]');
    var totalEl = document.getElementById('order-total');
    function sum() {
      var dozens = 0, dollars = 0;
      qty.forEach(function (i) { var n = Math.max(0, parseInt(i.value || '0', 10) || 0); dozens += n; dollars += n * parseFloat(i.getAttribute('data-price')); });
      totalEl.textContent = '$' + dollars;
      return dozens;
    }
    qty.forEach(function (i) { i.addEventListener('input', sum); });
    sum();
    order.addEventListener('submit', function (e) {
      var err = document.getElementById('order-error');
      if (sum() < 1) { e.preventDefault(); err.classList.add('show'); err.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
      else err.classList.remove('show');
    });
  }

  // Thank-you page wording for egg list signups.
  var msg = document.getElementById('thanks-msg');
  if (msg && new URLSearchParams(window.location.search).get('list')) {
    msg.textContent = "You're on the egg list. We'll email you when eggs are ready.";
  }
})();
