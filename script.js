// Eventide booking site - main JS file

document.addEventListener('DOMContentLoaded', () => {

  // search filter for the event cards
  const searchInput = document.getElementById('event-search');
  const eventCards = document.querySelectorAll('#event-grid .event-card');
  const noResults = document.getElementById('no-results');

  searchInput.addEventListener('input', (e) => {
    const term = e.target.value.trim().toLowerCase();
    let visibleCount = 0;

    eventCards.forEach(card => {
      const name = card.dataset.name.toLowerCase();
      const matches = name.includes(term);
      card.parentElement.style.display = matches ? '' : 'none';
      if (matches) visibleCount++;
    });

    noResults.classList.toggle('d-none', visibleCount > 0);
  });

  // clicking Book Now on a card fills the form dropdown and scrolls down
  const eventSelect = document.getElementById('event-select');
  document.querySelectorAll('.book-trigger').forEach(btn => {
    btn.addEventListener('click', () => {
      eventSelect.value = btn.dataset.event;
      updateTotal();
      document.getElementById('book').scrollIntoView({ behavior: 'smooth' });
    });
  });

  // live total price
  const quantityInput = document.getElementById('quantity');
  const totalDisplay = document.getElementById('total-value');

  function updateTotal() {
    const selected = eventSelect.options[eventSelect.selectedIndex];
    const price = parseFloat(selected.dataset.price) || 0;
    const qty = parseInt(quantityInput.value, 10) || 0;
    const total = price * qty;
    totalDisplay.textContent = `Rs. ${total.toFixed(2)}`;
  }

  eventSelect.addEventListener('change', updateTotal);
  quantityInput.addEventListener('input', updateTotal);
  updateTotal();

  // form submit -> show the bootstrap modal
  const form = document.getElementById('booking-form');
  const modalBody = document.getElementById('modal-body-content');
  const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = document.getElementById('full-name').value.trim();
    const email = document.getElementById('email').value.trim();
    const eventName = eventSelect.value;
    const qty = parseInt(quantityInput.value, 10) || 0;
    const price = parseFloat(eventSelect.options[eventSelect.selectedIndex].dataset.price) || 0;
    const total = (price * qty).toFixed(2);

    if (!name || !email || !eventName || qty < 1) {
      alert('Please fill in all the fields before confirming.');
      return;
    }

    modalBody.innerHTML = `
      <p>Thanks <strong>${escapeHtml(name)}</strong>. A confirmation will be sent to <strong>${escapeHtml(email)}</strong>.</p>
      <div class="summary-row"><span>Event</span><strong>${escapeHtml(eventName)}</strong></div>
      <div class="summary-row"><span>Tickets</span><strong>${qty}</strong></div>
      <div class="summary-row"><span>Total paid</span><strong>Rs. ${total}</strong></div>
    `;

    confirmModal.show();
    form.reset();
    updateTotal();
  });

  // escape user input so it can't break the modal HTML
  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, ch => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    }[ch]));
  }
});
