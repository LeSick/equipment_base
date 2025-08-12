document.addEventListener('DOMContentLoaded', function() {
    const addBtn = document.getElementById('add-form-btn');
    const container = document.getElementById('formset-container');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');

    addBtn.addEventListener('click', function() {
        const currentFormCount = parseInt(totalForms.value);
        const lastRow = container.querySelector('.form-row:last-child');
        const emptyRow = lastRow.cloneNode(true);

        // Clear the values in the cloned form
        emptyRow.querySelectorAll('input, select, textarea').forEach(function(input) {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = false;
            } else {
                input.value = '';
            }
        });
        // Clear duration field
        emptyRow.querySelectorAll('.duration-field').forEach(function(input) {
            input.value = '';
        });

        // Update the form index in the cloned row
        emptyRow.innerHTML = emptyRow.innerHTML.replace(
            new RegExp(`form-${currentFormCount - 1}-`, 'g'),
            `form-${currentFormCount}-`
        );

        container.appendChild(emptyRow);
        totalForms.value = currentFormCount + 1;
    });

    // Duration calculation
    function calculateDuration(row) {
        const startInput = row.querySelector('input[name$="start"]');
        const endInput = row.querySelector('input[name$="end"]');
        const durationInput = row.querySelector('.duration-field');
        if (!startInput || !endInput || !durationInput) return;

        function updateDuration() {
            const startVal = startInput.value;
            const endVal = endInput.value;
            if (startVal && endVal) {
                const startDate = new Date(startVal);
                const endDate = new Date(endVal);
                if (!isNaN(startDate) && !isNaN(endDate) && endDate > startDate) {
                    const diffMs = endDate - startDate;
                    const diffHrs = diffMs / (1000 * 60 * 60);
                    durationInput.value = diffHrs.toFixed(2);
                } else {
                    durationInput.value = '';
                }
            } else {
                durationInput.value = '';
            }
        }

        startInput.addEventListener('change', updateDuration);
        endInput.addEventListener('change', updateDuration);
    }

    // Initialize duration calculation for all rows
    function initDurationAllRows() {
        document.querySelectorAll('.form-row').forEach(calculateDuration);
    }
    initDurationAllRows();

    // When adding a new form row, re-initialize
    addBtn.addEventListener('click', function() {
        setTimeout(function() {
            const rows = document.querySelectorAll('.form-row');
            calculateDuration(rows[rows.length - 1]);
        }, 100);
    });
});