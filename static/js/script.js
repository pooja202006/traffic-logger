/* script.js – Smart Traffic Violation Logger */

document.addEventListener('DOMContentLoaded', function () {

  // ── Password Show/Hide Toggle ──────────────────────────────
  const togglePwBtn = document.getElementById('togglePw');
  const togglePwIcon = document.getElementById('togglePwIcon');
  const pwInput = document.getElementById('password');

  if (togglePwBtn && pwInput) {
    togglePwBtn.addEventListener('click', function () {
      if (pwInput.type === 'password') {
        pwInput.type = 'text';
        togglePwIcon.classList.replace('bi-eye-fill', 'bi-eye-slash-fill');
      } else {
        pwInput.type = 'password';
        togglePwIcon.classList.replace('bi-eye-slash-fill', 'bi-eye-fill');
      }
    });
  }

  // ── Auto-uppercase vehicle number inputs ──────────────────
  document.querySelectorAll('input[name="vehicle_number"], input[name="vehicle"]')
    .forEach(function (el) {
      el.addEventListener('input', function () {
        const pos = this.selectionStart;
        this.value = this.value.toUpperCase();
        this.setSelectionRange(pos, pos);
      });
    });

  // ── Auto-dismiss alerts after 5 seconds ───────────────────
  document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ── Add Violation form: prevent double-submit ─────────────
  const addForm = document.getElementById('addViolationForm');
  const submitBtn = document.getElementById('submitBtn');
  if (addForm && submitBtn) {
    addForm.addEventListener('submit', function () {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving…';
    });
  }

  // ── Animate stat cards on load ────────────────────────────
  const statCards = document.querySelectorAll('.stat-card');
  statCards.forEach(function (card, i) {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(function () {
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 80 * i);
  });

  // ── Tooltip init ──────────────────────────────────────────
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

});

// ── Delete confirmation (called inline from templates) ────────
function confirmDelete(event) {
  if (!confirm('⚠️ Are you sure you want to delete this violation?\nThis action cannot be undone.')) {
    event.preventDefault();
    return false;
  }
  return true;
}
