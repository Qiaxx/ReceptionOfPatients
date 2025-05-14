document.addEventListener('DOMContentLoaded', function() {
    const specialtyItems = document.querySelectorAll('.specialty-item');
    const specialtyInput = document.getElementById('specialty-input');
    const filterForm = document.getElementById('filter-form');

    specialtyItems.forEach(item => {
        item.addEventListener('click', function() {
            const specialtyId = this.getAttribute('data-specialty');
            specialtyInput.value = specialtyId;
            filterForm.submit();
        });
    });

    // Sort functionality
    const sortButtons = document.querySelectorAll('.sort-btn');
    const sortInput = document.getElementById('sort-input');

    sortButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sortValue = this.getAttribute('data-sort');
            sortInput.value = sortValue;
            filterForm.submit();
        });
    });

    // Search functionality - submit on enter
    const searchInput = document.getElementById('doctor-search');

    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            filterForm.submit();
        }
    });

    // // Schedule appointment functionality
    // const scheduleButtons = document.querySelectorAll('.schedule-btn');
    //
    // scheduleButtons.forEach(button => {
    //     button.addEventListener('click', function() {
    //         const doctorId = this.getAttribute('data-doctor-id');
    //         const calendarContainer = document.querySelector(`.calendar-container[data-doctor-id="${doctorId}"]`);
    //
    //         // Закрываем другие календари
    //         document.querySelectorAll('.calendar-container').forEach(el => {
    //             if (el !== calendarContainer) el.classList.add('hidden');
    //         });
    //
    //         // Показываем или скрываем календарь
    //         if (calendarContainer.classList.contains('hidden')) {
    //             calendarContainer.innerHTML = generateCalendarHTML();  // Простейший HTML-календарь
    //             calendarContainer.classList.remove('hidden');
    //         } else {
    //             calendarContainer.classList.add('hidden');
    //         }
    //     });
    // });
    //
    // // Простая генерация HTML-календаря
    // function generateCalendarHTML() {
    //     const today = new Date();
    //     let html = '<div class="grid grid-cols-7 gap-2 text-center">';
    //     const days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
    //     days.forEach(day => html += `<div class="font-bold">${day}</div>`);
    //
    //     const year = today.getFullYear();
    //     const month = today.getMonth();
    //     const firstDay = new Date(year, month, 1).getDay();
    //     const daysInMonth = new Date(year, month + 1, 0).getDate();
    //
    //     const start = (firstDay + 6) % 7;  // чтобы понедельник был первым
    //
    //     for (let i = 0; i < start; i++) html += '<div></div>';
    //     for (let d = 1; d <= daysInMonth; d++) {
    //         html += `<div class="cursor-pointer hover:bg-teal-100 rounded p-1">${d}</div>`;
    //     }
    //
    //     html += '</div>';
    //     return html;
    // }
});
