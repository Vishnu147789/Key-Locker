// Key Locker JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Auto-hide alerts
    autoHideAlerts();
    
    // Initialize copy to clipboard
    initializeCopyClipboard();

    // Initialize password strength checker on register page only
    initPasswordChecker();
});

// All existing functions here remain the same for tooltips, validation, alerts, copy, etc.

function initializeCopyClipboard() {
    const keyValues = document.querySelectorAll('.key-value');
    keyValues.forEach(keyValue => {
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-info ms-1';
        copyButton.innerHTML = '📋';
        copyButton.title = 'Copy to clipboard';
        copyButton.type = 'button';
        copyButton.addEventListener('click', function() {
            const val = keyValue.getAttribute('data-value');
            copyToClipboard(val);
            const original = copyButton.innerHTML;
            copyButton.innerHTML = '✅';
            copyButton.classList.remove('btn-outline-info');
            copyButton.classList.add('btn-success');
            setTimeout(() => {
                copyButton.innerHTML = original;
                copyButton.classList.remove('btn-success');
                copyButton.classList.add('btn-outline-info');
            }, 1000);
        });
        keyValue.parentNode.appendChild(copyButton);
    });
}

// Password strength logic
function checkPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength +=1;
    if (/[a-z]/.test(password)) strength +=1;
    if (/[A-Z]/.test(password)) strength +=1;
    if (/[0-9]/.test(password)) strength +=1;
    if (/[^a-zA-Z0-9]/.test(password)) strength +=1;
    return strength;
}

// Initialize password strength checker only on registration page
function initPasswordChecker() {
    const pwdInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm_password');

    if(pwdInput && confirmInput) {
        const strengthContainer = document.createElement('div');
        strengthContainer.className = 'password-strength mt-2';
        pwdInput.parentNode.appendChild(strengthContainer);

        pwdInput.addEventListener('input', () => {
            const val = pwdInput.value;
            const strength = checkPasswordStrength(val);
            const colors = ['danger','warning','info','success'];
            const progressWidth = strength ? (strength / 5) * 100 : 0;

            if(val.length === 0) {
                strengthContainer.innerHTML = '';
            } else if(val.length < 6) {
                strengthContainer.innerHTML = `<small class="text-danger">Minimum 6 characters required.</small>`;
            } else {
                strengthContainer.innerHTML = `
                    <div class="progress" style="height:5px;">
                        <div class="progress-bar bg-${colors[Math.min(strength-1, colors.length-1)]}" style="width: ${progressWidth}%;"></div>
                    </div>
                `;
            }
        });
    }
}
