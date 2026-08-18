document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const bookingForm = document.getElementById('booking-form');
    const genderCards = document.querySelectorAll('.gender-card');
    const ageInput = document.getElementById('age-input');
    const presetBtns = document.querySelectorAll('.preset-btn');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    const calculateBtn = document.getElementById('calculate-btn');
    const btnText = calculateBtn.querySelector('.btn-text');
    const btnSpinner = document.getElementById('btn-spinner');

    // Ticket Result Elements
    const ticketResultSection = document.getElementById('ticket-result');
    const ticketCategoryBadge = document.getElementById('ticket-category-badge');
    const ticketGender = document.getElementById('ticket-gender');
    const ticketAge = document.getElementById('ticket-age');
    const ticketBasePrice = document.getElementById('ticket-base-price');
    const ticketDiscountPercent = document.getElementById('ticket-discount-percent');
    const ticketDiscountAmount = document.getElementById('ticket-discount-amount');
    const ticketFinalPrice = document.getElementById('ticket-final-price');
    const ticketPnr = document.getElementById('ticket-pnr');

    // Gender Card Selection Handler
    genderCards.forEach(card => {
        card.addEventListener('click', () => {
            genderCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            const radioInput = card.querySelector('input[type="radio"]');
            if (radioInput) radioInput.checked = true;
            hideError();
        });
    });

    // Age Preset Buttons Handler
    presetBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const age = btn.getAttribute('data-age');
            ageInput.value = age;
            hideError();
            ageInput.focus();
        });
    });

    // Input change handler
    ageInput.addEventListener('input', () => {
        hideError();
    });

    // Form Submission Handler
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();

        // Get selected gender
        const selectedGenderCard = document.querySelector('.gender-card.active input[name="gender"]');
        const gender = selectedGenderCard ? selectedGenderCard.value : 'male';
        const age = ageInput.value.trim();

        // Front-end Pre-validation
        if (!age) {
            showError("Please enter the valid age");
            return;
        }

        const ageNum = Number(age);
        if (isNaN(ageNum) || ageNum < 0 || ageNum > 100) {
            showError("Please enter the valid age");
            return;
        }

        // Trigger Loading state
        setLoading(true);

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    gender: gender,
                    age: ageNum
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                showError(data.error || "Please enter the valid age");
                ticketResultSection.classList.add('hidden');
            } else {
                renderTicket(data);
            }
        } catch (err) {
            console.error("API error:", err);
            showError("Network error while connecting to server. Please try again.");
        } finally {
            setLoading(false);
        }
    });

    // Render Ticket Details
    function renderTicket(data) {
        ticketGender.textContent = data.gender === 'male' ? 'Male' : 'Female';
        ticketAge.textContent = `${data.age} yrs`;
        ticketCategoryBadge.textContent = data.category;

        // Category Badge Color styling
        if (data.discount_percent >= 50) {
            ticketCategoryBadge.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        } else if (data.discount_percent > 0) {
            ticketCategoryBadge.style.background = 'linear-gradient(135deg, #2563eb, #1d4ed8)';
        } else {
            ticketCategoryBadge.style.background = 'linear-gradient(135deg, #64748b, #475569)';
        }

        ticketBasePrice.textContent = `Rs. ${data.base_price}`;
        ticketDiscountPercent.textContent = `${data.discount_percent}%`;
        ticketDiscountAmount.textContent = `- Rs. ${data.discount_amount.toFixed(0)}`;
        ticketFinalPrice.textContent = `Rs. ${data.final_price.toFixed(0)}`;

        // Generate PNR
        const randomPnr = 'RAIL-' + Math.floor(1000000 + Math.random() * 9000000);
        ticketPnr.textContent = `PNR: ${randomPnr}`;

        // Reveal ticket section with animation
        ticketResultSection.classList.remove('hidden');
        ticketResultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Helper functions
    function showError(msg) {
        errorMessage.textContent = msg;
        errorAlert.classList.remove('hidden');
    }

    function hideError() {
        errorAlert.classList.add('hidden');
    }

    function setLoading(isLoading) {
        if (isLoading) {
            calculateBtn.disabled = true;
            btnText.style.opacity = '0.5';
            btnSpinner.classList.remove('hidden');
        } else {
            calculateBtn.disabled = false;
            btnText.style.opacity = '1';
            btnSpinner.classList.add('hidden');
        }
    }
});
