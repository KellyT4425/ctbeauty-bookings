// auto-submit
document.addEventListener("DOMContentLoaded", () => {
  const catSelect = document.querySelector('select[name="category"]');
  const treatSelect = document.querySelector('select[name="treatment"]');
  const availabilityField = document.querySelector(
    'select[name="availability"]'
  );
  const submitBtn = document.querySelector('button[type="submit"]');

  // Auto-submit when category/treatment change
  if (catSelect) {
    catSelect.addEventListener("change", (e) => e.target.form?.submit());
  }
  if (treatSelect) {
    treatSelect.addEventListener("change", (e) => e.target.form?.submit());
  }

  // Disable submit until an availability is picked
  if (availabilityField && submitBtn) {
    const toggleBtn = () => {
      submitBtn.disabled = !availabilityField.value;
    };
    toggleBtn(); // initial state
    availabilityField.addEventListener("change", toggleBtn);
  }
});
