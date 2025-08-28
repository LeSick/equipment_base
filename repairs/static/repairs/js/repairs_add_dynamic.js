document.addEventListener('DOMContentLoaded', function() {
    function updateShopsAndPositions(row) {
        const legalEntitySelect = row.querySelector('select[name$="legalentity"]');
        const shopSelect = row.querySelector('select[name$="shop"]');
        const equipmentPosSelect = row.querySelector('select[name$="pos"]');

        if (!legalEntitySelect || !shopSelect || !equipmentPosSelect) return;

        // Update shops when legal entity changes
        legalEntitySelect.addEventListener('change', function() {
            fetch(`/repairs/ajax/get-shops/?legalentity=${this.value}`)
                .then(response => response.json())
                .then(data => {
                    shopSelect.innerHTML = '<option value="">---------</option>';
                    data.forEach(shop => {
                        shopSelect.innerHTML += `<option value="${shop.id}">${shop.name}</option>`;
                    });
                    equipmentPosSelect.innerHTML = '<option value="">---------</option>';
                });
        });

        // Update equipment positions when shop changes
        shopSelect.addEventListener('change', function() {
            const legalEntityId = legalEntitySelect.value;
            fetch(`/repairs/ajax/get-equipment-positions/?legalentity=${legalEntityId}&shop=${this.value}`)
                .then(response => response.json())
                .then(data => {
                    equipmentPosSelect.innerHTML = '<option value="">---------</option>';
                    data.forEach(pos => {
                        equipmentPosSelect.innerHTML += `<option value="${pos.id}">${pos.pos}</option>`;
                    });
                });
        });
    }

    // Initialize for existing rows
    document.querySelectorAll('.form-row').forEach(updateShopsAndPositions);

    // When adding a new form row, re-initialize
    document.getElementById('add-form-btn').addEventListener('click', function() {
        setTimeout(function() {
            const rows = document.querySelectorAll('.form-row');
            updateShopsAndPositions(rows[rows.length - 1]);
        }, 100);
    });
});