document.addEventListener('DOMContentLoaded', function () {
    const legalEntityDropdown = document.getElementById('legalEntityDropdown');
    const equipClassDropdown = document.getElementById('equipClassDropdown');
    const equipSubclassDropdown = document.getElementById('equipSubclassDropdown');

    // Update Equipment Classes when Legal Entity changes
    legalEntityDropdown.addEventListener('change', function () {
        const entityId = this.value;

        fetch(`/equipment/ajax/get_classes/${entityId}/`)
            .then(response => response.json())
            .then(data => {
                const classDropdownMenu = document.querySelector('#equipClassDropdown + .dropdown-menu');
                classDropdownMenu.innerHTML = `
                    <li>
                        <a class="dropdown-item active" href="/equipment/equipment_list/${entityId}/0">
                            Все классы оборудования
                        </a>
                    </li>
                `;

                data.classes.forEach(cls => {
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.className = 'dropdown-item text-truncate';
                    a.href = `/equipment/equipment_list/${entityId}/${cls.id}`;
                    a.textContent = cls.name;
                    li.appendChild(a);
                    classDropdownMenu.appendChild(li);

                    // Add event listener to update subclasses when a class is selected
                    a.addEventListener('click', function (event) {
                        event.preventDefault();
                        updateSubclasses(entityId, cls.id);
                    });
                });
            })
            .catch(error => {
                console.error('Error fetching equipment classes:', error);
            });
    });

    // Update Equipment Subclasses when Equipment Class changes
    function updateSubclasses(entityId, classId) {
        fetch(`/equipment/ajax/get_subclasses/${classId}/`)
            .then(response => response.json())
            .then(data => {
                const subclassDropdownMenu = document.querySelector('#equipSubclassDropdown + .dropdown-menu');
                subclassDropdownMenu.innerHTML = `
                    <li>
                        <a class="dropdown-item active" href="/equipment/equipment_list/${entityId}/${classId}/0">
                            Все подклассы оборудования
                        </a>
                    </li>
                `;

                data.subclasses.forEach(subclass => {
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.className = 'dropdown-item text-truncate';
                    a.href = `/equipment/equipment_list/${entityId}/${classId}/${subclass.id}`;
                    a.textContent = subclass.name;
                    li.appendChild(a);
                    subclassDropdownMenu.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Error fetching equipment subclasses:', error);
            });
    }
});