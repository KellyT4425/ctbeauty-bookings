// auto-submit
document.addEventListener("DOMContentLoaded", function () {
  const catSelect = document.querySelector('select[name="category"]');
  if (catSelect) {
    catSelect.addEventListener("change", function () {
      this.form.submit();
    });
  }
  const treatSelect = document.querySelector('select[name="treatment"]');
  if (treatSelect) {
    treatSelect.addEventListener("change", function () {
      this.form.submit();
    });
  }
});

// disable submit button until availability selected
document.addEventListener("DOMContentLoaded", function () {
  const availabilityField = document.querySelector(
    'select[name="availability"]'
  );
  const submitBtn = document.querySelector('button[type="submit"]');
  function toggleBtn() {
    submitBtn.disabled = !availabilityField.value;
  }
  toggleBtn();
  availabilityField.addEventListener("change", toggleBtn);
});
