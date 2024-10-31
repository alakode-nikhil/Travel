document.getElementById('country-select').addEventListener('change', function() {
    const countryId = this.value;
    fetch(`/profiles/api/states/${countryId}/`)
        .then(response => response.json())
        .then(data => {
            const stateSelect = document.getElementById('state-select');
            stateSelect.innerHTML = '';
            data.forEach(state => {
                stateSelect.innerHTML += `<option value="${state.id}">${state.state_name}</option>`;
            });
        });
});

document.getElementById('state-select').addEventListener('change', function() {
    const stateId = this.value;
    fetch(`/profiles/api/districts/${stateId}/`)
        .then(response => response.json())
        .then(data => {
            const districtSelect = document.getElementById('district-select');
            districtSelect.innerHTML = '';
            data.forEach(district => {
                districtSelect.innerHTML += `<option value="${district.id}">${district.district_name}</option>`;
            });
        });
});