document.addEventListener('DOMContentLoaded', function() {
    fetch('/cars/api')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('cars-body');
            tbody.innerHTML = '';

            data.forEach(car => {
                const tr = document.createElement('tr');

                tr.innerHTML = `
                    <td>${car.id}</td>
                    <td>${car.brand}</td>
                    <td>${car.model}</td>
                    <td>${car.color}</td>
                    <td>${car.year}</td>
                    <td>${car.age}</td>
                    <td>${car.price}</td>
                    <td>
                        <a href="/car/{{ car.id }}">Info</a>
                        <a href="/car/edit/{{ car.id }}">Edit</a>
                        <form action="/car/remove/{{ car.id }}" method="post" style="display:inline;">
                            <input type="submit" value="Remove">
                        </form>
                    </td>
                `;

                tbody.appendChild(tr);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});

