document.addEventListener('DOMContentLoaded', function() {
  const dateInput = document.getElementById('date');
  const timeSlotsContainer = document.getElementById('time-slots-container');
  const selectedTimeInput = document.getElementById('selected-time');
  const formattedSelection = document.getElementById('formatted-selection');
  const doctorId = '{{ doctor.id }}';
  let selectedTimeSlot = null;

  // Set minimum date to today
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  dateInput.min = `${yyyy}-${mm}-${dd}`;

  // Format date for display
  function formatDate(dateString) {
    const options = { day: 'numeric', month: 'long' };
    return new Date(dateString).toLocaleDateString('ru-RU', options);
  }

  // Update the formatted selection text
  function updateFormattedSelection() {
    if (dateInput.value && selectedTimeSlot) {
      const formattedDate = formatDate(dateInput.value);
      formattedSelection.textContent = `${formattedDate} ${selectedTimeSlot}`;
    } else {
      formattedSelection.textContent = 'выбранное время';
    }
  }

  // Select a time slot
  function selectTimeSlot(timeSlot) {
    selectedTimeSlot = timeSlot;
    selectedTimeInput.value = timeSlot;

    // Update UI
    const timeSlotButtons = timeSlotsContainer.querySelectorAll('.time-slot-btn');
    timeSlotButtons.forEach(btn => {
      if (btn.textContent === timeSlot) {
        btn.classList.add('selected');
      } else {
        btn.classList.remove('selected');
      }
    });

    updateFormattedSelection();
  }

  // Fetch available time slots when date changes
  dateInput.addEventListener('change', function() {
    const date = this.value;

    // Show loading state
    timeSlotsContainer.innerHTML = '<div class="col-span-4 text-center text-stone-500">Загрузка доступных слотов...</div>';

    // Reset selected time
    selectedTimeSlot = null;
    selectedTimeInput.value = '';

    // Fetch available slots from API
    fetch(`/patient/api/free_slots/?date=${date}&doctor_id=${doctorId}`)
      .then(response => response.json())
      .then(data => {
        console.log(data);

        if (data.slots && data.slots.length > 0) {
          // Clear container
          timeSlotsContainer.innerHTML = '';

          // Add time slot buttons
          data.slots.forEach(time => {
            const timeBtn = document.createElement('button');
            timeBtn.type = 'button'; // Prevent form submission on click
            timeBtn.className = 'time-slot-btn p-2.5 rounded border border-solid cursor-pointer border-zinc-300';
            timeBtn.textContent = time;

            timeBtn.addEventListener('click', function() {
              selectTimeSlot(time);
            });

            timeSlotsContainer.appendChild(timeBtn);
          });
        } else {
          timeSlotsContainer.innerHTML = '<div class="col-span-4 text-center text-stone-500">Нет доступных слотов на выбранную дату</div>';
        }

        updateFormattedSelection();
      })
      .catch(error => {
        console.error('Error fetching time slots:', error);
        timeSlotsContainer.innerHTML = '<div class="col-span-4 text-center text-red-500">Ошибка при загрузке слотов. Пожалуйста, попробуйте еще раз.</div>';
      });

    updateFormattedSelection();
  });

  // Form validation before submit
  document.querySelector('.appointment-form').addEventListener('submit', function(e) {
    if (!dateInput.value || !selectedTimeInput.value) {
      e.preventDefault();
      alert('Пожалуйста, выберите дату и время приёма');
    }
  });
});
