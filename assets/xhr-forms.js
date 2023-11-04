// xhr-forms.js
(function () {
    // Convert all HTML forms to XHR requests
    function convertFormsToXHR() {
      const forms = document.querySelectorAll('form');
      forms.forEach((form) => {
        form.addEventListener('submit', function (event) {
          event.preventDefault();
          const formData = new FormData(form);
          const xhr = new XMLHttpRequest();
          
          // Disable the submit button during the request
          const submitBtn = form.querySelector('button[type="submit"]');
          const originalBtnText = submitBtn.textContent;
          submitBtn.disabled = true;
          submitBtn.textContent = 'Loading...';
  
          xhr.open('POST', form.action);
          xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
              // Re-enable the submit button
              submitBtn.disabled = false;
              submitBtn.textContent = originalBtnText;
  
              if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                if (response.success) {
                  Swal.fire('Success', response.message, 'success');
                } else {
                  Swal.fire('Error', response.message, 'error');
                }
              } else {
                Swal.fire('Error', 'An error occurred while processing the request', 'error');
              }
            }
          };
  
          xhr.send(formData);
        });
      });
    }
  
    // Automatically initialize when the page loads
    window.addEventListener('load', convertFormsToXHR);
  })();
  