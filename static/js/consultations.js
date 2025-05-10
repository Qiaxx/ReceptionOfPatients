document.addEventListener('DOMContentLoaded', function() {
  // Tab management
  const tabButtons = document.querySelectorAll('[role="tab"]');
  let activeTab = "Запись на прием"; // Default active tab

  // Set up tab click handlers
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      setActiveTab(button.dataset.tab);
    });

    // Keyboard accessibility
    button.addEventListener('keydown', (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        setActiveTab(button.dataset.tab);
      }
    });
  });

  // Function to set active tab
  function setActiveTab(tabName) {
    activeTab = tabName;

    // Update tab button states
    tabButtons.forEach(button => {
      const isActive = button.dataset.tab === activeTab;
      button.classList.toggle('active', isActive);
      button.setAttribute('aria-selected', isActive);
      button.tabIndex = isActive ? 0 : -1;
    });

    // Update tabpanel aria-label
    const tabPanel = document.querySelector('[role="tabpanel"]');
    if (tabPanel) {
      tabPanel.setAttribute('aria-label', activeTab);
    }
  }

  // Set up action buttons
  const consultationButton = document.querySelector('[data-action="consultation"]');
  if (consultationButton) {
    consultationButton.addEventListener('click', () => {
      alert("Консультация запрошена");
    });

    consultationButton.addEventListener('keydown', (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        alert("Консультация запрошена");
      }
    });
  }

  const appointmentButton = document.querySelector('[data-action="appointment"]');
  if (appointmentButton) {
    appointmentButton.addEventListener('click', () => {
      alert("Запись создана");
    });

    appointmentButton.addEventListener('keydown', (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        alert("Запись создана");
      }
    });
  }
});
